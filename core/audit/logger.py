import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger("EnterpriseAuditLogger")
logger.setLevel(logging.INFO)

class AuditLogger:
    @staticmethod
    def log_security_event(tenant_id: str, user_id: str, action: str, details: Dict[str, Any]) -> None:
        audit_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "action": action,
            "details": details
        }
        logger.info(f"AUDIT_EVENT: {audit_record}")

audit_logger = AuditLogger()