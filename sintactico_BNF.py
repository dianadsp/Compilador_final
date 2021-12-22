from rply import ParserGenerator
from rply.token import BaseBox
import matplotlib.pyplot as plt

t_var = {}
out_data = ""

def print_out (data):
    global out_data
    print (data)
    out_data = str(data)+"\n"+out_data

def clear_out():
    global out_data
    out_data = ""

class BoxNumber(BaseBox):
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

class BoxList(BaseBox):
    def __init__(self, value):
        if value != None:
            self.value = [value]
        else:
            self.value = []

    def add(self, new):
        #print ("Recien llegado:", new, new.value)
        self.value += new.value

    def get(self):
        #print ("print",self.value)
        #for v in self.value:
        #    print (v,type(v))
        return [i.get() for i in self.value]

class BoxString(BaseBox):
    def __init__(self, value):
        self.value = value[1:-1]

    def get(self):
        return self.value

class BoxID(BaseBox):
    def __init__(self, i_name, value):
        self.value = value
        self.name = i_name

    def exe(self):
        t_var[self.name] = self.value

    def get(self):
        return t_var[self.name]

class BoxPrint(BaseBox):
    def __init__(self, value):
        self.value = value

    def exe(self):
        print_out (self.value)

class BoxSentences(BaseBox):
    def __init__(self):
        self.values = []

    def add (self,new):
        self.values += [new]

    def exe(self):
        for s in self.values:
            print ("--------------------",type(s))
            s.exe()

class BoxBool (BaseBox):
    def __init__(self, i_value):
        self.value = i_value

    def get(self):
        return bool(self.value)

