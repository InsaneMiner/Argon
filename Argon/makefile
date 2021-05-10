#================================================================
COMPILER=gcc
LLVM=llc
OUTPUT=./output/output
LLVM_SOURCE=./output/output.ll
OBJECT_SOURCE=./output/output.o
LLVM_OUTPUT_TYPE=obj
LLVM_OPTIONS=-filetype=$(LLVM_OUTPUT_TYPE) 
COMPILER_OPTIONS=-fPIC -no-pie -fPIE
#================================================================
compile:
	$(LLVM) $(LLVM_OPTIONS) $(LLVM_SOURCE)
	$(COMPILER) $(OBJECT_SOURCE) -o $(OUTPUT) $(COMPILER_OPTIONS)
#================================================================
run:compile
	$(OUTPUT)
#================================================================
    