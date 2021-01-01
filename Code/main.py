import re
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


def parse_assign_variable(response):
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
                return name_variable(response['entities']['VariableName:VariableName'][0]['body']) + ' = None'
    else:
        print(front_end_error)
        print("Variable Name not found")


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
    if response['entities']['Expression:Expression'][0]['body'] == 'less or equal to' or \
            response['entities']['comparisons:comparisons'][0]['body'] == 'is less or equal to':
        print("if " + + " :")


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
        return "if " + placeholder_string + " :\n\t" + placeholder_string


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
            return "# " + response['entities']['CommentText:CommentText'][0]['body']
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
            return "# " + response['entities']['Expression:Expression'][0]['body']


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
        return (message)
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
        return message
    else:
        return "for " + placeholder_string + " in range( " + placeholder_string + "," + placeholder_string + " ):\n\t"


def parse_while_loop(response):
    if 'Expression:Expression' in response['entities']:
        return "while " + parse(response['entities']['Expression:Expression'][0]['body']) + ":\n\t" + placeholder_string
    else:
        return "while " + placeholder_string + ":\n\t" + placeholder_string


def parse_create_function(response):
    if 'Parameter:Parameter' in response['entities']:
        try:
            functionName = response['entities']['FunctionName:FunctionName'][0]['body']
        except KeyError:
            print(front_end_error)
            print("FunctionName not found")
            return
        message = "def" + functionName + " ("
        for parameter in response['entities']:
            message += parameter['body'] + ", "
        message[:-2]
        message += ") :"
        return (message)
    else:
        try:
            functionName = response['entities']['FunctionName:FunctionName'][0]['body']
        except KeyError:
            print(front_end_error)
            print("FunctionName not found")
            return
        message = "def" + functionName + "() :"
        return (message)


def parse_return(response):
    try:
        expression = parse(response['entities']['Expression:Expression'][0]['body'])
        return "return " + expression
    except KeyError:
        print(front_end_error)
        print("Expression not found")
        return


def parse_expression(string):
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


def parse(string):
    final_output = ""
    string = string.replace("greater or equal to", "GreaterOrEqual")
    string = string.replace("less or equal to", "LessOrEqual")
    logical_expressions = re.findall('and|or', string)
    if len(logical_expressions) == 0:
        logical_expressions.append(None)
    for comparison_operator in logical_expressions:
        comparison_operators = []
        if comparison_operator is not None:
            comparison_operators = string.split(comparison_operator)
        else:
            comparison_operators.append(string)
        counter_comparison = 0
        for logical_expression in comparison_operators:
            counter_comparison += 1
            logical_operators = re.findall(
                'GreaterOrEqual|LessOrEqual|equal to|equals|is greater than|is less than|greater than|less than',
                logical_expression)
            if len(logical_operators) == 0:
                logical_operators.append(string)
            for logical_operator in logical_operators:
                arithmetic_value = logical_expression.split(logical_operator)
                counter_arithemtic_value = 0
                for arithmetic_operation in arithmetic_value:  # examine 1 expression at a time
                    counter_arithemtic_value += 1
                    if arithmetic_operation[-1] == ' ':
                        arithmetic_operation = arithmetic_operation[:len(arithmetic_operation) - 1]
                    if arithmetic_operation[0] == ' ':
                        arithmetic_operation = arithmetic_operation[1:]
                    final_output += parse_expression(arithmetic_operation)
                    if counter_arithemtic_value != len(arithmetic_value):
                        if logical_operator == "greater than" or logical_operator == "is greater than":
                            final_output += " > "
                        elif logical_operator == "less than" or logical_operator == "is less than":
                            final_output += " < "
                        elif logical_operator == "equals" or logical_operator == "equal to":
                            final_output += " == "
                        elif logical_operator == "GreaterOrEqual":
                            final_output += " >= "
                        elif logical_operator == "LessOrEqual":
                            final_output += " <= "
            if counter_comparison != len(comparison_operators):
                final_output += " " + comparison_operator + " "
        return final_output


def parse_response(file_name):
    with open(file_name, 'rb') as f:
        response = client.speech(f, {'Content-Type': 'audio/wav'})
    print(response)
    if response['intents'][0]['name'] == 'AssignVariable':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_assign_variable(response)

    elif response['intents'][0]['name'] == 'IfElseStatement':
        if response['intents'][0]['confidence'] > confidence_threshold:
            print(front_end_block)
            parse_if_else_statement(response)
            command_if = client.message(response['entities']['command:command'][0]['body'])
            nested_if = True
            if command_if['intents'][0]['name'] == 'DeclareVariable':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_assign_variable(command_if)
            if command_if['intents'][0]['name'] == 'AddingComment':
                if command_if['intents'][0]['confidence'] > confidence_threshold:
                    parse_add_comment(command_if)
            print("else:")
            resp3 = client.message(response['entities']['command:command'][1]['body'])
            if resp3['intents'][0]['name'] == 'DeclareVariable':
                if resp3['intents'][0]['confidence'] > confidence_threshold:
                    parse_assign_variable(resp3)
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
                            final_output += parse_assign_variable(command_if)
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

    elif response['intents'][0]['name'] == 'CreateFunction':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_create_function(response)
    elif response['intents'][0]['name'] == 'Return':
        if response['intents'][0]['confidence'] > confidence_threshold:
            return front_end_block + parse_return(response)
    else:
        return "dsd-section\nintent not found"


naming_style = "snake"
if len(sys.argv) > 1 and sys.argv[1] == "-snake":
    naming_style = "snake"
elif len(sys.argv) > 1 and sys.argv[1] == "-camel":
    naming_style = "camel"
client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
front_end_error = "dsd-section\nvocoder-error-message\n"
front_end_warning = "dsd-section\nvocoder-warning-message\n"
front_end_block = "dsd-section\nvocoder-code-block\n"
placeholder_string = "#placeholder"
confidence_threshold = 0.75
print(parse_response('DefineCount=1+1.wav'))