class Parse_S():

    def __init__(self, stokens):
        #print(stokens)
        self.pg = ParserGenerator(stokens,
            precedence=[
            ('left', ['STRING', 'expr']),
            ('left', ['O_+', 'O_-']),
            ('left', ['O_*', 'O_/'])
            ]
        );

    def parse(self):

        @self.pg.production("main : main main")
        def main_main(p):
            if str(type(p[1])) != "<class 'NoneType'>":
                p[1].exe()
            if str(type(p[0])) != "<class 'NoneType'>":
                p[0].exe()

        @self.pg.production("main : declare")
        def main_declare(p):
            #print (type(p[0]))
            p[0].exe()

        @self.pg.production("main : R_PRINT D_( list D_) D_;")
        @self.pg.production("main : R_PRINT D_( expr D_) D_;")
        def print_fun (p):
            return BoxPrint (p[2].get())
        
        @self.pg.production("main : R_PRINT D_( ID D_) D_;")
        def print_id (p):
            if str(p[2].getstr()) in t_var:
                return BoxPrint (t_var[str(p[2].getstr())].get())
            else:
                print ("No esta declarada la variable '%s', \nERROR Semantico" % str(p[2].getstr()))
                raise AssertionError("No esta declarada la variable '%s', \nERROR Semantico" % str(p[2].getstr()))

        @self.pg.production("main : R_PRINT D_( STRING D_) D_;")
        def print_id (p):
            return BoxPrint (str(p[2].getstr()))

        @self.pg.production("expr : INTEGER")
        def expr_num(p):
            return BoxNumber(int(p[0].getstr()))

        @self.pg.production("expr : REAL")
        def expr_rel(p):
            return BoxNumber(float(p[0].getstr()))



        @self.pg.production("expr : ID")
        def expr_rel(p):
            if str(p[0].getstr()) in t_var:
                #print (type(t_var[str(p[0].getstr())].get()))
                return t_var[str(p[0].getstr())]
            else:
                print ("No esta declarada la variable '%s', \nERROR Semantico" % str(p[0].getstr()))
                raise AssertionError("No esta declarada la variable '%s', \nERROR Semantico" % str(p[0].getstr()))

        @self.pg.production('expr : D_( expr D_)')
        def expression_parens(p):
            return p[1]

        @self.pg.production("expr : expr O_+ expr")
        @self.pg.production("expr : expr O_- expr")
        @self.pg.production("expr : expr O_* expr")
        @self.pg.production("expr : expr O_/ expr")
        @self.pg.production("expr : expr O_== expr")
        @self.pg.production("expr : expr O_!= expr")
        @self.pg.production("expr : expr O_< expr")
        @self.pg.production("expr : expr O_<= expr")
        @self.pg.production("expr : expr O_> expr")
        @self.pg.production("expr : expr O_>= expr")
        @self.pg.production("expr : expr O_& expr")
        @self.pg.production("expr : expr O_! expr")

        def expr_op(p):
            lhs = p[0].get()
            rhs = p[2].get()
            if type(lhs) == str or type(rhs) == str:
                print ("No se Puede Operar Variables STRING, \nERROR Semantico")
                raise AssertionError("No se Puede Operar Variables STRING, \nERROR Semantico")
            if p[1].gettokentype() == "O_+":
                return BoxNumber(lhs + rhs)
            elif p[1].gettokentype() == "O_-":
                return BoxNumber(lhs - rhs)
            elif p[1].gettokentype() == "O_*":
                return BoxNumber(lhs * rhs)
            elif p[1].gettokentype() == "O_/":
                return BoxNumber(lhs / rhs)
            elif p[1].gettokentype() == "O_==":
                return BoxBool(lhs == rhs)
            elif p[1].gettokentype() == "O_!=":
                return BoxBool(lhs != rhs)
            elif p[1].gettokentype() == "O_<":
                return BoxBool(lhs < rhs)
            elif p[1].gettokentype() == "O_<=":
                return BoxBool(lhs <= rhs)
            elif p[1].gettokentype() == "O_>":
                return BoxBool(lhs > rhs)
            elif p[1].gettokentype() == "O_>=":
                return BoxBool(lhs >= rhs)
            elif p[1].gettokentype() == "O_&":
                return BoxBool(lhs and rhs)
            elif p[1].gettokentype() == "O_!":
                return BoxBool(lhs or rhs)

            else:
                print ("Es imposible operar el token %s, \nERROR Semantico" % p[1].gettokentype())
                raise AssertionError("Es imposible operar el token %s, \nERROR Semantico" % p[1].gettokentype())

        @self.pg.production("listvar : D_, expr")
        def list_var_expr (p):
            #print ("es exp:", p[1])
            return BoxList(p[1])

        @self.pg.production("listvar : D_, INTEGER")
        def list_var_expr (p):
            #print ("es exp:", p[1])
            return BoxList(BoxNumber(int((p[1].getstr()))))

        @self.pg.production("listvar : D_, REAL")
        def list_var_expr (p):
            #print ("es exp:", p[1])
            return BoxList(BoxNumber(float((p[1].getstr()))))

        @self.pg.production("listvar : D_, STRING")
        def list_var_str (p):
            return BoxList(BoxString(p[1].getstr()))

        @self.pg.production("listvar : D_, ID")
        def list_var_id (p):
            if str(p[1].getstr()) in t_var:
                return BoxList(t_var[str(p[1].getstr())])
            else:
                print ("No esta declarada la variable '%s', \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("No esta declarada la variable '%s', \nERROR Semantico" % str(p[1].getstr()))


        @self.pg.production("listvar : D_, list")
        def list_var_list (p):
            return BoxList(p[1])

        @self.pg.production("listvar : listvar listvar")
        def list_list (p):
            #print ("aqui:",p[0].get(),"->",p[1].get())
            l = BoxList(None)
            l.add(p[0])
            l.add(p[1])
            return l

        @self.pg.production("list : D_[ D_]")
        def list_none (p):
            return BoxList(None)

        @self.pg.production("list : D_[ STRING D_]")
        def list_str (p):
            return BoxList(BoxString(p[1].getstr()))

        @self.pg.production("list : D_[ ID D_]")
        def list_id (p):
            return BoxList(BoxID(p[1].getstr()))

        @self.pg.production("list : D_[ expr D_]")
        def list_expr (p):
            return BoxList(p[1])

        @self.pg.production("list : D_[ list D_]")
        def list_ll (p):
            return BoxList(p[1])

        @self.pg.production("list : D_[ STRING listvar D_]")
        def list_str (p):
            l = BoxList(BoxString(p[1].getstr()))
            l.add (p[2])
            return l

        @self.pg.production("list : D_[ ID listvar D_]")
        def list_id (p):
            if str(p[1].getstr()) in t_var:
                l = BoxList(t_var[str(p[1].getstr())])
                l.add (p[2])
                return l
            else:
                print ("No esta declarada la variable '%s', \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("No esta declarada la variable '%s', \nERROR Semantico" % str(p[1].getstr()))

        @self.pg.production("list : D_[ expr listvar D_]")
        def list_expr (p):
            l = BoxList(p[1])
            #print ("print p2:",p[2])
            l.add (p[2])
            return l

        @self.pg.production("list : D_[ list listvar D_]")
        def list_l (p):
            l = BoxList(p[1])
            l.add (p[2])
            return l

        @self.pg.production("declare : R_INTEGER ID O_= expr D_;")
        def declare_int (p):
            if str(p[1].getstr()) in t_var:
                print ("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
            else:
                return BoxID(str(p[1].getstr()), BoxNumber(int(p[3].value)))
                

        @self.pg.production("declare : R_FLOAT ID O_= expr D_;")
        def declare_float (p):
            if str(p[1].getstr()) in t_var:
                print ("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
            else:
                return BoxID(str(p[1].getstr()), p[3]) 
                

        @self.pg.production("declare : R_STRING ID O_= STRING D_;")
        def declare_str (p):
            if str(p[1].getstr()) in t_var:
                print ("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
            else:
                return BoxID(str(p[1].getstr()), BoxString(p[3].getstr()))
                

        @self.pg.production("declare : R_LIST ID O_= list D_;")
        def declare_str (p):
            if str(p[1].getstr()) in t_var:
                print ("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
                raise AssertionError("La Varible '%s' ya fue declarada previamente, \nERROR Semantico" % str(p[1].getstr()))
            else:
                return BoxID(str(p[1].getstr()), p[3])
                
        @self.pg.production("declare : ID O_= ID D_;")
        def declare_id (p):
            if not str(p[0].getstr()) in t_var:
                print ("La Varible '%s' no existe, \nERROR Semantico" % str(p[0].getstr()))
                raise AssertionError("La Varible '%s' no existe, \nERROR Semantico" % str(p[0].getstr()))
            else:
                if str(p[2].getstr()) in t_var:
                    return BoxID(str(p[0].getstr()), t_var[str(p[2].getstr())])
                else:
                    print ("No esta declarada la variable '%s', \nERROR Semantico" % str(p[0].getstr()))
                    raise AssertionError("No esta declarada la variable '%s', \nERROR Semantico" % str(p[0].getstr()))

        @self.pg.production("declare : ID O_= expr D_;")
        def declare_id (p):
            if not str(p[0].getstr()) in t_var:
                print ("La Varible '%s' no existe, \nERROR Semantico" % str(p[0].getstr()))
                raise AssertionError("La Varible '%s' no existe, \nERROR Semantico" % str(p[0].getstr()))
            else:
                return BoxID(str(p[0].getstr()), p[2])

        @self.pg.production("main : R_PLOT D_( list D_, list D_) D_;")
        def plot_fun (p):
            plt.plot(p[2].get(),p[4].get())
            plt.show()

        @self.pg.error
        def error_handler(token):
            print ("El token '%s' no se esperaba, \nERROR de Sintaxis" % token.gettokentype())
            raise ValueError("El token '%s' no se esperaba, \nERROR de Sintaxis" % token.gettokentype())


    def get_parser(self):
        return self.pg.build()