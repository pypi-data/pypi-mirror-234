import sys
import os

os.environ["ENVIRONMENT"] = "test"

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
