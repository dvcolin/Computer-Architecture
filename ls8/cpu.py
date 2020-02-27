"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.branch_table = {
            HLT: self.HLT,
            PRN: self.PRN,
            LDI: self.LDI,
            MUL: self.MUL,
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET,
            ADD: self.ADD
        }
        self.sp = 0xF4

    def HLT(self, op_a, op_b):
        sys.exit()

    def LDI(self, op_a, op_b):
        self.reg[op_a] = op_b

    def PRN(self, op_a, _):
        print(self.reg[op_a])

    def MUL(self, op_a, op_b):
        self.alu(MUL, op_a, op_b)

    def PUSH(self, op_a, _):
        self.sp -= 1
        self.ram[self.sp] = self.reg[op_a]

    def POP(self, op_a, _):
        self.reg[op_a] = self.ram[self.sp]
        self.sp += 1
        return self.reg[op_a]

    def CALL(self, op_a, _):
        self.sp -= 1
        self.ram[self.sp] = self.pc + 1
        self.pc = self.reg[op_a] - 2

    def RET(self, op_a, _):
        self.pc = self.POP(op_a, _)

    def ADD(self, op_a, op_b):
        self.alu(ADD, op_a, op_b)

    def load(self):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
        if len(sys.argv) != 2:
            print('Please provide a file name as a second argument.')
            sys.exit()

        filename = sys.argv[1]
        with open(filename, 'r') as file:
            address = 0
            for line in file:
                line_text = line.strip().split('#')
                command = line_text[0]
                if command == '':
                    continue
                self.ram[address] = int(command, 2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            value = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = value
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""

        while True:
            command = self.ram[self.pc]
            num_operands = command >> 6
            IR = self.branch_table[command]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            IR(operand_a, operand_b)
            self.pc += num_operands + 1
