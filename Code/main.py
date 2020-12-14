import sys

from wit import Wit

from word2number import w2n

nested_if = False
nested_while = False


def decapitalize(s):
    if not s:  # check that s is not empty string
        return s
    return s[0].lower() + s[1:]


def string_to_camel(variable_name):
    count = 0
    combinedString = ""
    for word in variable_name.split(' '):
        if count == 0:
            combinedString += decapitalize(word)
        else:
            combinedString += word.capitalize()
        count += 1
    return combinedString


def snake_to_camel(snake_variable):
    return ''.join(x.capitalize() or '_' for x in snake_variable.split('_'))


def string_to_snake(variable_name):
    count = 0
    combinedString = ""
    end_index = len(variable_name.split(' '))
    for word in variable_name.split(' '):
        count += 1
        combinedString += decapitalize(word)
        if end_index != count:
            combinedString += "_"
    return combinedString


def name_variable(variable_name):
    if naming_style == "snake":
        return string_to_snake(variable_name)
    else:
        return string_to_snake(variable_name)


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
            if nested_if:
                print("\t" + string_to_camel(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + output_string)
            else:
                print(string_to_camel(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + output_string)
        else:
            if nested_if:
                print(
                    "\t" + string_to_camel(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n')
            else:
                print(string_to_camel(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n')


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


def parse_for_loop(response):
    if 'Expression:Expression' in response['entities']:
        try:
            variables1, operators1 = parse(response['entities']['Expression:Expression'][0]['body'])
            variables2, operators2 = parse(response['entities']['Expression:Expression'][1]['body'])
        except KeyError:
            print(front_end_error)
            print("Missing an expression in for loop command")
            return
        except IndexError:
            print(front_end_error)
            print("Second Expression name was not understood in for loop")
            return
        try:
            variable = response['entities']['VariableName:VariableName'][0]['body']
        except KeyError:
            print(front_end_error)
            print("Variable Name not understood")
            return
        first_expression = ""
        second_expression = ""
        counter = -1
        for variable1 in variables1:
            if counter >= 0:
                first_expression += " " + operators1[counter] + " "
            first_expression += str(variable1)
            counter += 1
        counter = -1
        for variable2 in variables2:
            if counter >= 0:
                second_expression += " " + operators2[counter] + " "
            second_expression += str(variable2)
            counter += 1
        message = "for " + variable + " in ranage ( " + first_expression + " , " + second_expression + "):\n\t"
        message += "#command"
        print(message)
    elif 'VariableName:VariableName' in response['entities']:
        try:
            variable1 = response['entities']['VariableName:VariableName'][0]['body']
            variable2 = response['entities']['VariableName:VariableName'][1]['body']
        except KeyError:
            print(front_end_error)
            print("Variable Name not found in for loop")
            return
        except IndexError:
            print(front_end_error)
            print("Second Variable name was not understood in for loop")
            return
        message = "for " + variable1 + " in " + variable2 + ":\n\t"
        message += "#command"
        print(message)
    else:
        print("for #variable in range( #expression,#expression ):\n\t")


def parse_while_loop(response):
    if 'comparisons:comparisons' in response['entities']:
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
            print("while " + output_string + " ==  " + output_string2 + " :\n\t#command")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
            print("while " + output_string + "!=" + output_string2 + " :\n\t#command")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
            print("while " + output_string + ">" + output_string2 + " :\n\tcommand")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
            print("while " + output_string + "<" + output_string2 + " :\n\t#command")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
            print("while " + output_string + ">=" + output_string2 + " :\n\t#command")

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
            print("while " + output_string + "<=" + output_string2 + " :\n\t#command ")
    elif 'Expression:Expression' in response['entities']:
        variables, operators = parse(response['entities']['Expression:Expression'][0]['body'])
        output_string = ""
        counter = -1
        for variable in variables:
            if counter >= 0:
                output_string += " " + operators[counter] + " "
            output_string += str(variable)
            counter += 1
        print("while" + output_string + ":\n\t#command")
    else:
        print("while #exp com exp :\n\t#command")


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


naming_style = "snake"
if len(sys.argv) > 0 and sys.argv[0] == "-snake":
    naming_style = "snake"
elif len(sys.argv) > 0 and sys.argv[0] == "-camel":
    naming_style = "camel"

client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
with open('..\\..\\..\\..\\..\\Code\\WhileLoop.wav', 'rb') as f:
    resp = client.speech(f, {'Content-Type': 'audio/wav'})
print(resp)

front_end_error = "dsd-section\nvocoder-error-message"
front_end_block = "dsd-section\nvocoder-code-block"
confidence_threshold = 0.75

if resp['intents'][0]['name'] == 'DeclareVariable':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_declare_variable(resp)

if resp['intents'][0]['name'] == 'IfElseStatement':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_if_else_statement(resp)
        command_if = client.message(resp['entities']['command:command'][0]['body'])
        nested_if = True
        if command_if['intents'][0]['name'] == 'DeclareVariable':
            if command_if['intents'][0]['confidence'] > confidence_threshold:
                parse_declare_variable(command_if)
        if command_if['intents'][0]['name'] == 'AddingComment':
            if command_if['intents'][0]['confidence'] > confidence_threshold:
                parse_add_comment(command_if)
        print("else:")
        resp3 = client.message(resp['entities']['command:command'][1]['body'])
        if resp3['intents'][0]['name'] == 'DeclareVariable':
            if resp3['intents'][0]['confidence'] > confidence_threshold:
                parse_declare_variable(resp3)
        if resp3['intents'][0]['name'] == 'AddingComment':
            if resp3['intents'][0]['confidence'] > confidence_threshold:
                parse_add_comment(resp3)
        # missing nested ifs or nested if+ifElse

elif resp['intents'][0]['name'] == 'IfStatements':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_if_statement(resp)
        if 'command:command' in resp['entities']:
            command_if = client.message(resp['entities']['command:command'][0]['body'])
            nested_if = True
            if command_if['intents'][0]['name'] == 'DeclareVariable':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_declare_variable(command_if)
            if command_if['intents'][0]['name'] == 'AddingComment':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_add_comment(command_if)
            # missing nested ifs or nested if+ifElse

elif resp['intents'][0]['name'] == 'AddingComment':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_add_comment(resp)

elif resp['intents'][0]['name'] == 'ForLoop':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_for_loop(resp)

elif resp['intents'][0]['name'] == 'WhileLoop':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print(front_end_block)
        parse_while_loop(resp)

elif resp['intents'][0]['name'] == 'UndoCommand':
    if resp['intents'][0]['confidence'] > confidence_threshold:
        print("dsd-section\nundo\n")
else:
    print("dsd-section\nintent not found")
