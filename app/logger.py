# app/logger.py
import logging
import sys
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

# Create a logger named 'giftai'
logger = logging.getLogger("giftai")
logger.setLevel(logging.INFO)  # Set the logging level

# Create a stream handler to output logs to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)  # Set handler level

# Create and set the formatter
formatter = JsonFormatter()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
