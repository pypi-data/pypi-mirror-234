import atexit
import signal
import sys
import threading
from os import getenv
from typing import Any, Callable

from llm_monitor.schema.transaction import TransactionRecord, TransactionRecordBatch
from llm_monitor.utils.api_client import ApiClient

# static
LOOP_INTERVAL = 1
BATCH_SEND_INTERVAL = 10
MAX_BATCH_SIZE = 25
SEND_THRESHOLD = 5
WINDOWS_LIMIT = 5

# variable
BATCH = []
ELAPSED_WINDOWS = 0

IS_STREAMLIT = getenv("IS_STREAMLIT", False)

client: ApiClient


def initialize_api_client(project_name: str) -> None:
    global client
    client = ApiClient(project_name=project_name)


# This method is called by handlers/wrappers to add a new
# record to the send queue
def add_record_to_batch(record: TransactionRecord) -> None:
    global BATCH
    BATCH.append(record)
    # If we've hit our max BATCH size, don't wait for the next interval
    if len(BATCH) == MAX_BATCH_SIZE:
        _send_batch()


def _send_batch(force_send: bool = False) -> None:
    global BATCH
    global ELAPSED_WINDOWS

    if len(BATCH) > 0:
        if (
            not force_send
            and (len(BATCH) < SEND_THRESHOLD)
            and (ELAPSED_WINDOWS < WINDOWS_LIMIT)
        ):
            ELAPSED_WINDOWS = ELAPSED_WINDOWS + 1
        else:
            try:
                transaction_batch = TransactionRecordBatch(records=BATCH)
                client.ingest_batch(transaction_batch)
                BATCH = []
                ELAPSED_WINDOWS = 0
            except Exception as e:
                print(f"Caught exception in aggregator thread: {e}")


class AggregatorJob(threading.Thread):
    def __init__(self, execute: Callable, *args: Any, **kwargs: Any) -> None:
        threading.Thread.__init__(self)
        self.daemon = True
        self.stopped = threading.Event()
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

        # Send whatever is left in the queue before exiting
        atexit.register(_send_batch, force_send=True)

    def stop(self) -> None:
        self.stopped.set()
        self.join()

    def run(self) -> None:
        elapsed_time = 0
        while not self.stopped.wait(LOOP_INTERVAL):
            if elapsed_time >= BATCH_SEND_INTERVAL:
                self.execute(*self.args, **self.kwargs)
                elapsed_time = 0
            else:
                elapsed_time = elapsed_time + LOOP_INTERVAL


aggregator_job: AggregatorJob


def _signal_handler(signum: Any, frame: Any) -> None:
    global aggregator_job
    aggregator_job.stop()
    sys.exit()


def start_aggregator_job() -> None:
    global aggregator_job
    if not IS_STREAMLIT:
        # Add signal handlers to make sure we terminate the send_batch job thread
        # Streamlit apps run in a sub-process, so we can't set these
        signal.signal(signal.SIGTERM, _signal_handler)
        signal.signal(signal.SIGINT, _signal_handler)

    # Create the send_batch timed job and start it
    aggregator_job = AggregatorJob(execute=_send_batch)
    aggregator_job.start()
