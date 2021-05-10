from llvmlite import ir
import libs.common
import sys
import parser as pr
import lexer as le
import os 
import libs.Errors as er
import warnings

functions = {}

current_function = "main"
last_defined_function = "main"


functions[current_function] = {"blocks":{},"variables":{},"function_object":None,"global":{}}





class Number():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i



class ArgumentIntVar():
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i





class BinaryOp():
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):
    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class Print():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value
    def eval(self):
        global functions
        try:
            int(self.value.value)
            int_value = 1
        except:
            int_value = 0
         
        if int_value == 0:
            value = self.value.value
        else:
            value = self.value.eval()
        

        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()

        fmt = "%i \n\0"

        if "fstr" in functions["main"]["variables"]:
            pass
        else:
            c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                                bytearray(fmt.encode("utf8")))
            global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=f"fstr")
            global_fmt.linkage = 'internal'
            global_fmt.global_constant = True
            global_fmt.initializer = c_fmt
            functions["main"]["variables"]["fstr"]  = global_fmt


        fmt_arg = self.builder.bitcast(functions["main"]["variables"]["fstr"], voidptr_ty)

        # Call Print Function
        printed= 0
        if int_value == 0:
            if value not in functions[current_function]["variables"]:
                if current_function != "main":
                    for x in range(len(functions[current_function]["function_object"].args)):
                        if functions[current_function]["function_object"].args[x].name == value:
                            self.builder.call(self.printf, [fmt_arg, functions[current_function]["function_object"].args[x]])
                            printed = 1
                            break
                        else:
                            pass
                    if printed:
                        pass
                    else:
                        er.error("Please enter a valid variable into print function.")
                elif value in functions["main"]["global"]:
                    self.builder.call(self.printf, [fmt_arg, functions["main"]["global"][value]])
                else:
                    pass
            else:
                self.builder.call(self.printf, [fmt_arg, functions[current_function]["variables"][value]])
        else:
            self.builder.call(self.printf, [fmt_arg, value])
        

class INT_VAR():
    def __init__(self, builder, module, var_type,VAR_NAME,value):
        self.builder = builder
        self.module = module
        self.value = value
        self.VAR_NAME = VAR_NAME
        self.type = var_type

    def eval(self):
        global functions
        global current_function
        if self.type == "private":
            if self.VAR_NAME not in functions[current_function]["variables"] and self.VAR_NAME not in functions["main"]["global"]:
                value_ = ir.Constant(ir.IntType(32), self.value)

                alloca_name =str(f"{self.VAR_NAME}")
                i = self.builder.alloca(ir.IntType(32),None,alloca_name)

                j = self.builder.store(value_ , i,None)

                k = self.builder.load(i,"",None)
                functions[current_function]["variables"][f"{self.VAR_NAME}-pointer"] = i
                functions[current_function]["variables"][f"{self.VAR_NAME}"] = k
            else:
                er.error("Variable already defined")
        elif self.type == "global":
            if self.VAR_NAME not in functions[current_function]["variables"] and self.VAR_NAME not in functions["main"]["global"]:
                value_ = ir.Constant(ir.IntType(32), int(self.value))
                variable = ir.GlobalVariable(self.module,  ir.IntType(32),self.VAR_NAME)
                variable.linkage = "internal"
                #variable.global_constant = True
                variable.initializer = value_
                functions["main"]["global"][f"{self.VAR_NAME}"] = variable
            else:
                er.error("Variable already defined")
        
        return ""


class CHANGE_VARIABLE_VALUE():
    def __init__(self, builder, module, VAR_NAME,value):
        self.builder = builder
        self.module = module
        self.value = value
        self.VAR_NAME = VAR_NAME

    def eval(self):
        global current_function
        global function
        try:
            self.value = int(self.value)
            value_ = ir.Constant(ir.IntType(32), self.value)
        except:
            print("Failed")

        


        if self.VAR_NAME in functions[current_function]["variables"]:
            if functions[current_function]["variables"][self.VAR_NAME].type.width == 32:
                if type(self.value) is int:
                    j = self.builder.store(value_ , functions[current_function]["variables"][f"{self.VAR_NAME}-pointer"],None)
                    k = self.builder.load(functions[current_function]["variables"][f"{self.VAR_NAME}-pointer"],"",None)
                    functions[current_function]["variables"][self.VAR_NAME] = k

                else:
                    er.error(f"Inputed value is not type int")
            else:
                print("Var not int")
        elif self.VAR_NAME in variables["main"]["global"]:
            er.err("This is a global variable can not be changed")
        else:
            sys.exit(f"Error: Variable '{self.VAR_NAME}' does not exist ")
        return k

