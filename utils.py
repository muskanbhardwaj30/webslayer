import hashlib
import logging
import os
from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme or "http"
    netloc = p.netloc.lower()
    path = p.path.rstrip("/")
    return urlunparse((scheme, netloc, path, "", "", ""))


def url_to_hash(url: str) -> str:
    norm = normalize_url(url)   
    return hashlib.md5(norm.encode("utf-8")).hexdigest()
    

def setup_logger(log_file="logs/app.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Get or create the logger
    logger = logging.getLogger("web_chatbot")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    return logger
