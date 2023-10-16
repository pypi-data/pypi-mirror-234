import os, sys
def Error(err, Opcode, Operand):
    base = os.path.dirname(os.path.abspath(__file__))
    with open(base + '/objectCode.py', 'r') as f:
        a = f.readlines()
    a[0] = f'"{Opcode} {Operand}"\n'
    a[1] = f'err = {err}\n'
    with open(base + '/objectCode.py', 'w') as f:
        f.writelines(a)
    if sys.modules.get('Aciembler.objectCode'):
        sys.modules.pop('Aciembler.objectCode')
    import Aciembler.objectCode









