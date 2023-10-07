from typing import Optional
import uuid


class ProcessCmd:
    idempotency_id: str

    def __init__(self, idempotency_id: Optional[str] = None):
        self.idempotency_id = (
            idempotency_id if idempotency_id is not None else str(uuid.uuid4())
        )
