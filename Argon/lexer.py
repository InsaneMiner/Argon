from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')

        self.lexer.add('INT',r'int')

        self.lexer.add('FUNCTION',r'func')

        self.lexer.add("FUNCTION_ARGS",r'\^\((.*?)\)')

        self.lexer.add("COMMENT",r"\!\!")

        self.lexer.add("FUNCTION_CODE",r'\{([\s\S]*?)\}')

        self.lexer.add("STRING",r'\"(.*?)\"')

        self.lexer.add("IF",r"if")

        self.lexer.add("DOUBLE_EQUEL",r'\=\=')
        

        self.lexer.add('EQUAL_SIGN',r'\=')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        self.lexer.add("CALL_FUNCTION",r"\<CALLER\>")


        self.lexer.add("GLOBAL_VAR",r"global")

        self.lexer.add("PRIVATE_VAR",r"private")

        self.lexer.add("RETURN",r'return')

        self.lexer.add("VOID",r'void')

        self.lexer.add('CHARACTERS',r'[a-zA-Z]+')

        self.lexer.add('ONE_OR_MORE_NEXTLINES',r'.*[\n]{1}.*')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        # Number
        self.lexer.add('NUMBER', r'\d+')


        


        # Ignore spaces
        self.lexer.ignore('\s+')
        self.lexer.ignore(r'\n')

       


    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()