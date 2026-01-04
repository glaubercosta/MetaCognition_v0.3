import logging
import sys
from pythonjsonlogger import jsonlogger
from contextvars import ContextVar
import datetime

# Context variable to store request_id
request_id_ctx = ContextVar("request_id", default=None)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add timestamp
        if not log_record.get("timestamp"):
            now = datetime.datetime.now(datetime.UTC).isoformat()
            log_record["timestamp"] = now
            
        # Add log level
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        # Add request_id if available
        req_id = request_id_ctx.get()
        if req_id:
            log_record["request_id"] = req_id

def setup_logging():
    """Configure root logger to use JSON formatter."""
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Mute noisy libraries
    logging.getLogger("uvicorn.access").disabled = True # We will log requests ourselves if needed
    
    return logger

# Initialize on import? Or let main call it?
# Better to let main call it.
