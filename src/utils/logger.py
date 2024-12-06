import logging
from datetime import datetime
import os

def setup_logger(store_id=None):
    """Setup logger with file and console handlers"""
    timestamp = datetime.now().strftime('%m%d_%H%M')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Logger name based on store_id or default
    logger_name = f"store_{store_id}" if store_id else "menu_test"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # File handler
    log_file = f"logs/{logger_name}_{timestamp}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 