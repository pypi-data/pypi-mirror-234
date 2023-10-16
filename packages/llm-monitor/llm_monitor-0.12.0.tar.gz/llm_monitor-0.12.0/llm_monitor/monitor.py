import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

import pytz

from llm_monitor.schema.transaction import TransactionRecord
from llm_monitor.utils.aggregator import (
    add_record_to_batch,
    initialize_api_client,
    start_aggregator_job,
)


class LLMMonitor:
    timers: Dict[str, Dict[str, float]] = {}
    records: Dict[str, TransactionRecord] = {}

    def __init__(self, project_name: str, *args: Any, **kwargs: Any) -> None:
        """Initializes LLM Monitor

        Parameters
        ----------
        project_name : str
            The name of the project to log to
        """
        initialize_api_client(project_name=project_name)
        start_aggregator_job()

    def log_prompt(
        self,
        prompt: str,
        model: str,
        temperature: Optional[float],
        parent_trace_id: Optional[str],
    ) -> str:
        """Logs the beginning of a LLM request

        Parameters
        ----------
        prompt : str
            Prompt text as a string
        model : str
            Name of the model being prompted
        temperature : Optional[float]
            Temperature setting being passed to LLM
        parent_trace_id : Optional[str]
            ID of parent if there is one, e.g. chain

        Returns
        -------
        str
            ID of the trace being initiated
        """
        trace_id = str(uuid4())

        self.timers[trace_id] = {}
        self.timers[trace_id]["start"] = time.perf_counter()

        self.records[trace_id] = TransactionRecord(
            input_text=prompt,
            model=model,
            temperature=temperature,
            trace_id=trace_id,
            parent_trace_id=parent_trace_id,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
        )
        return trace_id

    def log_completion(
        self,
        trace_id: str,
        output_text: str,
        num_input_tokens: int,
        num_output_tokens: int,
        num_total_tokens: int,
        finish_reason: Optional[str] = None,
        status_code: Optional[int] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Logs the completion of the LLM request

        Parameters
        ----------
        trace_id : str
            ID of the trace started with log_prompt()
        output_text : str
            Completion text from the LLM response
        num_input_tokens : int
            Number of input tokens
        num_output_tokens : int
            Number of output tokens
        num_total_tokens : int
            Total number of tokens
        finish_reason : Optional[str]
            Finish reason from the LLM
        status_code : Optional[int]
            Status code of the API call to the LLM
        user_metadta : Optional[Dict[str, Any]]
            User-defined metadata as key-value pairs
        tags : Optional[List[str]]
            User-defined tags as a list of strings
        """
        self.timers[trace_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[trace_id]["stop"] - self.timers[trace_id]["start"]) * 1000
        )
        del self.timers[trace_id]

        model_dict = self.records[trace_id].model_dump()
        model_dict.update(
            output_text=output_text,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            finish_reason=finish_reason,
            latency_ms=latency_ms,
            status_code=status_code or 200,
            user_metadata=user_metadata,
            tags=tags,
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[trace_id]

    def log_error(
        self, trace_id: str, error_message: str, status_code: Optional[int]
    ) -> None:
        """Logs an error from an LLM caal

        Parameters
        ----------
        trace_id : str
            ID of the trace started with log_prompt()
        error_message : str
            Error message returned from the LLM
        status_code : Optional[int]
            Status code of the API request to the LLM
        """
        self.timers[trace_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[trace_id]["stop"] - self.timers[trace_id]["start"]) * 1000
        )
        del self.timers[trace_id]

        model_dict = self.records[trace_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error_message}",
            num_input_tokens=0,
            num_output_tokens=0,
            num_total_tokens=0,
            latency_ms=latency_ms,
            status_code=status_code or 500,
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[trace_id]
