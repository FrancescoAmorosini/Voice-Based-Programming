import sys
import pyjulius3
import Queue


# Initialize and try to connect
client = pyjulius3.Client('localhost', 10500)