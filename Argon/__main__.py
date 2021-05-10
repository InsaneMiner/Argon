

from lexer import Lexer
from parser import Parser
from codegen import CodeGen
from subprocess import Popen, PIPE
import os
import libs.Errors as er
import sys
import argparse
import shutil
import libs.genmakefile as makefile
import warnings



def compile(file, output,output_dir):
    with open(file,"r") as f:
        text_input = f.read()
    text_input = text_input.split("\n")


    er.setenv("currentLine","0")



    codegen = CodeGen()

    module = codegen.module
    builder = codegen.builder
    printf = codegen.printf

    skip = 0

    for x in range(len(text_input)):
        
        if skip != 0:
            skip -= 1
            continue

        er.setenv("currentLine",str(int(er.getenv("currentLine"))+1))
        if text_input[x].replace("\n","") == "":
            
            continue
        

        if text_input[x].replace("\t","").replace("\n","").replace(" ","")[:4].replace(" ","") == "func":
            found_paren = False
            after_text = text_input[x:]
            curl_paren_code = ""
            for x1 in range(len(after_text)):
                curl_paren_code += f"{after_text[x1]}\n"
                if "}" in after_text[x1]:
                    found_paren = True
                    break
            if found_paren:
                lexer = Lexer().get_lexer()
                tokens = lexer.lex(curl_paren_code)
                skip = x1
            else:
                er.error(f"Error: No ending to curly braces. Start of curly braces on line {x}")
        else:
            lexer = Lexer().get_lexer()
            tokens = lexer.lex(text_input[x])

        
        lexer1 = Lexer().get_lexer()
        Tokens1 = lexer.lex(text_input[x])
        for token in Tokens1:
            print(token)
        

        pg = Parser(module, builder, printf)
        pg.parse()

        # This gives a warning, so i just ignore the warning.
        warnings.simplefilter("ignore")
        
        parser = pg.get_parser()
        parser.parse(tokens).eval()

        warnings.simplefilter("default")
        

    try:
        os.mkdir("./output/")
    except OSError as e:
        if e.errno == 17:
            pass
        else:
            sys.exit("Compiler Error: connot make output dir.")
    codegen.create_ir()


    codegen.save_ir(f"{output_dir}/{output}.ll")

    try:
        with open("./ArgonMakeFile","wb") as f:
            f.write(makefile.gen(output, f"{output_dir}/{output}.ll",f"{output_dir}/{output}.o"))
    except:
        sys.exit("Failed to write to file 'makefile'")

    process = Popen(['make','--makefile=ArgonMakeFile','compile'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr == b"":
        pass
    else:
        print(stderr.decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description='Gecko Compiler.')

    parser.add_argument("-f","--file", help="location of source file")
    parser.add_argument("-o","--output", help="location of the output file", default="./output.out")
    parser.add_argument("--keep-all-output", help="Keeps all outputed files, e.g(llvm ir file, object file)",action="store_true")
    parser.add_argument("--clean", help="Removes all uneeded files and folders",action="store_true")
    parser.add_argument("--new", help="Creates new Argon project",default="")
    

    args = parser.parse_args()



    if args.clean:
        try:
            os.mkdir("./output/")
            shutil.rmtree("./output/")
            sys.exit("Looks like it is already clean")
        except OSError as e:
            if e.errno == 17:
                try:
                    shutil.rmtree("./output/")
                    try:
                        os.remove("GeckoMakeFile")
                    except:
                        pass
                    sys.exit("Project cleaned")
                except Exception as e:
                    sys.exit("Failed to remove dir './output/'")
    if args.new != '':
        try:
            os.mkdir(f"./{args.new}")
            with open(f"./{args.new}/main.argon","w") as f:
                f.write("")
            sys.exit("Created project")

        except:
            sys.exit("Failed to create project")

    if args.file == None:
        sys.exit("No file input")
    

    try:
        open(args.file).read()
    except FileNotFoundError as fileerr:
        if fileerr.errno == 2:
            sys.exit("Source file does not exist")

    compile(args.file,args.output,"./output")

    if args.keep_all_output == False:
        try:
            os.remove(f"./output/{args.output}.ll")
            os.remove(f"./output/{args.output}.o")
        except:
            pass


if __name__ == "__main__":
    main()
else:
    sys.exit(0)