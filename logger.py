import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/automation.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("InternshipAutomation")