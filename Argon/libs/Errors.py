import os
import sys

def error(msg):
    line = getenv("currentLine")
    print(f"{msg}. Error from line: {line}")
    sys.exit(1)
def warning():
    pass
def setenv(name,value):
    os.environ[name] = value
def getenv(name):
    return os.environ[name]