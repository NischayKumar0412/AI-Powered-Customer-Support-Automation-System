from typing import TypedDict, List, Dict, Any, Optional, Annotated
import operator

class SupportState(TypedDict):
    customer_id: str
    messages: Annotated[list, operator.add]
    query: str
    intent: Optional[str]
    retrieved_context: Optional[str]
    requires_approval: bool
    approval_status: Optional[str]
    draft_response: Optional[str]
    final_response: Optional[str]
