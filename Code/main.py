import sys
from wit import Wit

from word2number import w2n

nested_if = False
nested_while = False


def decapitalize_word(s):
    if not s:  # check that s is not empty string
        return s
    return s[0].lower() + s[1:]


def string_to_camel(variable_name):
    count = 0
    combinedString = ""
    for word in variable_name.split(' '):
        if count == 0:
            combinedString += decapitalize_word(word)
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
        combinedString += decapitalize_word(word)
        if end_index != count:
            combinedString += "_"
    return combinedString


def name_variable(variable_name):
    if naming_style == "snake":
        return string_to_snake(variable_name)
    else:
        return string_to_camel(variable_name)


def parse_declare_variable(response):
    if 'VariableName:VariableName' in response['entities']:
        if 'Expression:Expression' in response['entities']:
            expression = parse(response['entities']['Expression:Expression'][0]['body'])
            if nested_if:
                return ("\t" + name_variable(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + expression)
            else:
                return (name_variable(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + expression)
        else:
            if nested_if:
                return "\t" + name_variable(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n'
            else:
                return name_variable(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n'


def parse_if_else_statement(response):
    first_expression = parse(response['entities']['Expression:Expression'][0]['body'])
    second_expression = parse(response['entities']['Expression:Expression'][1]['body'])
    if response['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
        print("if " + first_expression + "==" + second_expression + " :")
    if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
        print("if " + first_expression + "!=" + second_expression + " :")
    if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
        print("if " + first_expression + ">" + second_expression + " :")
    if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
        print("if " + first_expression + "<" + second_expression + " :")
    if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
        print("if " + first_expression + ">=" + second_expression + " :")
    if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
        print("if " + first_expression + "<=" + second_expression + " :")


def parse_if_statement(response):
    if 'command:command' in response['entities']:
        first_expression = parse(response['entities']['Expression:Expression'][0]['body'])
        second_expression = parse(response['entities']['Expression:Expression'][1]['body'])
        if response['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
            return "if " + first_expression + "==" + second_expression + " :"

        if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
            return "if " + first_expression + "!=" + second_expression + " :"

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
            return "if " + first_expression + ">" + second_expression + " :"

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
            return "if " + first_expression + "<" + second_expression + " :"

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
            return "if " + first_expression + ">=" + second_expression + " :"

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
            return "if " + first_expression + "<=" + second_expression + " :\n\t "
    else:
        return "if "+placeholder_string+" :\n\t"+placeholder_string


def parse_add_comment(response):
    try:
        if len(response['entities']['CommentText:CommentText'][0]['body']) > 120:
            final_output = ""
            words = response['entities']['CommentText:CommentText'][0]['body'].split(" ")
            out = "#"
            for i in range(0, int(len(words) / 2)):
                out += " " + words[i]
            final_output += out
            out = "#"
            for i in range(int(len(words) / 2), len(words)):
                out += " " + words[i]
            final_output += out
            return final_output
        else:
            return ("# " + response['entities']['CommentText:CommentText'][0]['body'])
    except KeyError:
        if len(response['entities']['Expression:Expression'][0]['body']) > 120:
            final_output = ""
            words = response['entities']['Expression:Expression'][0]['body'].split(" ")
            out = "#"
            for i in range(0, int(len(words) / 2)):
                out += " " + words[i]
            final_output += out
            out = "#"
            for i in range(int(len(words) / 2), len(words)):
                out += " " + words[i]
            final_output += out
            return final_output
        else:
            return ("# " + response['entities']['Expression:Expression'][0]['body'])


def parse_for_loop(response):
    if 'Expression:Expression' in response['entities']:
        try:
            first_expression = parse(response['entities']['Expression:Expression'][0]['body'])
            second_expression = parse(response['entities']['Expression:Expression'][1]['body'])
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
        message = "for " + variable + " in range ( " + first_expression + " , " + second_expression + "):\n\t"
        message += placeholder_string
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
        message += placeholder_string
        return (message)
    else:
        return ("for "+placeholder_string+" in range( "+placeholder_string+","+placeholder_string+" ):\n\t")


def parse_while_loop(response):
    if 'comparisons:comparisons' in response['entities']:
        expression1 = parse(response['entities']['Expression:Expression'][0]['body'])
        expression2 = parse(response['entities']['Expression:Expression'][1]['body'])
        if response['entities']['comparisons:comparisons'][0]['body'] == 'equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is equal to':
            return "while " + expression1 + " ==  " + expression2 + " :\n\t#"+placeholder_string

        if response['entities']['comparisons:comparisons'][0]['body'] == 'non equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is non equal to':
            return "while " + expression1 + "!=" + expression2 + " :\n\t"+placeholder_string

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater than':
            return "while " + expression1 + ">" + expression2 + " :\n\t"+placeholder_string

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less than' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less than':
            return "while " + expression1 + "<" + expression2 + " :\n\t"+placeholder_string

        if response['entities']['comparisons:comparisons'][0]['body'] == 'greater or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is greater or equal to':
            return "while " + expression1 + ">=" + expression2 + " :\n\t"+placeholder_string

        if response['entities']['comparisons:comparisons'][0]['body'] == 'less or equal to' or \
                response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
            return "while " + expression1 + "<=" + expression2 + " :\n\t"+placeholder_string
    elif 'Expression:Expression' in response['entities']:
        expression = parse(response['entities']['Expression:Expression'][0]['body'])
        return "while" + expression + ":\n\t" + placeholder_string
    else:
        return "while " + placeholder_string + " com exp :\n\t" + placeholder_string


# takes a string and converts it to operations and variables
def parse(string):
    expression_operators = ['plus',
                            'multiply', 'multiplied', 'multiplication', 'times', 'asterisk',
                            'modulo', 'mod',
                            'minus', 'unary'
                                     'division', 'divide by', 'divided by',
                            'to the power of',
                            'and',
                            'or',
                            ]
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
                if word == "minus" or word == "unary":
                    op_out.append("-")
                if word == "division":
                    op_out.append("÷")
                if word == "modulo" or word == "mod":
                    op_out.append("%")
                if word == "multiply" or word == "asterisk" or word == "multiplication" or word == "times":
                    op_out.append("*")
                if word == "and":
                    op_out.append("and")
                if word == "or":
                    op_out.append("or")
            elif str(w2n.word_to_num(word)).isnumeric():
                # if it is a valid number.  Just accumulate this number in num_out.
                digit = w2n.word_to_num(word)
                num_out.append(digit)
        except ValueError:
            # else this is a variable name so convert it
            if variableDetectionFlag:
                buffer.append(word.capitalize())
            else:
                buffer.append(decapitalize_word(word))
                variableDetectionFlag = True
    if buffer:
        VariableName = ""
        for index in buffer:
            variableDetectionFlag = True
            VariableName = VariableName + index
        if variableDetectionFlag:
            num_out.append(VariableName)
    counter = -1
    expression = ""
    for variable in num_out:
        if counter >= 0:
            expression += " " + op_out[counter] + " "
        expression += str(variable)
        counter += 1
    return expression


def parse_response(file_name):
    with open('CommentHelloWorld.wav', 'rb') as f:
        response = client.speech(f, {'Content-Type': 'audio/wav'})
    if file_name['intents'][0]['name'] == 'DeclareVariable':
        if response['intents'][0]['confidence'] > confidence_threshold:
            print(front_end_block)
            return parse_declare_variable(response)

    elif response['intents'][0]['name'] == 'IfElseStatement':
        if response['intents'][0]['confidence'] > confidence_threshold:
            print(front_end_block)
            parse_if_else_statement(response)
            command_if = client.message(response['entities']['command:command'][0]['body'])
            nested_if = True
            if command_if['intents'][0]['name'] == 'DeclareVariable':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_declare_variable(command_if)
            if command_if['intents'][0]['name'] == 'AddingComment':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_add_comment(command_if)
            print("else:")
            resp3 = client.message(response['entities']['command:command'][1]['body'])
            if resp3['intents'][0]['name'] == 'DeclareVariable':
                if resp3['intents'][0]['confidence'] > confidence_threshold:
                    parse_declare_variable(resp3)
            if resp3['intents'][0]['name'] == 'AddingComment':
                if resp3['intents'][0]['confidence'] > confidence_threshold:
                    parse_add_comment(resp3)
            # missing nested ifs or nested if+ifElse

    elif response['intents'][0]['name'] == 'IfStatements':
        if response['intents'][0]['confidence'] > confidence_threshold:
            final_output = parse_if_statement(response)
            if 'command:command' in response['entities']:
                command_if = client.message(response['entities']['command:command'][0]['body'])
                nested_if = True
                try:
                    if command_if['intents'][0]['name'] == 'DeclareVariable':
                        if command_if['intents'][0]['confidence'] > confidence_threshold:
                            final_output += parse_declare_variable(command_if)
                    if command_if['intents'][0]['name'] == 'AddingComment':
                        if command_if['intents'][0]['confidence'] > confidence_threshold:
                            final_output += parse_add_comment(command_if)
                except IndexError:
                    final_output += "\n\t" + placeholder_string
                    print("no inner command found")
            return front_end_block + final_output
            # missing nested ifs or nested if+ifElse

    elif response['intents'][0]['name'] == 'AddingComment':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_add_comment(response)

    elif response['intents'][0]['name'] == 'ForLoop':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_for_loop(response)

    elif response['intents'][0]['name'] == 'WhileLoop':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_while_loop(response)

    elif response['intents'][0]['name'] == 'UndoCommand':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return "dsd-section\nvocoder-undo\n"
    else:
        return "dsd-section\nintent not found"


naming_style = "snake"
if len(sys.argv) > 1 and sys.argv[1] == "-snake":
    naming_style = "snake"
elif len(sys.argv) > 1 and sys.argv[1] == "-camel":
    naming_style = "camel"
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
front_end_error = "dsd-section\nvocoder-error-message\n"
front_end_block = "dsd-section\nvocoder-code-block\n"
placeholder_string = "#placeholder"
confidence_threshold = 0.75
print(parse_response('CommentHelloWorld.wav'))

# def test_answer():
#     with open('IfCount5.wav', 'rb') as f:
#         resp = client.speech(f, {'Content-Type': 'audio/wav'})
#     resp['intents'][0]['name'] = "AddingComment"
#     resp['intents'][0]['confidence'] = 0.8
#     resp['entities']['CommentText:CommentText'][0]['body'] = "hello world"
#     assert parse_response(resp) == front_end_block + "\n#hello world"
