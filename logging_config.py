import logging

logging.basicConfig(
    filename="project_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("project_logger")
