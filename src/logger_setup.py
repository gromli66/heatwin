import logging
import logging.config
import yaml
import os

def setup_logging(config_path="configs/logging.yaml"):
    os.makedirs("logs", exist_ok=True)
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    logging.config.dictConfig(config)