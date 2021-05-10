; ModuleID = "Argon Code Generater. file: ./codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = call i32 @"mainw"()
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

declare i32 @"sum"(i32 %"a", i32 %"b") 

define i32 @"mainw"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"fstr" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i8 1)
  ret i32 1
}

@"fstr" = internal constant [5 x i8] c"%i \0a\00"