import logging
import os
import warnings

class generateLog():

    def __init__(self, path):
        self.path = f"{path}/files.log"

    def setLog(self):
        self.__createfile()

    def __createfile(self):
        log_dir = os.path.dirname(self.path)
        if not os.path.exists(log_dir) and log_dir != "":
            os.makedirs(log_dir)
        else:
            raise ValueError("Folder already exist")
        if not os.path.exists(self.path):
            with open(self.path, 'w'):
                pass

    def __setsettings(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.path),
            ]
        )
        sklearn_logger = logging.getLogger('sklearn')
        sklearn_logger.setLevel(logging.DEBUG)
        def log_warnings(message, category, filename, lineno, file=None, line=None):
            logging.warning(f"{category.__name__}: {message} (in {filename} at line {lineno})")
        warnings.showwarning = log_warnings
