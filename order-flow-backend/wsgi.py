import sys
import os

# Add the backend folder to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "order-flow-backend"))

from main import app

