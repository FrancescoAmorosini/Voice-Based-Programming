

from wit import Wit
import sys
import pyjulius3
import queue

#
# # Initialize and try to connect
# client = pyjulius3.Client('localhost', 10500)
# try:
#     client.connect()
# except pyjulius3.ConnectionError:
#     print('Start julius as module first!')
#     sys.exit(1)
#
# # Start listening to the server
# client.start()
#
# try:
#     while 1:
#         try:
#
#             result = client.results.get(False)
#
#         except queue.Empty:
#             continue
#
#         if isinstance(result, pyjulius3.Sentence):
#           print('Sentence "%s" recognized with score %.2f' % (result, result.score))
# except KeyboardInterrupt:
#     print('Exiting...')
#     client.disconnect()  # disconnect from julius

client = Wit("JWG5NMZBJQYCCXVSRNC7K5B3YKM2XQQJ")
with open('Recording2.wav', 'rb') as f:
  resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp))