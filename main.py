import dis
import sys

try:
    code = open(sys.argv[1]).read()
    code = compile(code, '<string>', 'exec')
    
    dis.dis(code)
    
    print(code)
    print(dir(code))
    print(code.co_code)
    print(code.co_stacksize)
    #print(code.co_firstlineno)

    exec(code, {})

    print(code.co_stacksize)
except:
    print("PyVCS - Created by docmarionum1 and kevidryon2\nUsage: <path-to-pyvcs-python>/python main.py <file>")