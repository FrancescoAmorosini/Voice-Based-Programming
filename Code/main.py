from wit import Wit
import sys
import pyjulius3
import queue
import re
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
with open('CommentHelloWorld.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp) + '\n')
message = ""
if_else = 0
while(True):
    if resp['intents'][0]['name'] == 'DeclareVariable':
        print("This Message is an DeclareVariable")

    if resp['intents'][0]['name'] == 'IfElseStatement':
        if_else = 1
        command_if = resp['entities']['command:command'][0]['body']
        command_else = resp['entities']['command:command'][1]['body']
        if resp['intents'][0]['confidence'] > 0.75:
            exp = ["", ""]
            for x in range(2):
                expresion = resp['entities']['Expression:Expression'][x]['body']
                expresion = expresion.replace("one", "1")
                expresion = expresion.replace("two", "2")
                expresion = expresion.replace("three", "3")
                expresion = expresion.replace("four", "4")
                expresion = expresion.replace("five", "5")
                expresion = expresion.replace("six", "6")
                expresion = expresion.replace("seven", "7")
                expresion = expresion.replace("eight", "8")
                expresion = expresion.replace("nine", "9")
                expresion = expresion.replace("zero", "0")
                expresion = expresion.replace("plus", "+")
                expresion = expresion.replace("minus", "-")
                expresion = expresion.replace("times", "*")
                expresion = expresion.replace("divided by", "/")
                exp[x] += expresion
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
                message  += "if " + exp[0] + "==" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " == " + exp[1] +
                #    " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
                message  += "if " + exp[0] + "!=" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " < " + exp[1] +
                #      " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
                message  += "if " + exp[0] + ">" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " == " + exp[1] +
                #      " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'less than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
                message  += "if " + exp[0] + "<" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " < " + exp[1] +
                #      " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
                message  += "if " + exp[0] + ">=" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " < " + exp[1] +
                #      " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
                message  += "if " + exp[0] + "<=" + exp[1] + " :\n\t"# + resp['entities']['command:command'][0]['body'] + "\nelse: \n\t" + resp['entities']['command:command'][1]['body']
                #print("if " + exp[0] + " < " + exp[1] +
                #      " :\n\t " + resp['entities']['command:command'][0]['body'] + "\nelse:\n\t" + resp['entities']['command:command'][1]['body'])

    if resp['intents'][0]['name'] == 'IfStatements':
        if resp['intents'][0]['confidence'] > 0.65:
            if 'command:command' in resp['entities']:
                exp = ["", ""]
                for x in range(2):
                    expresion = resp['entities']['Expression:Expression'][x]['body']
                    expresion = expresion.replace("one", "1")
                    expresion = expresion.replace("two", "2")
                    expresion = expresion.replace("three", "3")
                    expresion = expresion.replace("four", "4")
                    expresion = expresion.replace("five", "5")
                    expresion = expresion.replace("six", "6")
                    expresion = expresion.replace("seven", "7")
                    expresion = expresion.replace("eight", "8")
                    expresion = expresion.replace("nine", "9")
                    expresion = expresion.replace("zero", "0")
                    expresion = expresion.replace("plus", "+")
                    expresion = expresion.replace("minus", "-")
                    expresion = expresion.replace("times", "*")
                    expresion = expresion.replace("divided by", "/")
                    exp[x] += expresion
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
                    message += "if " + exp[0] + " == " + exp[1] + " :\n\t"
                    #print("if " + exp[0] + " == " + exp[1] +
                    #    " :\n\t")
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
                    message += "if " + exp[0] + " != " + exp[1] + " :\n\t "
                    #print("if " + exp[0] + " != " + exp[1] +
                    #    " :\n\t " + resp['entities']['command:command'][0]['body'])
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
                    message += "if " + exp[0] + " > " + exp[1] + " :\n\t "
                    #print("if " + exp[0] + " == " + exp[1] +
                    #    " :\n\t " + resp['entities']['command:command'][0]['body'])
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'less than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
                    message += "if " + exp[0] + " < " + exp[1] + " :\n\t "
                    #print("if " + exp[0] + " < " + exp[1] +
                    #    " :\n\t " + resp['entities']['command:command'][0]['body'])
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
                    message += "if " + exp[0] + " >= " + exp[1] + " :\n\t "
                    #print("if " + exp[0] + " < " + exp[1] +
                    #    " :\n\t " + resp['entities']['command:command'][0]['body'])
                if resp['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
                    message += "if " + exp[0] + " <= " + exp[1] + " :\n\t "
                    #print("if " + exp[0] + " < " + exp[1] +
                    #    " :\n\t " + resp['entities']['command:command'][0]['body'])
            else:
                message += "if (#) :\n\t#"

    if resp['intents'][0]['name'] == 'AddingComment':
        if resp['intents'][0]['confidence'] > 0.75:  # can change the value
            expresion = resp['entities']['Expression:Expression'][0]['body']
            expresion = expresion.replace("one", "1")
            expresion = expresion.replace("two", "2")
            expresion = expresion.replace("three", "3")
            expresion = expresion.replace("four", "4")
            expresion = expresion.replace("five", "5")
            expresion = expresion.replace("six", "6")
            expresion = expresion.replace("seven", "7")
            expresion = expresion.replace("eight", "8")
            expresion = expresion.replace("nine", "9")
            expresion = expresion.replace("zero", "0")
            expresion = expresion.replace("plus", "+")
            expresion = expresion.replace("minus", "-")
            expresion = expresion.replace("times", "*")
            expresion = expresion.replace("divided by", "/")
            message += '# ' + expresion
    if 'command:command' not in resp['entities'] and (if_else == 2 or if_else == 0) :
        print(message)
        break
    
    if if_else == 2 :
        message += "\nelse: \n\t"
        resp = client.message(command_else)
    if if_else == 1 :
        resp = client.message(command_if)
        if_else = 2
    if if_else == 0 :    
        resp = client.message(resp['entities']['command:command'][0]['body'])

#print(w2n.word_to_num("two million three thousand nine hundred and eighty four"))
# print("This is one line of code"
#      "this is the same line so they should not be separated"
#      "\n this one is a new line i want to see if its noticed")
#print("this is a new print command")
