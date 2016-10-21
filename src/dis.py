# The processor has seven 8-bit registers (A, B, C, D, E, H, and L), where A is the primary 8-bit accumulator and the other six registers can be used as either individual 8- # bit registers or as three 16-bit register pairs (BC, DE, and HL) depending on the particular instruction. Some instructions also enable the HL register pair to be used as a # (limited) 16-bit accumulator, and a pseudo-register, M, can be used almost anywhere that any other register can be used, referring to the memory address pointed to by the  # HL pair. It also has a 16-bit stack pointer to memory (replacing the 8008's internal stack), and a 16-bit program counter. 

#Example:
#; memcpy --
#; Copy a block of memory from one location to another.
#;
#; Entry registers
#;       BC - Number of bytes to copy
#;       DE - Address of source data block
#;       HL - Address of target data block
#;
#; Return registers
#;       BC - Zero
#
#            org     1000h       ;Origin at 1000h
#memcpy      public
#loop        mov     a,b         ;Test BC,
#            ora     c           ;If BC = 0,
#            rz                  ;Return
#            ldax    d           ;Load A from (DE)
#            mov     m,a         ;Store A into (HL)
#            inx     d           ;Increment DE
#            inx     h           ;Increment HL
#            dcx     b           ;Decrement BC
#            jmp     loop        ;Repeat the loop
#            end

# A simple disassembler for the 8080 CPU.
import binascii
import sys
import dis_helper as dh

# Get the file to disassemble, then create the output file name ("dis_filename")
source = str(sys.argv[1])
filename = source.split('.')[0] + "_dis.txt"

#Read the file
with open(source, "rb") as f:
	content = f.read()

hexed = binascii.hexlify(content).decode()
bit_size = int(len(hexed) / 2)

dis = ""

opcode = 0
cont = 0

#The contents of the designated register or memory) are incremented by 1 and the result is stored in the same place. If the operand is a memory location, its location is specified by the contents of the HL registers.
INR = "INR"

