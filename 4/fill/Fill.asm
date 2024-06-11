// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(BEGIN)
  //choose black or white 
  @KBD
  D=M
  @WHITE
  D;JEQ
  @BLACK
  0;JMP

(DRAW_LOOP_INIT)
  // i = 8192, addr = 16384
  @8192
  D=A
  @i
  M=D

  @SCREEN
  D=A
  @addr
  M=D

(DRAW_LOOP)
  // if i is 0 goto begin
  @i
  D=M
  @BEGIN
  D;JEQ

  // D = R0 (color to fill)
  @R0
  D=M

  // A = addr, [A] = D (R0)
  @addr
  A=M
  M=D

  // addr = addr + 1
  @addr
  D=M+1
  M=D

  // i = i - 1
  @i
  D=M
  D=D-1
  M=D

  @DRAW_LOOP
  0;JMP

(BLACK)
  // R0 = -1
  @R0
  M=-1
  @DRAW_LOOP_INIT
  0;JMP

(WHITE)
  // R0 = 0
  @R0
  M=0
  @DRAW_LOOP_INIT
  0;JMP
