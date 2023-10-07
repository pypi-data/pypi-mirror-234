from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TransactionRecord(BaseModel):
    latency_ms: Optional[int] = None
    status_code: Optional[int] = None
    input_text: str
    output_text: Optional[str] = None
    model: str
    num_input_tokens: Optional[int] = None
    num_output_tokens: Optional[int] = None
    num_total_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    trace_id: Optional[str] = None
    parent_trace_id: Optional[str] = None
    output_logprobs: Optional[Dict] = None
    created_at: str
    tags: Optional[List[str]] = None
    user_metadata: Optional[Dict[str, Any]] = None
    temperature: Optional[float] = None


class TransactionRecordBatch(BaseModel):
    records: List[TransactionRecord]
