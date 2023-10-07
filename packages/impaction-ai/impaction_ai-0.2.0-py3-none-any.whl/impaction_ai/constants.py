class EventTypes:
    SESSION_OPEN = "session_open"
    SESSION_CLOSE = "session_close"
    USER_RECOGNIZE = "user_recognize"
    MESSAGE_CREATE = "message_create"


ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"

DEFAULT_ASSISTANT_ID = "DEFAULT"


FLUSH_INTERVAL_MS = 3000  # regular flush interval
FLUSH_BATCH_SIZE = 50
FLUSH_TIMEOUT_SECONDS = 5
MAX_BUFFER_SIZE = 200
BUFFER_CONSUME_WAIT_TIME_MS = 3000  # Wait time when buffery is empty
API_MAX_RETIRES = 3


SERVER_BASE_URL = "https://api.impaction.ai"
