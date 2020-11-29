import sys

from wit import Wit

from word2number import w2n

nested_if = False


def decapitalize(s):
    if not s:  # check that s is not empty string
        return s
    return s[0].lower() + s[1:]


def snake_to_camel(variablename):
    count = 0
    combinedString = ""
    for word in variablename.split(' '):
        if count == 0:
            combinedString += decapitalize(word)
        else:
            combinedString += word.capitalize()
        count += 1
    return combinedString


def parse_declare_variable(response):
    if 'VariableName:VariableName' in response['entities']:
        if 'Expression:Expression' in response['entities']:
            variables, operators = parse(response['entities']['Expression:Expression'][0]['body'])
            output_string = ""
            counter = -1
            for variable in variables:
                if counter >= 0:
                    output_string += " " + operators[counter] + " "
                output_string += str(variable)
                counter += 1
            if nested_if == True:
                print("\t" + snake_to_camel(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + output_string)
            else:
                print(snake_to_camel(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + output_string)
        else:
            if nested_if == True:
                print("\t" + snake_to_camel(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n')
            else:
                print(snake_to_camel(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n')


def parse_if_else_statement(response):
    variables, operators = parse(response['entities']['Expression:Expression'][0]['body'])
    output_string = ""
    counter = -1
    for variable in variables:
        if counter >= 0:
            output_string += " " + operators[counter] + " "
        output_string += str(variable)
        counter += 1
    variables2, operators2 = parse(response['entities']['Expression:Expression'][1]['body'])
    output_string2 = ""
    counter = -1
    for variable2 in variables2:
        if counter >= 0:
            output_string2 += " " + operators2[counter] + " "
        output_string2 += str(variable2)
        counter += 1
    if response['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
        print("if " + output_string + "==" + output_string2 + " :")

    if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
        print("if " + output_string + "!=" + output_string2 + " :")

    if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
        print("if " + output_string + ">" + output_string2 + " :")

    if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
        print("if " + output_string + "<" + output_string2 + " :")

    if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
        print("if " + output_string + ">=" + output_string2 + " :")

    if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
        print("if " + output_string + "<=" + output_string2 + " :")


def parse_if_statement(response):
    if 'command:command' in response['entities']:
        variables, operators = parse(response['entities']['Expression:Expression'][0]['body'])
        output_string = ""
        counter = -1
        for variable in variables:
            if counter >= 0:
                output_string += " " + operators[counter] + " "
            output_string += str(variable)
            counter += 1
        variables2, operators2 = parse(response['entities']['Expression:Expression'][1]['body'])
        output_string2 = ""
        counter = -1
        for variable2 in variables2:
            if counter >= 0:
                output_string2 += " " + operators2[counter] + " "
            output_string2 += str(variable2)
            counter += 1
        if response['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
            print("if " + output_string + "==" + output_string2 + " :")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
            print("if " + output_string + "!=" + output_string2 + " :")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
            print("if " + output_string + ">" + output_string2 + " :")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
            print("if " + output_string + "<" + output_string2 + " :")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
            print("if " + output_string + ">=" + output_string2 + " :")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
            print("if " + output_string + "<=" + output_string2 + " :\n\t ")
    else:
        print("if #Condition :\n\t#Command")


def parse_add_comment(response):
    if len(response['entities']['CommentText:CommentText'][0]['body']) > 120:
        words = response['entities']['CommentText:CommentText'][0]['body'].split(" ")
        out = "#"
        for i in range(0, int(len(words) / 2)):
            out += " " + words[i]
        print(out)
        out = "#"
        for i in range(int(len(words) / 2), len(words)):
            out += " " + words[i]
        print(out)
    else:
        print("# " + response['entities']['CommentText:CommentText'][0]['body'])


# takes a string and converts it to operations and variables
def parse(string):
    expression_operators = ['plus', 'minus', 'times', 'asterisk', 'multiplication', 'division', 'modulo', 'mod',
                            'multiply',
                            'multiplied']
    op_out = []  # This holds the operators that are found in the string (left to right)
    num_out = []  # this holds the non-operators that are found in the string (left to right)
    buffer = []
    words = string.split(" ")
    variableDetectionFlag = False
    for word in words:  # examine 1 word at a time
        try:
            if word in expression_operators:
                VariableName = ""
                for index in buffer:
                    variableDetectionFlag = True
                    VariableName = VariableName + index
                if variableDetectionFlag:
                    num_out.append(VariableName)
                    variableDetectionFlag = False
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
            if variableDetectionFlag:
                buffer.append(word.capitalize())
            else:
                buffer.append(decapitalize(word))
                variableDetectionFlag = True
    if buffer:
        VariableName = ""
        for index in buffer:
            variableDetectionFlag = True
            VariableName = VariableName + index
        if variableDetectionFlag:
            num_out.append(VariableName)

    return num_out, op_out


# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
with open('declare expression.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Wit.ai response: ' + str(resp) + '\n')

if resp['intents'][0]['name'] == 'DeclareVariable':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_declare_variable(resp)

if resp['intents'][0]['name'] == 'IfElseStatement':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_if_else_statement(resp)
        command_if = client.message(resp['entities']['command:command'][0]['body'])
        nested_if = True
        if command_if['intents'][0]['name'] == 'DeclareVariable':
            if command_if['intents'][0]['confidence'] > 0.75:
                parse_declare_variable(command_if)
        if command_if['intents'][0]['name'] == 'AddingComment':
            if command_if['intents'][0]['confidence'] > 0.75:
                parse_add_comment(command_if)
        print("else:")
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
            command_if = client.message(resp['entities']['command:command'][0]['body'])
            nested_if = True
            if command_if['intents'][0]['name'] == 'DeclareVariable':
                if command_if['intents'][0]['confidence'] > 0.75:
                    parse_declare_variable(command_if)
            if command_if['intents'][0]['name'] == 'AddingComment':
                if command_if['intents'][0]['confidence'] > 0.75:
                    parse_add_comment(command_if)
            # missing nested ifs or nested if+ifElse

if resp['intents'][0]['name'] == 'AddingComment':
    if resp['intents'][0]['confidence'] > 0.75:
        print("dsd-section\nvocoder-code-block\n")
        parse_add_comment(resp)
