"""CPU functionality."""

import sys

LDI = int(0b10000010)
PRN = int(0b01000111)
HLT = int(0b00000001)
MUL = int(0b10100010)


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
        if len(sys.argv) != 2:
            print('Too many arguments provided.')
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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            value = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = value
            print(value)
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
        # IR = self.pc
        while True:
            command = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if command == HLT:
                sys.exit()
            elif command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif command == MUL:
                self.alu(MUL, operand_a, operand_b)
                self.pc += 2
