from rply import LexerGenerator
import lexico

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()
        self.lexico = lexico.analizador_lexico()
        self.l_lex = []
    def _add_tokens(self):

        # palabras reservadas
        for p_res in self.lexico.reserver_words:
            #print (p_res)
            self.lexer.add("R_"+p_res, (r""+p_res))
            self.l_lex += ["R_"+p_res]
        # Delimitadores
        for p_del in self.lexico.delimiters:
            #print (r'\+')
            #print ((r'\\'+p_del)[1:])
            self.lexer.add("D_"+p_del,(r"\\"+p_del)[1:] )
            self.l_lex += ["D_"+p_del]
        # Operadores
        for p_ope in self.lexico.operators:
            #print (r'\+')
            #print ((r'\\'+p_ope)[1:])
            self.lexer.add("O_"+p_ope, (r"\\"+p_ope)[1:])
            self.l_lex += ["O_"+p_ope]
        # Real
        self.lexer.add('REAL', r'\d*\.\d+')
        self.l_lex += ['REAL']
        # Integer
        self.lexer.add('INTEGER', r'[0-9]+')
        self.l_lex += ['INTEGER']
        # String
        self.lexer.add('STRING', r'"[^"]*"')
        self.l_lex += ['STRING']
        # Id
        self.lexer.add('ID', r'[a-zA-Z][a-zA-Z0-9_]*')
        self.l_lex += ['ID']
        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


def main(data):
    lexer = Lexer()
    tokens = lexer.get_lexer().lex(data)
    return lexer.l_lex,tokens
    #for t in tokens:
    #    try:
    #        print (t)
    #    except:
    #        print ("error")

if __name__ == "__main__":
    main("hola 10.2 0.2 FLOAT ")