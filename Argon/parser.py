from rply import ParserGenerator
from ast import Number, Sum, Sub, Print, INT_VAR,CHANGE_VARIABLE_VALUE,DEFINE_FUNCTION,COMMENT,FUNCTION_CODE,CALL_FUNCTION,RETURN,IF_STATEMENT
import sys 
import libs.Errors as er

class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUMBER', 'PRINT', 'OPEN_PAREN', 'CLOSE_PAREN',
             'SEMI_COLON', 'SUM', 'SUB', "INT", 'CHARACTERS',
             'EQUAL_SIGN','FUNCTION','FUNCTION_ARGS','COMMENT',
             'STRING','FUNCTION_CODE','CALL_FUNCTION',"ONE_OR_MORE_NEXTLINES",
             'PRIVATE_VAR','GLOBAL_VAR','RETURN','VOID','DOUBLE_EQUAL','IF',
             ]
        )
        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):

        
        @self.pg.production('program : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        @self.pg.production('program : PRINT OPEN_PAREN CHARACTERS CLOSE_PAREN SEMI_COLON')
        def program(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('program : GLOBAL_VAR INT CHARACTERS EQUAL_SIGN NUMBER SEMI_COLON')
        @self.pg.production('program : PRIVATE_VAR INT CHARACTERS EQUAL_SIGN NUMBER SEMI_COLON')
        def program(p):
            return INT_VAR(self.builder, self.module, p[0].value,p[2].value ,p[4].value)
        @self.pg.production('program : RETURN NUMBER SEMI_COLON')  
        @self.pg.production('program : RETURN VOID SEMI_COLON')  
        def program(p):
            return RETURN(self.builder, self.module, p[1].value)
        @self.pg.production('program : CHARACTERS EQUAL_SIGN NUMBER SEMI_COLON')
        def program(p):
            return CHANGE_VARIABLE_VALUE(self.builder, self.module, p[0].value ,p[2].value)


        @self.pg.production('program : FUNCTION CHARACTERS FUNCTION_ARGS FUNCTION_CODE')
        @self.pg.production('program : FUNCTION CHARACTERS FUNCTION_ARGS ONE_OR_MORE_NEXTLINES FUNCTION_CODE')
        def program(p):
            return DEFINE_FUNCTION(self.builder, self.module,self.printf, p[1].value,p[2].value, p[3].value)

        @self.pg.production('program : COMMENT STRING')
        def program(p):
            return COMMENT(self.builder, self.module)

        #@self.pg.production('program : FUNCTION_CODE')
        #def program(p):
        #    return FUNCTION_CODE(self.builder, self.module,p[0].value,self.printf)

        @self.pg.production('program : CALL_FUNCTION STRING FUNCTION_ARGS SEMI_COLON')
        def program(p):
            return CALL_FUNCTION(self.builder, self.module,p[1].value,p[2].value)

        @self.pg.production('program : IF OPEN_PAREN STRING CLOSE_PAREN FUNCTION_CODE')
        def program(p):
            return IF_STATEMENT(self.builder, self.module)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'SUM':
                return Sum(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            if token.name == "$end":
                sys.exit("Error: Missing ';'")
            er.error("Error: "+str(token))


    def get_parser(self):
        return self.pg.build()