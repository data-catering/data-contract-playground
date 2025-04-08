import sys
import logging

# Create a mock venv.logger module
class MockVenv:
    class Logger:
        def info(self, msg):
            logging.info(msg)
            
        def debug(self, msg):
            logging.debug(msg)
            
        def warning(self, msg):
            logging.warning(msg)
            
        def error(self, msg):
            logging.error(msg)

# Create the mock module
mock_venv = MockVenv()
mock_venv.logger = MockVenv.Logger()

# Add it to sys.modules
sys.modules['venv'] = mock_venv