class DEFINE_FUNCTION():
    def __init__(self, builder, module,printf,value, args,function_code):
        self.builder = builder
        self.module = module
        self.value = value
        self.args = args
        self.printf = printf
        self.function_code = function_code
    def eval(self):
        global last_defined_function
    
        args = self.args[2:-1].split(",")
        function_args = []
        for arg in args:    
            if arg.replace(" ","")[:3] == "int":
                function_args.append(ir.IntType(32))

        try:
            func_ty = ir.FunctionType(ir.IntType(32),function_args)
            func = ir.Function(self.module, func_ty, name=f'{str(self.value)}')
        except Exception as e:
            er.error(f"Function '{e}' already defined")
        
        block = func.append_basic_block(name='entry')

        functions[f"{self.value}"] = func

        arg_amount = 0

        for arg in args:
            if arg.replace(" ","")[:3] == "int":
                func.args[arg_amount].name = arg[3:].replace(" ","")
            arg_amount+=1

        last_defined_function = f'{str(self.value)}'
        functions[f'{str(self.value)}'] = {"blocks":{"entry": block},"variables":{},"function_object":func}


        fun_code = FUNCTION_CODE(self.builder,self.module,self.function_code,self.printf).eval()


        return func
class COMMENT():
    def __init__(self, builder, module):
        self.builder = builder
        self.module = module
    def eval(self):
        return ""

class FUNCTION_CODE():
    def __init__(self,builder, module,code,printf):
        self.builder = builder
        self.module = module
        self.code = code
        self.printf = printf
    def eval(self):
        global current_function
        global last_defined_function
        current_function = last_defined_function
        self.code = self.code[1:-1].replace("\n\n","").replace("\t","").split("\n")[:-1]

        with self.builder.goto_block(functions[current_function]["blocks"]["entry"]):
            for x in range(len(self.code)):
                if self.code[x].replace("\n","") == "":
                    er.setenv("currentLine",str(int(er.getenv("currentLine"))+1))
                    continue
                lexer = le.Lexer().get_lexer()
                tokens = lexer.lex(self.code[x])
                
                token_temp = lexer.lex(self.code[x])
                looped = 0
                for x in token_temp:
                    if x.value == "func" and looped == 0:
                        er.setenv("currentLine",str(int(er.getenv("currentLine"))-1))
                        er.error("Error: Functions can not be defined from inside another function")
                    else:
                        break

                pg = pr.Parser(self.module, self.builder, self.printf)
                pg.parse()

                warnings.simplefilter("ignore")

                parser = pg.get_parser()
                
                parser.parse(tokens).eval()

                warnings.simplefilter("default")

                er.setenv("currentLine",str(int(er.getenv("currentLine"))+1))
            value_ = ir.Constant(ir.IntType(32), 1)
            #self.builder.ret(value_)
            block_terminated = functions[current_function]["blocks"]["entry"].is_terminated
            if block_terminated:
                pass
            else:
                function_name  = functions[current_function]["function_object"].name
                er.error(f"Function '{function_name}' needs to be returned")
        current_function = "main"
        
        return ""

class CALL_FUNCTION():
    def __init__(self, builder, module,name, args):
        self.builder = builder
        self.module = module
        self.name = name
        self.args = args
    def eval(self):
        global functions
        args = self.args[2:-1].split(",")

        if self.name[1:-1] not in functions.keys():
            er.error(f"Function '{self.name[1:-1]}' is not defined")

        args_ = []
        for arg in args:    
            try:
                if arg == "":
                    continue
                else:
                    int(arg.replace(" ",""))
                    args_.append(ir.Constant(ir.IntType(32), int(arg.replace(" ",""))))
            except:
                er.error("Not a interger")
        if len(args_) > len(functions[self.name[1:-1]]["function_object"].args):
            er.error("To many arguments passed")
        elif len(args_) < len(functions[self.name[1:-1]]["function_object"].args):
            er.error("Not enough arguments passed")
        self.builder.call(functions[self.name[1:-1]]["function_object"],args_,name="",cconv=None, tail=False, fastmath=())


        return ""



class RETURN():
    def __init__(self, builder, module,value):
        self.builder = builder
        self.module = module
        self.value = value
    def eval(self):
        global function
        global current_function
        try:
            self.value = int(self.value)
        except:
            pass

        if type(self.value) is int:
            self.value = ir.Constant(ir.IntType(32), int(self.value))
            self.builder.ret(self.value)
        elif self.value == "void":
            try:
                self.builder.ret_void()
            except:
                self.value = ir.Constant(ir.IntType(32), int(0))
                self.builder.ret(self.value)



        
        
        return ""

class IF_STATEMENT():
    def __init__(self, builder, module):
        self.builder = builder
        self.module = module
    def eval(self):

        return ""

