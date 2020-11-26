from wit import Wit
import sys
# from word2number import w2n

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
with open('IfCount5.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp) + '\n')

if resp['intents'][0]['name'] == 'DeclareVariable':
    print("This Message is an DeclareVariable")

if resp['intents'][0]['name'] == 'IfElseStatement':
    print("This Message is an IfElseStatement")

if resp['intents'][0]['name'] == 'IfStatements':
    if resp['intents'][0]['confidence'] > 0.75:
        if 'command:command' in resp['entities']:
            exp = ["", ""]
            for x in range(2) :
                expresion = resp['entities']['Expression:Expression'][x]['body']
                expresion = expresion.replace("one","1")
                expresion = expresion.replace("two","2")
                expresion = expresion.replace("three","3")
                expresion = expresion.replace("four","4")
                expresion = expresion.replace("five","5")
                expresion = expresion.replace("six","6")
                expresion = expresion.replace("seven","7")
                expresion = expresion.replace("eight","8")
                expresion = expresion.replace("nine","9")
                expresion = expresion.replace("cero","0")
                expresion = expresion.replace("plus","+")
                expresion = expresion.replace("minus","-")
                expresion = expresion.replace("times","*")
                expresion = expresion.replace("divided by","/")
                exp[x] += expresion
                print(exp[x])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
                print("if " + exp[0] + " == " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
                print("if " + exp[0] + " < " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
                print("if " + exp[0] + " == " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'less than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
                print("if " + exp[0] + " < " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
                print("if " + exp[0] + " < " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
            if resp['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
                print("if " + exp[0] + " < " + exp[1] +
                      " :\n\t " + resp['entities']['command:command'][0]['body'])
        else:
            print("if (#) :\n\t#")

if resp['intents'][0]['name'] == 'AddingComment':
    if resp['intents'][0]['confidence'] > 0.75:  # can change the value
        print('# ' + resp['entities']['Expression:Expression'][0]['body'])

#print(w2n.word_to_num("two million three thousand nine hundred and eighty four"))
# print("This is one line of code"
#      "this is the same line so they should not be separated"
#      "\n this one is a new line i want to see if its noticed")
#print("this is a new print command")
