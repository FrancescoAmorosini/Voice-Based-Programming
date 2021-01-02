import unittest

from main import parse_response, parse_expression,parse

front_end_error = "dsd-section\nvocoder-error-message\n"
front_end_warning = "dsd-section\nvocoder-warning-message\n"
front_end_block = "dsd-section\nvocoder-code-block\n"
front_end_undo = "dsd-section\nvocoder-undo\n"
front_end_delete = "dsd-section\nvocoder-delete\n"
placeholder_string = "$$"


class MyTestCase(unittest.TestCase):

    def test_comment(self):
       self.assertEqual(parse_response('CommentHelloWorld.wav'), front_end_block + '# hello world')
    
    def test_if_statement(self):
        self.assertEqual(parse_response('CreateAnIfStatement.wav'),
                         front_end_block + 'if ' + placeholder_string + ' :\n\t' + placeholder_string)
        self.assertEqual(parse_response('IfCount5.wav'), front_end_block + 'if count > 5 :\n\t$$')
        self.assertEqual(parse_response('IfCountLessTwoPlusThen.wav'), front_end_block + 'if county < 2 + person :\n\t$$')

    # def test_if_else_statement(self):
    #    self.assertEqual(parse_response('CreateAnIfElseStatement.wav'), front_end_block + 'if '+ placeholder_string + ' :\n\t' + placeholder_string + '\nelse:\n\t' + placeholder_string)

    def test_while(self):
        self.assertEqual(parse_response('WhileLoop.wav'),
                         front_end_block + 'while ' + placeholder_string + ':\n\t' + placeholder_string)
        self.assertEqual(parse_response('WhileLoopExp.wav'), front_end_block + "while count == 5:\n\t" + placeholder_string)
    
    def test_for(self):
        self.assertEqual(parse_response('for_second.wav'),
                         front_end_block + 'for burgers and in range ( 0 , 10 ):\n\t' + placeholder_string)

    def test_assignVariable(self):
        self.assertEqual(parse_response('declare expression.wav'),
                         front_end_block + 'number_of_cars = 5 + 3 - number_of_entrances')
        self.assertEqual(parse_response('DefineVariableCount.wav'), front_end_block + 'count = None')
        self.assertEqual(parse_response('DefineCount=1+1.wav'), front_end_block + 'count = 1 + 1')
        self.assertEqual(parse_response('Declare_variable.wav'), front_end_block + 'number_of_cars = None')

    # def test_create_function(self):
    #    self.assertEqual(parse_response('CreateFunction.wav'), front_end_block + "def #FunctionName() :")

    # def test_undo_command(self):
    #    self.assertEqual(parse_response('undo1.wav'), front_end_undo)

    # def test_delete(self):
    #    self.assertEqual(parse_response('delete1.wav'), front_end_delete)

    # def test_return(self):
    #    self.assertEqual(parse_response('return.wav'), front_end_block + "return")

    def test_expressions(self):
        self.assertEqual(parse_expression("three plus four"), "3 + 4")
        self.assertEqual(parse("space greater than five and number of cars less than four"), "space > 5 "
                                                                                                        "and "
                                                                                                        "number_of_cars "
                                                                                                        "< 4")
    # Missing RedoCommand and InsertExpression
