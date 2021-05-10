

def gen(output,source,object_source,compiler="gcc",llvm="llc",COMPILER_OPTIONS="-fPIC -no-pie -fPIE", LLVM_OPTIONS="",LLVM_OUTPUT_TYPE="obj"):

    makefile = bytes(f"""#================================================================
COMPILER={compiler}
LLVM={llvm}
OUTPUT={output}
LLVM_SOURCE={source}
OBJECT_SOURCE={object_source}
LLVM_OUTPUT_TYPE={LLVM_OUTPUT_TYPE}
LLVM_OPTIONS=-filetype=$(LLVM_OUTPUT_TYPE) {LLVM_OPTIONS}
COMPILER_OPTIONS={COMPILER_OPTIONS}
#================================================================
compile:
\t$(LLVM) $(LLVM_OPTIONS) $(LLVM_SOURCE)
\t$(COMPILER) $(OBJECT_SOURCE) -o $(OUTPUT) $(COMPILER_OPTIONS)
#================================================================
run:compile
\t$(OUTPUT)
#================================================================
    ""","utf-8")
    return makefile
