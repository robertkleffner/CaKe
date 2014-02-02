import sys
import fileinput

def emulate(instr, stack):
    quotesToPush = []
    
    instructions = []
    for c in instr:
        instructions.append(c)

    while len(instructions) > 0:
        c = instructions.pop(0)
        runCommand(c, stack, instructions, quotesToPush)
    print(str(stack).replace(',','').replace("'",''))

def runCommand(c, stack, instructions, quotesToPush):
    if c == '@':
            c = instructions.pop(0)
            if c == '\\':
                c = '\\' + instructions.pop(0)
            stack.append(c)
    elif c == '.':
        toprint = stack.pop()
        if toprint == '\\n':
            print()
        else:
            print(toprint, end="")
    elif c == '>':
        stack.append(sys.stdin.read(1))
    elif c == 'k':
        # [B] [A] k == A
        # executes the program on top of the stack
        # but first removes the element below it
        top = stack.pop()
        stack.pop()
        if isinstance(top, list):
            for i in top[::-1]:
                if isinstance(i, list):
                    quotesToPush.append(i)
                    instructions.insert(0, 's')
                else:
                    instructions.insert(0, i)
        else:
            raise Exception("K expects quotation on top of stack.")
    elif c == 'q':
        # [B] [A] q == [[B]] [A B]
        # pushes a quotation of [B] on the stack, and then
        # pushes a concatenation of A and B
        top = stack.pop()
        below = stack.pop()
        stack.append([below])
        
        cat = []
        for i in top:
            cat.append(i)
        for i in below:
            cat.append(i)
        stack.append(cat)
    elif c == 'o':
        # o == [] [q] [k]
        # Not much to it... pushes an empty quotation,
        # quoted q, and quoted k! That's it.
        stack.append(list())
        stack.append(['q'])
        stack.append(['k'])
    elif c == 's':
        stack.append(quotesToPush.pop())
    else:
        stack.append(c)

# []: [] == [[]]
emulate('ookok', [])

# k: [] [[]] == []
emulate('ookokookokk',[])

# zap: [[]] == 
emulate('ookokok',[])

# dip: [[]] [[]] == [] [[]]
emulate('ookokookokookkokookokookokookkokookokookkokoookokookkokkookokookkokkookokookokookkokookookokookkokkookokookokookkokookkookokookkokkookkookokookkokkookkookokookkokkookkkookkk',[])

# unit: [] == [[]]
emulate('ookokookokookkok',[])

# i: [[]] == []
emulate('ookokookokookkokookokookkk',[])

print("[CaKe]: ", end="")
line = sys.stdin.readline().strip('\n')
stack = []
while line != "quit":
    emulate(line, stack)
    print("[CaKe]: ", end="")
    line = sys.stdin.readline().strip('\n')
