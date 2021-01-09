import unittest

from word2number import w2n

from main import parse_response, parse_expression, parse, decapitalize_word, string_to_camel, snake_to_camel

front_end_error = "dsd-section\nvocoder-error\n"
front_end_warning = "dsd-section\nvocoder-warning\n"
front_end_block = "dsd-section\nvocoder-code-block\n"
front_end_undo = "dsd-section\nvocoder-undo\n"
front_end_redo = "dsd-section\nvocoder-redo\n"
front_end_delete = "dsd-section\nvocoder-delete\n"
placeholder_string = "$$"


class MyTestCase(unittest.TestCase):

    def test_deCapitalize(self):
        self.assertEqual(decapitalize_word(""), "")

    def test_snake_to_camel(self):
        self.assertEqual(snake_to_camel("hello_world"), "HelloWorld")

    def test_string_to_camel(self):
        self.assertEqual(string_to_camel("hello world"), "helloWorld")

    def test_intent_error(self):
        self.assertEqual(parse_response('IntentError.wav'), front_end_error + 'intent not Detected')

    def test_comment(self):
        self.assertEqual(parse_response('CommentHelloWorld.wav'), front_end_block + '# hello world')
        self.assertEqual(parse_response('CommandComment.wav'), front_end_block + '# hello world this has to make an error')
        self.assertEqual(parse_response('LongComment.wav'), front_end_block + "# this is a very long command which should be split into lines i have to go shopping i\n# have to go to the university and i'm going to drink a coffee now please split it into lines")

    def test_if_statement(self):
        self.assertEqual(parse_response('CreateAnIfStatement.wav'),
                         front_end_block + 'if ' + placeholder_string + ' :\n\t' + placeholder_string)
        self.assertEqual(parse_response('IfCount5.wav'), front_end_block + 'if count > 5 :\n\t$$')
        self.assertEqual(parse_response('IfAssign.wav'), front_end_block + "if count == 5 :\n\ttest = testing")
        self.assertEqual(parse_response('IfCall.wav'), front_end_block + "if count == 5 :\n\tevaluated_weather ()")
        self.assertEqual(parse_response('IfReturn.wav'), front_end_block + "if there > 2 :\n\treturn high")
        self.assertEqual(parse_response('IfDefineNone.wav'), front_end_block + "if country_s == 5 :\n\tcount = None\n")
        self.assertEqual(parse_response('IfShortComment.wav'), front_end_block + "if number == 2 :\n\t# hello world")

    def test_if_else_statement(self):
       self.assertEqual(parse_response('IfElseReturn.wav'), front_end_block + 'if country == 5 :\n\treturn\nelse:\n\treturn count')

    def test_while(self):
        self.assertEqual(parse_response('WhileLoop.wav'),
                         front_end_block + 'while ' + placeholder_string + ':\n\t' + placeholder_string)
        self.assertEqual(parse_response('WhileLoopExp.wav'),
                         front_end_block + "while count == 5:\n\t" + placeholder_string)
        self.assertEqual(parse_response('whiletest.wav'),
                         front_end_block + "while counter > 5:\n\t" + placeholder_string)
        self.assertEqual(parse_response('WhileUntilTest.wav'),
                         front_end_block + "while test_if_not == fail_value:\n\t" + placeholder_string)

    def test_for(self):
        self.assertEqual(parse_response('ForRange1_10.wav'),
                         front_end_block + 'for number in range ( 0 , 10 ):\n\t' + placeholder_string)
        self.assertEqual(parse_response('fors2ed.wav'), front_end_warning + "Variable Name not understood\n" 
                        + front_end_block + "for $$ in range ( 0 , 10 ):\n\t$$")
        self.assertEqual(parse_response('ForElemInCount.wav'),
                         front_end_block + "for element in count:\n\t" + placeholder_string)
        self.assertEqual(parse_response('EmptyFor.wav'), front_end_block + "for $$ in range( $$,$$ ):\n\t$$")
        self.assertEqual(parse_response('ForRangeFrom0Until.wav'), front_end_warning + "Second Expression name was not understood in for loop\n" + front_end_block + "for weather in range ( saro , $$ ):\n\t$$")
        self.assertEqual(parse_response('ForLoopMissingExp.wav'), front_end_warning + "Second Variable name was not understood in for loop\n" + front_end_block + "for weather in $$:\n\t$$")


    def test_assignVariable(self):
        self.assertEqual(parse_response('declare expression.wav'),
                         front_end_block + 'number_of_cars = 5 + 3 - number_of_entrances')
        self.assertEqual(parse_response('DefineCount=1+1.wav'), front_end_block + 'count = 1 + 1')
        self.assertEqual(parse_response('Declare_variable.wav'),
                         front_end_block + 'number_of_cars = ' + placeholder_string)
        self.assertEqual(parse_response('DefineVariabeA.wav'),
                         front_end_error + "Variable Name not found")
        self.assertEqual(parse_response('DefineVariableCount.wav'),
                         front_end_block + "count = $$")

    def test_create_function(self):
        self.assertEqual(parse_response('CreateFunction.wav'), front_end_error + "FunctionName not found")
        self.assertEqual(parse_response('CreateFunction0Params.wav'), front_end_block + "def multiply ():\n\t")
        self.assertEqual(parse_response('CreateFunction2.wav'),
                        front_end_block + "def evaluate_weather (username_common_mail):\n\t")

    def test_call_function(self):
        self.assertEqual(parse_response('CallFunction.wav'), front_end_block + "evaluate_weather (de)")
        self.assertEqual(parse_response('CallFunctionWeather.wav'), front_end_block + "evaluate_weather ()")

    def test_undo_command(self):
        self.assertEqual(parse_response('Undo.wav'), front_end_undo)
        self.assertEqual(parse_response('Undo16.wav'), front_end_undo + "16")

    def test_redo_command(self):
        self.assertEqual(parse_response('Redo20.wav'), front_end_redo + "20")
        self.assertEqual(parse_response('Redo.wav'), front_end_redo)

    def test_delete(self):
        self.assertEqual(parse_response('Delete1_11.wav'), front_end_delete + "1\n11")
        self.assertEqual(parse_response('Delete.wav'), front_end_delete)
        self.assertEqual(parse_response('Delete1_error.wav'), front_end_error + "delete line numbers where not understood")


    def test_return(self):
        self.assertEqual(parse_response('Return.wav'), front_end_block + "return")
        self.assertEqual(parse_response('ReturnVacDays.wav'), front_end_block + "return vacation_days")

    def test_insert_expression(self):
        self.assertEqual(parse_response('InsExp.wav'), front_end_block + "number + 3 * 4")
        self.assertEqual(parse_response('InsExpErr.wav'), front_end_error + "Expression not found")

    def test_expressions(self):
        self.assertEqual(parse_expression("three plus four"), "3 + 4")
        self.assertEqual(parse("space greater than five and number of cars less than four"), "space > 5 "
                                                                                             "and "
                                                                                             "number_of_cars "
                                                                                             "< 4")
        self.assertEqual(parse("three plus four is less than number of cars and x is greater than five"),
                         "7 < number_of_cars and x > 5")
        self.assertEqual(parse("index or number of times"),
                         "index or numberof")
        self.assertEqual(parse_expression("three mod four division two"), "3 % 4 / 2")
        self.assertEqual(parse("space greater or equal to five and number of cars less or equal to four"), "space >= 5 "
                                                                                             "and "
                                                                                             "number_of_cars "
                                                                                             "<= 4")
        self.assertEqual(parse("space greater or equal to one hundred and number of cars less or equal to four"), "space >= 100 "
                                                                                                           "and "
                                                                                                           "number_of_cars "
                                                                                                           "<= 4")
        #self.assertEqual(parse("one hundred and twenty-eight"),"128")

