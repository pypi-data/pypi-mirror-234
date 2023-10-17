import sys

import logging
import logging.config
from tracemalloc import start
logging.captureWarnings(True)
logging.basicConfig(stream=sys.stdout)

from app import app, server

# register callbacks
from routes import render_page_content
from helpers.utils import start_kinit_daemon

if __name__ == '__main__':
    start_kinit_daemon() # independent of Dash APP
    app.run_server(debug=True, host='0.0.0.0', port=18880)
