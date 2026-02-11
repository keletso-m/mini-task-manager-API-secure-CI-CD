import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_security_event(message):
    logging.warning(f"[SECURITY EVENT] {message}")
    

