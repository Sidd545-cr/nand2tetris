// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.


//Check if r1 or r2 are zero

@R0
D=M
@ZERO
D;JEQ 

@R1
D=M
@ZERO
D;JEQ 

//subtract 1 from i
@R0
D=M
@i
M=D-1

//push r1 in r2(result)
@R1
D=M
@R2
M=D

//do the monkey dance
(loop)
//check if i is 0
@i
D=M
@END
D;JEQ

//add r1 to r2
@R1
D=M
@R2
M=D+M
//i--
@i
D=M-1
M=D
@loop
0;JMP

(ZERO)
@R2
M=0
@END
0;JMP


(END)
@END
0;JMP 