for x in range(0, bit_size):
	
	if cont > 0:
		cont-=1
		opcode+=1
		continue
	
	# Get the instruction opcode as 2 chars
	byte = hexed[x*2] + hexed[(x*2)+1]	
	instr = ""
	
	# Memory register 
	dest = ""

	if byte == "00":
		instr = "NOP"	
	
	elif byte == "01":
		instr = "LXI"
		
		# Offset is how many bytes instruction takes minus 1
		offset = 2 
		addr = "B,$"	
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "02":
		instr = "STAX"
		dest = "B"

	elif byte == "03":
		instr = "INX"
		dest = "B"

	elif byte == "04":
		instr = INR
		dest = "B"

	elif byte == "05":
		instr = "DCR"
		dest = "B"

	elif byte == "06":
		instr = "MVI"
		offset = 1 
		addr = "B,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "07":
		instr = "RLC"
	
	elif byte == "08":
		instr = ""

	elif byte == "09":
		instr = "DAD"
		dest = "B"

	elif byte == "0a":
		instr = "LDAX"
		dest = "B"

	elif byte == "0b":
		instr = "DCX"
		dest = "B"

	elif byte == "0c":
		instr = INR
		dest = "C"

	elif byte == "0d":
		instr = "DCR"
		dest = "C"
	
	elif byte == "0e":
		instr = "MVI"
		offset = 1 
		addr = "C,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "0f":
		instr = "RRC"

	elif byte == "10":
		instr = ""
	
	elif byte == "11":
		instr = "LXI"
		offset = 2 
		addr = "$,D"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "12":
		instr = "STAX"
		dest = "D"
	
	elif byte == "13":
		instr = "INX"
		dest = "D"

	elif byte == "14":
		instr = INR
		dest = "D"

	elif byte == "15":
		instr = "DCR"
		dest = "D"

	elif byte == "16":
		instr = "MVI"
		offset = 1 
		addr = "D,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "17":
		instr = "RAL"

	elif byte == "18":
		instr = ""

	elif byte == "19":
		instr = "DAD"
		dest = "D"

	elif byte == "1a":
		instr = "LDAX"
		dest = "D"

	elif byte == "1b":
		instr = "DCX"
		dest = "D"

	elif byte == "1c":
		instr = INR
		dest = "E"

	elif byte == "1d":
		instr = "DCR"
		dest = "E"

	elif byte == "1e":
		instr = "MVI"
		offset = 1 
		addr = "E,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "1f":
		instr = "RAR"
	
	elif byte == "20":
		instr = "RIM"

	elif byte == "21":
		instr = "LXI"
		offset = 2 
		addr = "$,H"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "22":
		instr = "SHLD"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "23":
		instr = "INX"
		dest = "H"

	elif byte == "24":
		instr = INR
		dest = "H"

	elif byte == "25":
		instr = "DCR"
		dest = "H"

	elif byte == "26":
		instr = "MVI"
		offset = 1 
		addr = "H,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "27":
		instr = "DAA"

	elif byte == "28":
		instr = ""

	elif byte == "29":
		instr = "DAD"
		dest = "H"

	elif byte == "2a":
		instr = "LHLD"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "2b":
		instr = "DCX"
		dest = "H"

	elif byte == "2c":
		instr = INR
		dest = "L"

	elif byte == "2d":
		instr = "DCR"
		dest = "L"

	elif byte == "2e":
		instr = "MVI"
		offset = 1 
		addr = "L,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "2f":
		instr = "CMA"

	elif byte == "30":
		instr = "SIM"

	elif byte == "31":
		instr = "LXI"
		offset = 2 
		addr = "$,SP"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "32":
		instr = "STA"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "33":
		instr = "INX"
		dest = "SP"

	elif byte == "34":
		instr = INR
		dest = "M"

	elif byte == "35":
		instr = "DCR"
		dest = "M"

	elif byte == "36":
		instr = "MVI"
		offset = 1 
		addr = "M,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "37":
		instr = "STC"

	elif byte == "38":
		instr = ""

	elif byte == "39":
		instr = "DAD"
		dest = "SP"

	elif byte == "3a":
		instr = "LDA"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "3b":
		instr = "DCX"
		dest = "SP"

	elif byte == "3c":
		instr = INR
		dest = "A"

	elif byte == "3d":
		instr = "DCR"
		dest = "A"

	elif byte == "3e":
		instr = "MVI"
		offset = 1 
		addr = "A,$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "3f":
		instr = "CMC"

	# MOV B
	elif byte == "40":
		instr = "MOV"
		dest = "B,B"

	elif byte == "41":
		instr = "MOV"
		dest = "B,C"	

	elif byte == "42":
		instr = "MOV"
		dest = "B,D"

	elif byte == "43":
		instr = "MOV"
		dest = "B,E"

	elif byte == "44":
		instr = "MOV"
		dest = "B,H"

	elif byte == "45":
		instr = "MOV"
		dest = "B,L"

	elif byte == "46":
		instr = "MOV"
		dest = "B,M"

	elif byte == "47":
		instr = "MOV"
		dest = "B,A"

	# MOV C
	elif byte == "48":
		instr = "MOV"
		dest = "C,B"

	elif byte == "49":
		instr = "MOV"
		dest = "C,C"	

	elif byte == "4a":
		instr = "MOV"
		dest = "C,D"

	elif byte == "4b":
		instr = "MOV"
		dest = "C,E"

	elif byte == "4c":
		instr = "MOV"
		dest = "C,H"

	elif byte == "4d":
		instr = "MOV"
		dest = "C,L"

	elif byte == "4e":
		instr = "MOV"
		dest = "C,M"

	elif byte == "4f":
		instr = "MOV"
		dest = "C,A"

	# MOV D
	elif byte == "50":
		instr = "MOV"
		dest = "D,B"

	elif byte == "51":
		instr = "MOV"
		dest = "D,C"	

	elif byte == "52":
		instr = "MOV"
		dest = "D,D"

	elif byte == "53":
		instr = "MOV"
		dest = "D,E"

	elif byte == "54":
		instr = "MOV"
		dest = "D,H"

	elif byte == "55":
		instr = "MOV"
		dest = "D,L"

	elif byte == "56":
		instr = "MOV"
		dest = "D,M"

	elif byte == "57":
		instr = "MOV"
		dest = "D,A"

	# MOV E
	elif byte == "58":
		instr = "MOV"
		dest = "E,B"

	elif byte == "59":
		instr = "MOV"
		dest = "E,C"	

	elif byte == "5a":
		instr = "MOV"
		dest = "E,D"

	elif byte == "5b":
		instr = "MOV"
		dest = "E,E"

	elif byte == "5c":
		instr = "MOV"
		dest = "E,H"

	elif byte == "5d":
		instr = "MOV"
		dest = "E,L"

	elif byte == "5e":
		instr = "MOV"
		dest = "E,M"

	elif byte == "5f":
		instr = "MOV"
		dest = "E,A"

	# MOV H
	elif byte == "60":
		instr = "MOV"
		dest = "H,B"

	elif byte == "61":
		instr = "MOV"
		dest = "H,C"	

	elif byte == "62":
		instr = "MOV"
		dest = "H,D"

	elif byte == "63":
		instr = "MOV"
		dest = "H,E"

	elif byte == "64":
		instr = "MOV"
		dest = "H,H"

	elif byte == "65":
		instr = "MOV"
		dest = "H,L"

	elif byte == "66":
		instr = "MOV"
		dest = "H,M"

	elif byte == "67":
		instr = "MOV"
		dest = "H,A"
	
	# MOV L
	elif byte == "68":
		instr = "MOV"
		dest = "L,B"

	elif byte == "69":
		instr = "MOV"
		dest = "L,C"	

	elif byte == "6a":
		instr = "MOV"
		dest = "L,D"

	elif byte == "6b":
		instr = "MOV"
		dest = "L,E"

	elif byte == "6c":
		instr = "MOV"
		dest = "L,H"

	elif byte == "6d":
		instr = "MOV"
		dest = "L,L"

	elif byte == "6e":
		instr = "MOV"
		dest = "L,M"

	elif byte == "6f":
		instr = "MOV"
		dest = "L,A"
	
	# MOV M
	elif byte == "70":
		instr = "MOV"
		dest = "M,B"

	elif byte == "71":
		instr = "MOV"
		dest = "M,C"	

	elif byte == "72":
		instr = "MOV"
		dest = "M,D"

	elif byte == "73":
		instr = "MOV"
		dest = "M,E"

	elif byte == "74":
		instr = "MOV"
		dest = "M,H"

	elif byte == "75":
		instr = "MOV"
		dest = "M,L"

	elif byte == "76":
		instr = "MOV"
		dest = "M,M"

	elif byte == "77":
		instr = "MOV"
		dest = "M,A"
	
	# MOV A
	elif byte == "78":
		instr = "MOV"
		dest = "A,B"

	elif byte == "79":
		instr = "MOV"
		dest = "A,C"	

	elif byte == "7a":
		instr = "MOV"
		dest = "A,D"

	elif byte == "7b":
		instr = "MOV"
		dest = "A,E"

	elif byte == "7c":
		instr = "MOV"
		dest = "A,H"

	elif byte == "7d":
		instr = "MOV"
		dest = "A,L"

	elif byte == "7e":
		instr = "MOV"
		dest = "A,M"

	elif byte == "7f":
		instr = "MOV"
		dest = "A,A"

	# ADD
	elif byte == "80":
		instr = "ADD"
		dest = "B"

	elif byte == "81":
		instr = "ADD"
		dest = "C"

	elif byte == "82":
		instr = "ADD"
		dest = "D"

	elif byte == "83":
		instr = "ADD"
		dest = "E"

	elif byte == "84":
		instr = "ADD"
		dest = "H"
		
	elif byte == "85":
		instr = "ADD"
		dest = "L"

	elif byte == "86":
		instr = "ADD"
		dest = "B"

	elif byte == "87":
		instr = "ADD"
		dest = "A"

	# ADC
	elif byte == "88":
		instr = "ADC"
		dest = "B"
	
	elif byte == "89":
		instr = "ADC"
		dest = "C"
	
	elif byte == "8a":
		instr = "ADC"
		dest = "D"

	elif byte == "8b":
		instr = "ADC"
		dest = "E"

	elif byte == "8c":
		instr = "ADC"
		dest = "H"

	elif byte == "8d":
		instr = "ADC"
		dest = "L"

	elif byte == "8e":
		instr = "ADC"
		dest = "M"

	elif byte == "8f":
		instr = "ADC"
		dest = "A"

	# SUB
	elif byte == "90":
		instr = "SUB"
		dest = "B"
	
	elif byte == "91":
		instr = "SUB"
		dest = "C"
	
	elif byte == "92":
		instr = "SUB"
		dest = "D"

	elif byte == "93":
		instr = "SUB"
		dest = "E"

	elif byte == "94":
		instr = "SUB"
		dest = "H"

	elif byte == "95":
		instr = "SUB"
		dest = "L"

	elif byte == "96":
		instr = "SUB"
		dest = "M"

	elif byte == "97":
		instr = "SUB"
		dest = "A"
	
	# SBB
	elif byte == "98":
		instr = "SBB"
		dest = "B"
	
	elif byte == "99":
		instr = "SBB"
		dest = "C"
	
	elif byte == "9a":
		instr = "SBB"
		dest = "D"

	elif byte == "9b":
		instr = "SBB"
		dest = "E"

	elif byte == "9c":
		instr = "SBB"
		dest = "H"

	elif byte == "9d":
		instr = "SBB"
		dest = "L"

	elif byte == "9e":
		instr = "SBB"
		dest = "M"

	elif byte == "9f":
		instr = "SBB"
		dest = "A"
	
	# ANA 
	elif byte == "a0":
		instr = "ANA"
		dest = "B"
	
	elif byte == "a1":
		instr = "ANA"
		dest = "C"
	
	elif byte == "a2":
		instr = "ANA"
		dest = "D"

	elif byte == "a3":
		instr = "ANA"
		dest = "E"

	elif byte == "a4":
		instr = "ANA"
		dest = "H"

	elif byte == "a5":
		instr = "ANA"
		dest = "L"

	elif byte == "a6":
		instr = "ANA"
		dest = "M"

	elif byte == "a7":
		instr = "ANA"
		dest = "A"
	
	# XRA 
	elif byte == "a8":
		instr = "XRA"
		dest = "B"
	
	elif byte == "a9":
		instr = "XRA"
		dest = "C"
	
	elif byte == "aa":
		instr = "XRA"
		dest = "D"

	elif byte == "ab":
		instr = "XRA"
		dest = "E"

	elif byte == "ac":
		instr = "XRA"
		dest = "H"

	elif byte == "ad":
		instr = "XRA"
		dest = "L"

	elif byte == "ae":
		instr = "XRA"
		dest = "M"

	elif byte == "af":
		instr = "XRA"
		dest = "A"

	# ORA 
	elif byte == "b0":
		instr = "ORA"
		dest = "B"
	
	elif byte == "b1":
		instr = "ORA"
		dest = "C"
	
	elif byte == "b2":
		instr = "ORA"
		dest = "D"

	elif byte == "b3":
		instr = "ORA"
		dest = "E"

	elif byte == "b4":
		instr = "ORA"
		dest = "H"

	elif byte == "b5":
		instr = "ORA"
		dest = "L"

	elif byte == "b6":
		instr = "ORA"
		dest = "M"

	elif byte == "b7":
		instr = "ORA"
		dest = "A"
	# CMP 
	elif byte == "b8":
		instr = "CMP"
		dest = "B"
	
	elif byte == "b9":
		instr = "CMP"
		dest = "C"
	
	elif byte == "ba":
		instr = "CMP"
		dest = "D"

	elif byte == "bb":
		instr = "CMP"
		dest = "E"

	elif byte == "bc":
		instr = "CMP"
		dest = "H"

	elif byte == "bd":
		instr = "CMP"
		dest = "L"

	elif byte == "be":
		instr = "CMP"
		dest = "M"

	elif byte == "bf":
		instr = "CMP"
		dest = "A"
	
	elif byte == "c0":
		instr = "RNZ"
		dest = ""

	elif byte == "c1":
		instr = "POP"
		dest = "B"
	
	elif byte == "c2":
		instr = "JNZ"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "c3":
		instr = "JMP"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "c4":
		instr = "CNZ"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "c5":
		instr = "PUSH"
		dest = "B"
		
	elif byte == "c6":
		instr = "ADI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "c7":
		instr = "RST"
		dest = "0"

	elif byte == "c8":
		instr = "RZ"
		dest = ""

	elif byte == "c9":
		instr = "RET"
		dest = ""
	
	elif byte == "ca":
		instr = "JZ"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "cb":
		instr = ""
		dest = ""
	
	elif byte == "cc":
		instr = "CZ"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "cd":
		instr = "CALL"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "ce":
		instr = "ACI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "cf":
		instr = "RST"
		dest = "1"
	
	elif byte == "d0":
		instr = "RNC"
		dest = ""
	
	elif byte == "d1":
		instr = "POP"
		dest = "D"
	
	elif byte == "d2":
		instr = "JNC"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "d3":
		instr = "OUT"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "d4":
		instr = "CNC"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "d5":
		instr = "PUSH"
		dest = "D"
	
	elif byte == "d6":
		instr = "SUI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "d7":
		instr = "RST"
		dest = "2"
	
	elif byte == "d8":
		instr = "RC"
		dest = ""

	elif byte == "d9":
		instr = ""
		dest = ""

	elif byte == "da":
		instr = "JC"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "db":
		instr = "IN"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "dc":
		instr = "CC"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "dd":
		instr = ""
		dest = ""
	
	elif byte == "de":
		instr = "SBI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "df":
		instr = "RST"
		dest = "3"
	
	elif byte == "e0":
		instr = "RPO"
		dest = ""
	
	elif byte == "e1":
		instr = "POP"
		dest = "H"
	
	elif byte == "e2":
		instr = "JPO"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "e3":
		instr = "XTHL"
		dest = ""
	
	elif byte == "e4":
		instr = "CPO"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "e5":
		instr = "PUSH"
		dest = "H"
	
	elif byte == "e6":
		instr = "ANI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "e7":
		instr = "RST"
		dest = "4"
	
	elif byte == "e8":
		instr = "RPE"
		dest = ""
	
	elif byte == "e9":
		instr = "PCHL"
		dest = ""
	
	elif byte == "ea":
		instr = "JPE"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "eb":
		instr = "XCHG"
		dest = ""
	
	elif byte == "ec":
		instr = "CPE"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "ed":
		instr = ""
		dest = ""

	elif byte == "ee":
		instr = "XRI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "ef":
		instr = "RST"
		dest = "5"
	
	elif byte == "f0":
		instr = "RP"
		dest = ""
	
	elif byte == "f1":
		instr = "POP"
		dest = "PSW"
	
	elif byte == "f2":
		instr = "JP"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "f3":
		instr = "DI"
		dest = ""
	
	elif byte == "f4":
		instr = "CP"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "f5":
		instr = "PUSH"
		dest = "PSW"

	elif byte == "f6":
		instr = "ORI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "f7":
		instr = "RST"
		dest = "6"
	
	elif byte == "f8":
		instr = "RM"
		dest = ""
	
	elif byte == "f9":
		instr = "SPHL"
		dest = ""

	elif byte == "fa":
		instr = "JM"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)
	
	elif byte == "fb":
		instr = "EI"
		dest = ""

	elif byte == "fc":
		instr = "CM"
		offset = 2 
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "fd":
		instr = ""
		dest = ""
	
	elif byte == "fe":
		instr = "CPI"
		offset = 1
		addr = "$"
		dest = dh.get_dest(offset, hexed, addr, x)
		cont = int(offset)

	elif byte == "ff":
		instr = "RST"
		dest = "7"

	dis += hex(opcode) + "\t" + instr + "\t" + dest + "\n" 

	opcode += 1

with open(filename, "w") as f:
	f.write(dis)

