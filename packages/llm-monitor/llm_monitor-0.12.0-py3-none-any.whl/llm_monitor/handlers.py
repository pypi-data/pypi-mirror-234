import time
from datetime import datetime
from typing import Any, Dict, List

import pytz
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult

from llm_monitor.schema.transaction import TransactionRecord
from llm_monitor.utils.aggregator import (
    add_record_to_batch,
    initialize_api_client,
    start_aggregator_job,
)


class MonitorHandler(BaseCallbackHandler):
    timers: Dict[str, Dict[str, float]] = {}
    records: Dict[str, TransactionRecord] = {}

    def __init__(self, project_name: str, *args: Any, **kwargs: Any) -> None:
        """LangChain callbackbander for LLM Monitoring

        Parameters
        ----------
        project_name : str
            Name of the project to log to
        """
        initialize_api_client(project_name=project_name)
        start_aggregator_job()
        super().__init__(*args, **kwargs)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        input_text = prompts[0]
        run_id = kwargs["run_id"]
        self.timers[run_id] = {}
        self.timers[run_id]["start"] = time.perf_counter()

        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")

        model = kwargs["invocation_params"]["model_name"]
        temperature = kwargs["invocation_params"].get("temperature")
        self.records[run_id] = TransactionRecord(
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
        )

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        input_text = messages[0][0].content
        run_id = kwargs["run_id"]
        self.timers[run_id] = {}
        self.timers[run_id]["start"] = time.perf_counter()

        tags = kwargs.get("tags")
        metadata = kwargs.get("metadata")

        model = kwargs["invocation_params"]["model_name"]
        temperature = kwargs["invocation_params"].get("temperature")
        self.records[run_id] = TransactionRecord(
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
            temperature=temperature,
            tags=tags,
            user_metadata=metadata,
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        run_id = kwargs["run_id"]
        self.timers[run_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[run_id]["stop"] - self.timers[run_id]["start"]) * 1000
        )
        del self.timers[run_id]

        generation = response.generations[0][0]
        if hasattr(generation, "message"):
            output_text = generation.message.content
        else:
            output_text = generation.text
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
            num_input_tokens = usage.get("prompt_tokens", 0)
            num_output_tokens = usage.get("completion_tokens", 0)
            num_total_tokens = usage.get("total_tokens", 0)

        if generation.generation_info:
            finish_reason = generation.generation_info.get("finish_reason", "")

        model_dict = self.records[run_id].model_dump()
        model_dict.update(
            output_text=output_text,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            finish_reason=finish_reason,
            trace_id=str(kwargs["run_id"]),
            parent_trace_id=str(kwargs["parent_run_id"]),
            latency_ms=latency_ms,
            status_code=200,
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[run_id]

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> Any:
        """Run when LLM errors."""
        run_id = kwargs["run_id"]
        self.timers[run_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[run_id]["stop"] - self.timers[run_id]["start"]) * 1000
        )
        del self.timers[run_id]

        model_dict = self.records[run_id].model_dump()
        model_dict.update(
            output_text=f"ERROR: {error}",
            num_input_tokens=0,
            num_output_tokens=0,
            num_total_tokens=0,
            latency_ms=latency_ms,
            status_code=getattr(error, "http_status", 500),
        )

        add_record_to_batch(TransactionRecord(**model_dict))
        del self.records[run_id]
