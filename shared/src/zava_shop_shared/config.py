import logging
import os
import pathlib

# Load environment variables from .env file if dotenv is available
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # dotenv not available, continue without it
    pass

# Configure basic logging to show INFO level messages
logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(message)s")

# Suppress verbose Azure logging
for name in [
    "azure.core.pipeline.policies.http_logging_policy",
    "azure.ai.agents",
    "azure.ai.projects",
    "azure.core",
    "azure.identity",
    "uvicorn.access",
]:
    logging.getLogger(name).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class Config:
    """Configuration class for managing application settings."""

    def __init__(self):
        """Initialize configuration with environment variables."""

        ABS_DB_PATH = "sqlite+aiosqlite:////workspace/data/retail.db"

        # Use absolute path if running in container (/workspace exists), else compute absolute path
        if pathlib.Path("/workspace").exists():
            DEFAULT_SQLITE_URL = ABS_DB_PATH
        else:
            # Compute absolute path to data/retail.db from the shared module location
            shared_dir = pathlib.Path(__file__).parent.parent.parent.parent
            db_path = (shared_dir / "data" / "retail.db").resolve()
            DEFAULT_SQLITE_URL = f"sqlite+aiosqlite:///{db_path}"

        # SQLite database URL
        self._sqlite_database_url: str = self._clean_env_value(
            os.getenv("SQLITE_DATABASE_URL", DEFAULT_SQLITE_URL)
        )

    def _clean_env_value(self, value: str) -> str:
        """Strip surrounding quotes that might be added by Docker."""
        return value.strip('"').strip("'") if value else ""

    @property
    def sqlite_database_url(self) -> str:
        """Returns the SQLite database URL."""
        return self._sqlite_database_url
