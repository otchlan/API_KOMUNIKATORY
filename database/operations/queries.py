import os
import logging
from database.models import Message
from database.db_session import db

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('logs/queries.log')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Create stream handler for console
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info("queries.py module loaded. Logger configuration initialized.")

def get_all_messages():
    logger.info("Function 'get_all_messages()' called.")
    
    try:        
        if db:
            logger.info("Successfully connected to the database.")
        else:
            logger.warning("Failed to establish a connection to the database.")
            return None, None
        
        messages = db.query(Message).all()
        
        if messages:
            logger.info(f"Successfully fetched {len(messages)} messages from the database.")
        else:
            logger.warning("No messages found in the database.")
        
        columns = [column.name for column in Message.__table__.columns]
        
        if columns:
            logger.info(f"Fetched column headers: {', '.join(columns)}")
        else:
            logger.warning("No column headers found for the Message table.")
        
        return messages, columns
    
    except Exception as e:
        logger.error(f"Error occurred while fetching messages: {str(e)}")
        return None, None
