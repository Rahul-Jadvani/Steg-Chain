import os
import json
import logging

# Default Configuration
CONFIG = {
    'paths': {
        'key_file_directory': os.path.join(os.path.expanduser("~"), "Desktop", "coding", "UNI", "StegChain", "Key_file"),
    },
    'ui': {
        'text_field_width': 500,
        'theme_color': 'indigo',
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
    },
    'global_message': "Default message to be encrypted or decrypted",
}

# Load Configuration from External File
def load_config(config_path="config.json"):
    global CONFIG
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            file_config = json.load(file)
        CONFIG.update(file_config)
    return CONFIG

# Setup Logging
def setup_logging():
    logging.basicConfig(
        level=getattr(logging, CONFIG['logging']['level']),
        format=CONFIG['logging']['format']
    )

# Initialize
setup_logging()
logging.info("Configuration loaded successfully.")
