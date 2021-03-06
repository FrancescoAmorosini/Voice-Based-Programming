import re
import sys
from wit import Wit
from word2number import w2n

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


def parse_assign_variable(response, nested_if):
    if 'VariableName:VariableName' in response['entities']:
        if 'Expression:Expression' in response['entities']:
            expression = parse(response['entities']['Expression:Expression'][0]['body'])
            if nested_if:
                return ("\t" + name_variable(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + expression)
            else:
                return (front_end_block + name_variable(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + expression)
        else:
            if nested_if:
                return "\t" + name_variable(response['entities']['VariableName:VariableName'][0]['body']) + ' = None\n'
            else:
                return front_end_block + name_variable(
                    response['entities']['VariableName:VariableName'][0]['body']) + ' = ' + placeholder_string
    else:
        return front_end_error + "Variable Name not found"


def parse_if_else_statement(response):
    expression = parse(response['entities']['Expression:Expression'][0]['body'])
    return "if " + expression + " :\n\t"


def parse_if_statement(response):
    if 'command:command' in response['entities']:
        expression = parse(response['entities']['Expression:Expression'][0]['body'])
        return "if " + expression + " :\n\t"
    else:
        return "if " + placeholder_string + " :\n\t" + placeholder_string


def parse_add_comment(response, nested_if):
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
            if nested_if == True:
                return final_output
            else:
                return front_end_block + final_output
        else:
            if response['entities']['CommentText:CommentText'][0]['body'][0] == "command":
                response['entities']['CommentText:CommentText'][0]['body'].replace("command ", "")
            if nested_if == True:
                return "# " + response['entities']['CommentText:CommentText'][0]['body']
            else:
                return front_end_block + "# " + response['entities']['CommentText:CommentText'][0]['body']
    except KeyError:
        if len(response['entities']['Expression:Expression'][0]['body']) > 120:
            if response['entities']['Expression:Expression'][0]['body'][0] == "command":
                response['entities']['Expression:Expression'][0]['body'].replace("command ", "")
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
            if nested_if == True:
                return final_output
            else:
                return front_end_block + final_output
        else:
            if response['entities']['Expression:Expression'][0]['body'][:7] == "command":
                return front_end_block + "# " + response['entities']['Expression:Expression'][0]['body'].replace(
                    "command ", "")
            if nested_if == True:
                return "# " + response['entities']['Expression:Expression'][0]['body']
            else:
                return front_end_block + "# " + response['entities']['Expression:Expression'][0]['body']


def parse_for_loop(response):
    if 'Expression:Expression' in response['entities']:
        message = ""
        try:
            first_expression = parse(response['entities']['Expression:Expression'][0]['body'])
        except KeyError:
            first_expression = placeholder_string
            message += front_end_warning + "Missing an expression in for loop command"
        try:
            second_expression = parse(response['entities']['Expression:Expression'][1]['body'])
        except IndexError:
            second_expression = placeholder_string
            message += front_end_warning + "Second Expression name was not understood in for loop"
        try:
            variable = name_variable(response['entities']['VariableName:VariableName'][0]['body'])
        except KeyError:
            variable = placeholder_string
            message += front_end_warning + "Variable Name not understood\n"
        message += front_end_block + "for " + variable + " in range ( " + first_expression + \
                  " , " + second_expression + " ):\n\t"
        message += placeholder_string
        return message
    elif 'VariableName:VariableName' in response['entities']:
        message = ""
        try:
            variable1 = name_variable(response['entities']['VariableName:VariableName'][0]['body'])
        except KeyError:
            variable1 = placeholder_string
            message += front_end_warning + "Variable Name not found in for loop"
        try:
            variable2 = name_variable(response['entities']['VariableName:VariableName'][1]['body'])
        except IndexError:
            variable2 = placeholder_string
            message += front_end_warning + "Second Variable name was not understood in for loop\n"
        message += front_end_block + "for " + variable1 + " in " + variable2 + ":\n\t"
        message += placeholder_string
        return message
    else:
        return front_end_block + "for " + placeholder_string + " in range( " + placeholder_string + \
               "," + placeholder_string + " ):\n\t" + placeholder_string


def parse_while_loop(response, nested_if):
    try:
        if 'Expression:Expression' in response['entities']:
            return front_end_block + "while " + parse(
                response['entities']['Expression:Expression'][0]['body']) + ":\n\t" + placeholder_string
        else:
            if nested_if == True:
                return "while " + placeholder_string + ":\n\t" + placeholder_string
            else:
                return front_end_block + "while " + placeholder_string + ":\n\t" + placeholder_string
    except IndexError:
        return front_end_warning + "Expression not found\n" \
               + front_end_block + "while " + placeholder_string + ":\n\t" + placeholder_string


def parse_create_function(response):
    if 'Parameter:Parameter' in response['entities']:
        try:
            functionName = name_variable(response['entities']['FunctionName:FunctionName'][0]['body'])
        except KeyError:
            return front_end_error + "FunctionName not found"
        message = "def " + functionName + " ("
        i = 0
        for x in response['entities']['Parameter:Parameter']:
            name_parameter = name_variable(response['entities']['Parameter:Parameter'][i]['body'])
            message += name_parameter + ", "
            i += 1
        message = message[:-2]
        message += "):\n\t" + placeholder_string
        return front_end_block + message
    else:
        try:
            functionName = name_variable(response['entities']['FunctionName:FunctionName'][0]['body'])
        except KeyError:
            return front_end_error + "FunctionName not found"
        message = "def " + functionName + " ():\n\t"
        return front_end_block + message


def parse_call_function(response, nested_if):
    if 'Parameter:Parameter' in response['entities']:
        try:
            functionName = name_variable(response['entities']['FunctionName:FunctionName'][0]['body'])
        except KeyError:
            return front_end_error + "FunctionName not found"

        message = functionName + " ("
        i = 0
        for x in response['entities']['Parameter:Parameter']:
            try:
                name_parameter = w2n.word_to_num(name_variable(response['entities']['Parameter:Parameter'][i]['body']))
            except ValueError:
                name_parameter = name_variable(response['entities']['Parameter:Parameter'][i]['body'])
            message += str(name_parameter) + ", "
            i += 1
        message = message[:-2]
        message += ")"
        if nested_if:
            return message
        else:
            return front_end_block + message
    else:
        try:
            functionName = name_variable(response['entities']['FunctionName:FunctionName'][0]['body'])
        except KeyError:
            return front_end_error + "FunctionName not found"
        message = functionName + " ()"
        if nested_if:
            return message
        else:
            return front_end_block + message


def parse_return(response):
    try:
        expression = parse(response['entities']['Expression:Expression'][0]['body'])
        return "return " + expression
    except KeyError:
        return "return"


def parse_delete(response):
    try:
        number1 = parse(response['entities']['Number:Number'][0]['body'])
    except KeyError:
        return "vocoder-line-delete\n"
    try:
        number2 = parse(response['entities']['Number:Number'][1]['body'])
        return "vocoder-line-delete\n" + number1 + "\n" + number2
    except IndexError:
        return front_end_error + "delete line numbers where not understood"


def parse_undo(response):
    try:
        number = parse(response['entities']['Number:Number'][0]['body'])
        return front_end_undo + number
    except KeyError:
        return front_end_undo


def parse_redo(response):
    try:
        number = parse(response['entities']['Number:Number'][0]['body'])
        return front_end_redo + number
    except KeyError:
        return front_end_redo


def parse_expression(string):
    string = string.replace("greater or equal to", " GreaterOrEqual")
    string = string.replace("less or equal to", " LessOrEqual")
    string = string.replace("is equal to", " IsEqualTo")
    string = string.replace("is equal", " IsEqualTo")
    string = string.replace("equal to", " IsEqualTo")
    string = string.replace("equals", " IsEqualTo")
    string = string.replace("is greater than", " GreaterThan")
    string = string.replace("greater than", " GreaterThan")
    string = string.replace("is less than", " LessThan")
    string = string.replace("less than", " LessThan")
    expression = ""
    expression_operators = ['plus',
                            'multiply', 'multiplied', 'multiplication', 'times', 'asterisk',
                            'modulo', 'mod',
                            'minus', 'unary',
                            'division', 'divide by', 'divided by',
                            'to the power of',
                            ]
    comparison_operators = ['GreaterOrEqual', 'LessOrEqual', 'IsEqualTo', 'GreaterThan', 'LessThan']
    logical_operators = ['and', 'or']
    op_out = []  # This holds the operators that are found in the string (left to right)
    # num_out = []  # this holds the non-operators that are found in the string (left to right)
    variableBuffer = []
    numberBuffer = []
    words = string.split(" ")
    variableFlag = False
    numberFlag = False
    logicalOperatorSpotted = False
    for word in words:  # examine 1 word at a time
        try:
            if word in logical_operators :
                logicalOperatorSpotted = word
                if variableBuffer:
                    VariableName = ""
                    counter = 1
                    for index in variableBuffer:
                        variableFlag = True
                        VariableName = VariableName + index
                        if naming_style == "snake" and counter != len(variableBuffer):
                            VariableName += "_"
                        counter += 1
                    if variableFlag:
                        expression += VariableName +" "
                    variableFlag = False
                    variableBuffer = []
                if numberFlag == False:
                    if variableFlag:
                        VariableName = ""
                        counter = 0
                        for index in variableBuffer:
                            variableFlag = True
                            VariableName += index
                            if naming_style == "snake" and counter == len(variableBuffer):
                                VariableName += "_"
                            counter += 1
                        expression += VariableName + " "
                        variableFlag = False
                        variableBuffer = []
                    expression += word + " "
                    logicalOperatorSpotted = False
            elif word in comparison_operators:
                if numberFlag:
                    numberFlag = False
                    numberString = ""
                    for index in numberBuffer:
                        numberString += index + " "
                    expression += str(w2n.word_to_num(numberString))+" "
                    numberBuffer = []

                if variableBuffer:
                    VariableName = ""
                    counter = 1
                    for index in variableBuffer:
                        variableFlag = True
                        VariableName = VariableName + index
                        if naming_style == "snake" and counter != len(variableBuffer):
                            VariableName += "_"
                        counter += 1
                    if variableFlag:
                        expression += VariableName +" "
                    variableFlag = False
                    variableBuffer = []

                if word == "GreaterThan":
                    expression += "> "
                elif word == "LessThan":
                    expression += "< "
                elif word == "IsEqualTo":
                    expression += "== "
                elif word == "GreaterOrEqual":
                    expression += ">= "
                elif word == "LessOrEqual":
                    expression += "<= "
                logicalOperatorSpotted=False

            elif word in expression_operators:  # found an operator.
                if numberFlag:
                    numberFlag = False
                    numberString = ""
                    for index in numberBuffer:
                        numberString += index + " "
                    expression += str(w2n.word_to_num(numberString))+" "
                    numberBuffer = []

                if variableBuffer:
                    VariableName = ""
                    counter = 1
                    for index in variableBuffer:
                        variableFlag = True
                        VariableName = VariableName + index
                        if naming_style == "snake" and counter != len(variableBuffer):
                            VariableName += "_"
                        counter += 1
                    if variableFlag:
                        expression += VariableName +" "
                    variableFlag = False
                    variableBuffer = []
                if word == "plus":
                    # op_out.append("+")
                    expression += "+ "
                if word == "minus" or word == "unary":
                    # op_out.append("-")
                    expression += "- "
                if word == "division" or word == "divided by" or word == "divide by":
                    # op_out.append("/")
                    expression += "/ "
                if word == "modulo" or word == "mod":
                    # op_out.append("%")
                    expression += "% "
                if word == "multiply" or word == "asterisk" or word == "multiplication" or word == "times":
                    # op_out.append("*")
                    expression += "* "
                logicalOperatorSpotted=False


            elif str(w2n.word_to_num(word)).isnumeric():
                numberFlag = True
                numberBuffer.append(word)

                # if it is a valid number.  Just accumulate this number.
        except ValueError:
            if numberFlag:
                numberFlag = False
                numberString = ""
                for index in numberBuffer:
                    numberString += index + " "
                expression += str(w2n.word_to_num(numberString))+" "
                numberBuffer = []
            if logicalOperatorSpotted:

                expression += logicalOperatorSpotted + " "
            logicalOperatorSpotted=False
            if word == "":
                continue
            # else this is a variable name so convert it
            if variableFlag and naming_style == "camel":
                variableBuffer.append(word.capitalize())
            else:
                variableBuffer.append(decapitalize_word(word))
                variableFlag = True
    if variableBuffer:
        VariableName = ""
        counter = 1
        for index in variableBuffer:
            variableFlag = True
            VariableName = VariableName + index
            if naming_style == "snake" and counter != len(variableBuffer):
                VariableName += "_"
            counter += 1
        if variableFlag:
            expression += VariableName
    if numberBuffer:
        numberString = ""
        for index in numberBuffer:
            numberString += index + " "
        expression += str(w2n.word_to_num(numberString))

    return expression

def parse(string):
    string = string.replace("greater or equal to", " GreaterOrEqual")
    string = string.replace("less or equal to", " LessOrEqual")
    string = string.replace("is equal to", " IsEqualTo")
    string = string.replace("is equal", " IsEqualTo")
    string = string.replace("equal to", " IsEqualTo")
    string = string.replace("equals", " IsEqualTo")
    string = string.replace("is greater than", " GreaterThan")
    string = string.replace("greater than", " GreaterThan")
    string = string.replace("is less than", " LessThan")
    string = string.replace("less than", " LessThan")
    return parse_expression(string)


def parse_response(file_name):
    with open(file_name, 'rb') as f:
        response = client.speech(f, {'Content-Type': 'audio/wav'})
    print(response)
    nested_if = False
    try:
        if response['intents'][0]['name'] == 'AssignVariable':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_assign_variable(response, nested_if)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_assign_variable(response, nested_if)

        elif response['intents'][0]['name'] == 'IfElseStatement':
            if response['intents'][0]['confidence'] > confidence_threshold:
                final_output = parse_if_else_statement(response)
                command_if = client.message(response['entities']['command:command'][0]['body'])
                nested_if = True
                if command_if['intents'][0]['name'] == 'AssignVariable':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_assign_variable(command_if, nested_if)
                if command_if['intents'][0]['name'] == 'AddingComment':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_add_comment(command_if, nested_if)
                if command_if['intents'][0]['name'] == 'Return':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_return(command_if)
                if command_if['intents'][0]['name'] == 'CallFunction':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_call_function(command_if, nested_if)
                final_output += "else:\n\t"
                command_else = client.message(response['entities']['command:command'][1]['body'])
                if command_else['intents'][0]['name'] == 'AssignVariable':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_assign_variable(command_else, nested_if)
                if command_else['intents'][0]['name'] == 'AddingComment':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_add_comment(command_else, nested_if)
                if command_else['intents'][0]['name'] == 'Return':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_return(command_else)
                if command_else['intents'][0]['name'] == 'CallFunction':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_call_function(command_else, nested_if)
                return front_end_block + final_output
                # missing nested ifs or nested if+ifElse
            else:
                print(front_end_warning + "The confidence is low")
                final_output = parse_if_else_statement(response)
                command_if = client.message(response['entities']['command:command'][0]['body'])
                nested_if = True
                if command_if['intents'][0]['name'] == 'AssignVariable':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_assign_variable(command_if, nested_if)
                if command_if['intents'][0]['name'] == 'AddingComment':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_add_comment(command_if, nested_if)
                if command_if['intents'][0]['name'] == 'Return':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_return(command_if)
                if command_if['intents'][0]['name'] == 'CallFunction':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_call_function(command_if, nested_if)
                final_output += "else:\n\t"
                command_else = client.message(response['entities']['command:command'][1]['body'])
                if command_else['intents'][0]['name'] == 'AssignVariable':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_assign_variable(command_else, nested_if)
                if command_else['intents'][0]['name'] == 'AddingComment':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_add_comment(command_else, nested_if)
                if command_else['intents'][0]['name'] == 'Return':
                    if command_if['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_return(command_else)
                if command_else['intents'][0]['name'] == 'CallFunction':
                    if command_else['intents'][0]['confidence'] > confidence_threshold:
                        final_output += parse_call_function(command_else, nested_if)
                return front_end_block + final_output
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
                                final_output += parse_assign_variable(command_if, nested_if)
                        if command_if['intents'][0]['name'] == 'AddingComment':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_add_comment(command_if, nested_if)
                        if command_if['intents'][0]['name'] == 'Return':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_return(command_if)
                        if command_if['intents'][0]['name'] == 'CallFunction':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_call_function(command_if, nested_if)
                    except IndexError:
                        final_output += placeholder_string
                        print(front_end_warning + "no inner command found")
                return front_end_block + final_output
                # missing nested ifs or nested if+ifElse
            else:
                print(front_end_warning + "The confidence is low")
                final_output = parse_if_statement(response)
                if 'command:command' in response['entities']:
                    command_if = client.message(response['entities']['command:command'][0]['body'])
                    nested_if = True
                    try:
                        if command_if['intents'][0]['name'] == 'DeclareVariable':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_assign_variable(command_if, nested_if)
                        if command_if['intents'][0]['name'] == 'AddingComment':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_add_comment(command_if, nested_if)
                        if command_if['intents'][0]['name'] == 'Return':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_return(command_if)
                        if command_if['intents'][0]['name'] == 'CallFunction':
                            if command_if['intents'][0]['confidence'] > confidence_threshold:
                                final_output += parse_call_function(command_if, nested_if)
                    except IndexError:
                        final_output += placeholder_string
                        print(front_end_warning + "no inner command found")
                return front_end_block + final_output
                # missing nested ifs or nested if+ifElse

        elif response['intents'][0]['name'] == 'AddingComment':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_add_comment(response, nested_if)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_add_comment(response, nested_if)

        elif response['intents'][0]['name'] == 'ForLoop':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_for_loop(response)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_for_loop(response)

        elif response['intents'][0]['name'] == 'WhileLoop':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_while_loop(response, nested_if)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_while_loop(response, nested_if)

        elif response['intents'][0]['name'] == 'UndoCommand':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_undo(response)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_undo(response)

        elif response['intents'][0]['name'] == 'CreateFunction':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_create_function(response)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_create_function(response)

        elif response['intents'][0]['name'] == 'Return':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return front_end_block + parse_return(response)
            else:
                print(front_end_warning + "The confidence is low")
                return front_end_block + parse_return(response)

        elif response['intents'][0]['name'] == 'Delete':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_delete(response)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_delete(response)

        elif response['intents'][0]['name'] == 'InsertExpression':
            if response['intents'][0]['confidence'] > confidence_threshold:
                try:
                    message_string = response['entities']['Expression:Expression'][0]['body']
                    return front_end_block + parse_expression(message_string)
                except KeyError:
                    print(front_end_error)
            else:
                print(front_end_warning + "The confidence is low")
                try:
                    message_string = response['entities']['Expression:Expression'][0]['body']
                    return front_end_block + parse_expression(message_string)
                except KeyError:
                    print(front_end_error)

        elif response['intents'][0]['name'] == 'CallFunction':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_call_function(response, nested_if)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_call_function(response, nested_if)

        elif response['intents'][0]['name'] == 'RedoCommand':
            if response['intents'][0]['confidence'] > confidence_threshold:
                return parse_redo(response)
            else:
                print(front_end_warning + "The confidence is low")
                return parse_redo(response)
        else:
            return front_end_error + "intent not in the list"
    except IndexError:
        return front_end_error + "intent not Detected"


naming_style = "snake"
if len(sys.argv) > 1 and sys.argv[1] == "-snake":
    naming_style = "snake"
elif len(sys.argv) > 1 and sys.argv[1] == "-camel":
    naming_style = "camel"
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
front_end_error = "dsd-section\nvocoder-error\n"
front_end_warning = "dsd-section\nvocoder-warning\n"
front_end_block = "dsd-section\nvocoder-code-block\n"
front_end_undo = "dsd-section\nvocoder-undo\n"
front_end_redo = "dsd-section\nvocoder-redo\n"
front_end_delete = "dsd-section\nvocoder-delete\n"

placeholder_string = "$$"
confidence_threshold = 0.75
#print(parse_response('vocoder\src\scripts\cmd\conda\output.wav'))
print(parse_response('output.wav'))
