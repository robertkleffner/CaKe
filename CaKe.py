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
    if "quoteIndex" not in runCommand.__dict__:
        runCommand.quoteIndex = 0
    
    if runCommand.quoteIndex or c == '[':
        if c == '[':
            runCommand.quoteIndex += 1
            stack.append(runCommand.quoteIndex) # use boolean becuase we don't have them in eck
        elif c == ']':
            # create a separate list of all the values up to the latest quote index
            if runCommand.quoteIndex > 0:
                values = stack[stack.index(runCommand.quoteIndex)+1:len(stack)]
                del stack[stack.index(runCommand.quoteIndex):len(stack)]
                stack.append(values)
                runCommand.quoteIndex -= 1
        else:
            stack.append(c)
        return
    elif c == '@':
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
    elif c == 'c':
        # [B] [A] c == [[B] A] [A [B]]
        # can be expressed as c == [cons] sip2 take
        top = stack.pop()
        below = stack.pop()
        one = []
        two = []
        one.append(below)
        for i in top:
            one.append(i)
            two.append(i)
        two.append(below)
        stack.append(one)
        stack.append(two)
    elif c == 's':
        stack.append(quotesToPush.pop())
    else:
        stack.append(c)

### push combinator x:  == x
##print(emulate('[]').replace(',','').replace("'",''))
##print(emulate('[k]').replace(',','').replace("'",''))
##print(emulate('[c]').replace(',','').replace("'",''))
##
### k: [[]] [[]] == []
##print(emulate('[[]][[]]k').replace(',','').replace("'",''))
##
### c: [[]] [[]] == [[[]] []] [[] [[]]]
##print(emulate('[[]][[]]c').replace(',','').replace("'",''))
##
### zap: [[]] == 
##print(emulate('[[]][]k').replace(',','').replace("'",''))
##
### dip: [[]] [[]] == [] [[]]
##print(emulate('[[]][[]]ck').replace(',','').replace("'",''))
##
### cons: [[]] [[]] == [[[]] []]
##print(emulate('[[]][[]]c[]k').replace(',','').replace("'",''))
##
### unit: [] == [[]]
##print(emulate('[][]c[]k').replace(',','').replace("'",''))
##
### i: [[]] == []
##print(emulate('[[]][[]]ckk').replace(',','').replace("'",''))
##
### dup: [] == [] []
##print(emulate('[][]cckck').replace(',','').replace("'",''))
##
### hello world:
##print(emulate('@\n@!@d@l@r@o@W@ @,@o@l@l@e@H..............').replace(',','').replace("'",''))
##
### print a single character of input:
##print(emulate('>.').replace(',','').replace("'",''))
##
### a simple infinite loop:
##print(emulate('[[]cckck@\n@!@d@l@r@o@W@ @,@o@l@l@e@H..............[[]]ckk][]cckck[[]]ckk').replace(',','').replace("'",''))

print("[CaKe]: ", end="")
line = sys.stdin.readline().strip('\n')
stack = []
while line != "quit":
    emulate(line, stack)
    print("[CaKe]: ", end="")
    line = sys.stdin.readline().strip('\n')
