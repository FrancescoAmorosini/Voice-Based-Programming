from wit import Wit
import sys
import pyjulius3
import queue
from word2number import w2n

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


print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
with open('..\Recording2.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp))
if resp['intents'][0]['name'] == 'DeclareVariable':
    print("This Message is an DeclareVariable")
if resp['intents'][0]['name'] == 'IfElseStatement':
    print("This Message is an IfElseStatement")
if resp['intents'][0]['name'] == 'IfStatements':
    print("This Message is an IfStatements")
if resp['intents'][0]['name'] == 'AddingComment':
    print("This Message is an AddingComment")
if resp['intents'][0]['name'] == 'IfElseStatement':
    print("This Message is an IfElseStatement")

print(w2n.word_to_num("two million three thousand nine hundred and eighty four"))
print("This is one line of code"
      "this is the same line so they should not be separated"
      "/n this one is a new line i want to see if its noticed")
print("this is a new print command")
