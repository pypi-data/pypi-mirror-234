import xlrd2
from Aciembler.Error import Error

def first_pass(path, add_base = 'd'):
    opcodes = ['LDM', 'LDD', 'LDI', 'LDX', 'LDR', 'MOV', 'STO', 'ADD', 'SUB', 'INC', 'DEC', 'JMP', 'CMP', 'CMI', 'JPE',
              'JPN', 'IN', 'OUT', 'END', 'AND', 'OR', 'XOR', 'LSL', 'LSR']
    add_opcode_to_memory = ['LDD', 'LDI', 'STO', 'CMI']
    add_opcode_to_opcode = ['JMP', 'JPE', 'JPN']
    add_and_val_opcodes = ['ADD', 'SUB', 'CMP', 'AND', 'XOR', 'OR']
    wb = xlrd2.open_workbook(path)
    program = []
    memory = []
    register = []

    for i in range(1, (sheet := wb.sheets()[0]).nrows):
        a, b, c, d = sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3)
        program.append([a, b, c, d])

    for i in range(1, (sheet := wb.sheets()[1]).nrows):
        a, b, c = sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2)
        memory.append([a, b, c])
    for i in range(0, (sheet := wb.sheets()[2]).nrows):
        try:
            a, b = sheet.cell_value(i, 0), sheet.cell_value(i, 1)
            register.append([a, b])
        except:
            if i == 0:
                register.append(["ACC", "#0"])
            elif i == 1:
                register.append(["IX", "#0"])

    for i in range(len(program)):
        if program[i][2] not in opcodes:
            Error("NameError", program[i][2], program[i][3])
            return 0, 0, 0
        else:
            if program[i][2] in add_opcode_to_memory:  # opcode with address that links to memory
                for j in range(len(memory)):
                    if program[i][3] == memory[j][1] or program[i][3] == memory[j][0]:  # the label of opcode meets the label in the memory
                        program[i][3] = memory[j][0]
                        break
                else:
                    Error("NameError", program[i][2], program[i][3])
                    return 0, 0, 0
            elif program[i][2] in add_opcode_to_opcode:  # opcode with address that links to opcode
                for j in range(len(program)):
                    if program[i][3] == program[j][1] or program[i][3] == program[j][0]:  # the label of opcode meets the label in the opcode
                        program[i][3] = program[j][0]
                        break
                else:
                    Error("NameError", program[i][2], program[i][3])
                    return 0, 0, 0
            elif program[i][2] in add_and_val_opcodes:  # opcode with address or value operands
                if program[i][3][0] not in ['#', '&'] and program[i][3][0] != 'B':  # the operand is not an decimal or hexadecimal address
                    for j in range(len(memory)):
                        if program[i][3] == memory[j][1] or program[i][3] == memory[j][0]:  # the label of opcode meets the label in the memory
                            program[i][3] = memory[j][0]
                            break
                    else:
                        Error("NameError", program[i][2], program[i][3])
                        return 0, 0, 0

                if program[i][3][0] == 'B':
                    if len(program[i][3])  < 2: # the operand is B, but not an address, B is a lable
                        for j in range(len(memory)):
                            if program[i][3] == memory[j][1] or program[i][3] == memory[j][0]:  # the label of opcode meets the label in the memory
                                program[i][3] = memory[j][0]
                                break
                        else:
                            Error("NameError", program[i][2], program[i][3])
                            return 0, 0, 0
                    else:
                        if program[i][3][1] not in ['0', '1']: # the operand is in form of BX, where X is not 0, or 1
                            for j in range(len(memory)):
                                if program[i][3] == memory[j][1] or program[i][3] == memory[j][0]:  # the label of opcode meets the label in the memory
                                    program[i][3] = memory[j][0]
                                    break
                            else:
                                Error("NameError", program[i][2], program[i][3])
                                return 0, 0, 0


    final_program = []
    final_memory = {}
    final_register = {}

    for i in range(len(program)):
        final_program.append([program[i][0], program[i][2], program[i][3]])

    for i in range(len(memory)):
        final_memory.update({memory[i][0]: memory[i][2]})

    for i in range(len(register)):
        final_register.update({register[i][0]: register[i][1]})
    return (final_program, final_memory, final_register)