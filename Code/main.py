import sys

from wit import Wit

from word2number import w2n


def snake_to_camel(variablename):
    return ''.join(
        word.capitalize() or '_' for word in variablename.split(' '))



def parse_declare_variable(response):
    if 'VariableName:VariableName' in response['entities']:
        if 'Expression:Expression' in response['entities']:
            variables, operators = parse(resp['entities']['Expression:Expression'][0]['body'])
            output_string = ""
            counter = -1
            for variable in variables:
                if counter >= 0:
                    output_string += " " + operators[counter] + " "
                output_string += str(variable)
                counter += 1
            print(snake_to_camel(resp['entities']['VariableName:VariableName'][0]['body']) + ' = ' + output_string)
        else:
            print("dsd-section\nvocoder-code-block\n" + snake_to_camel(
                resp['entities']['VariableName:VariableName'][0]['body']) + ' = None\n')
def parse_if_else_statement(response):
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
        print("if " + exp[0] + "==" + exp[1] + " :\n\t")

    if resp['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
        print("if " + exp[0] + "!=" + exp[1] + " :\n\t")

    if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
        print("if " + exp[0] + ">" + exp[1] + " :\n\t")

    if resp['entities']['comparisons:comparisons'][0]['body'] == 'less than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
        print("if " + exp[0] + "<" + exp[1] + " :\n\t")

    if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
        print("if " + exp[0] + ">=" + exp[1] + " :\n\t")

    if resp['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
        print("if " + exp[0] + "<=" + exp[1] + " :\n\t")

def parse_if_statement(response):
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
            print("if " + exp[0] + " == " + exp[1] + " :\n\t")

        if resp['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
            print("if " + exp[0] + " != " + exp[1] + " :\n\t ")

        if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
            print("if " + exp[0] + " > " + exp[1] + " :\n\t ")

        if resp['entities']['comparisons:comparisons'][0]['body'] == 'less than' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
            print("if " + exp[0] + " < " + exp[1] + " :\n\t ")

        if resp['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
            print("if " + exp[0] + " >= " + exp[1] + " :\n\t ")

        if resp['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or resp['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
            print("if " + exp[0] + " <= " + exp[1] + " :\n\t ")
    else:
        print("if (#) :\n\t#")

def parse_add_comment(response):
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
        print("#"  + expresion)

# takes a string and converts it to operations and variables
def parse(string):
    expression_operators = ['plus', 'minus', 'times', 'asterisk', 'multiplication', 'division', 'modulo', 'mod',
                            'multiply',
                            'multiplied']
    op_out = []  # This holds the operators that are found in the string (left to right)
    num_out = []  # this holds the non-operators that are found in the string (left to right)
    buffer = []
    words = string.split(" ")
    for word in words:  # examine 1 word at a time
        try:
            if word in expression_operators:
                VariableName = ""
                flag = False
                for index in buffer:
                    flag = True
                    VariableName = VariableName + index
                if flag:
                    num_out.append(VariableName)
                    flag = False
                buffer = []
                # found an operator.
                if word == "plus":
                    op_out.append("+")
                if word == "minus":
                    op_out.append("-")
                if word == "division":
                    op_out.append("÷")
                if word == "modulo":
                    op_out.append("%")
                if word == "mod":
                    op_out.append("%")
                if word == "multiply":
                    op_out.append("*")
                if word == "multiply":
                    op_out.append("*")
                if word == "asterisk":
                    op_out.append("*")
                if word == "multiplication":
                    op_out.append("*")
                if word == "times":
                    op_out.append("*")
            elif str(w2n.word_to_num(word)).isnumeric():
                # if it is a valid number.  Just accumulate this number in num_out.
                digit = w2n.word_to_num(word)
                num_out.append(digit)
        except ValueError:
            # else this is a variable name so convert it
            buffer.append(snake_to_camel(word))
    if buffer:
        VariableName = ""
        flag = False
        for index in buffer:
            flag = True
            VariableName = VariableName + index
        if flag:
            num_out.append(VariableName)

    return num_out, op_out


# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
with open('CreateAnIfStatement.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Wit.ai response: ' + str(resp) + '\n')
message = ""
if_else = 0

if resp['intents'][0]['name'] == 'DeclareVariable':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_declare_variable(resp)

if resp['intents'][0]['name'] == 'IfElseStatement':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_if_else_statement(resp)
        resp2 = client.message(resp['entities']['command:command'][0]['body'])
        if resp2['intents'][0]['name'] == 'DeclareVariable':
            if resp2['intents'][0]['confidence'] > 0.75:
                parse_declare_variable(resp2)
        if resp2['intents'][0]['name'] == 'AddingComment':
            if resp2['intents'][0]['confidence'] > 0.75:
                parse_add_comment(resp2)
        print("\nelse: \n\t")
        resp3 = client.message(resp['entities']['command:command'][1]['body'])
        if resp3['intents'][0]['name'] == 'DeclareVariable':
            if resp3['intents'][0]['confidence'] > 0.75:
                parse_declare_variable(resp3)
        if resp3['intents'][0]['name'] == 'AddingComment':
            if resp3['intents'][0]['confidence'] > 0.75:
                parse_add_comment(resp3)
        # missing nested ifs or nested if+ifElse

if resp['intents'][0]['name'] == 'IfStatements':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_if_statement(resp)
        if 'command:command' in resp['entities']:
            resp2 = client.message(resp['entities']['command:command'][0]['body'])
            if resp2['intents'][0]['name'] == 'DeclareVariable':
                if resp2['intents'][0]['confidence'] > 0.75:
                    parse_declare_variable(resp2)
            if resp2['intents'][0]['name'] == 'AddingComment':
                if resp2['intents'][0]['confidence'] > 0.75:
                    parse_add_comment(resp2)
            # missing nested ifs or nested if+ifElse

if resp['intents'][0]['name'] == 'AddingComment':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_add_comment(resp)