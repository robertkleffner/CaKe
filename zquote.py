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
    elif c == 'z':
        # [B] [A] z == [[][][[][][]zz[][]zz]z] [[][]zz] [B] A
        # LOLWAT
        # In terms of cake and k:
        # [B] [A] z == [cake] [k] A
        # can be expressed as z == [zap [cake] [k]] dip i
        # So essentially, it's function is to place [cake] and [k] on the
        # stack, move [B] to the front, and then execute [A].
        # Not that hard really.
        #
        # Thanks again to Brent Kerby here, who showed how my initial
        # instinct (translating Fokker's X into a concatenative combinator)
        # was incorrect, and for providing a rather nice single combinator
        # basis in terms of his cake and k!

        a = stack.pop()
        stack.pop()

        stack.append(['c'])
        stack.append(['k'])
        if isinstance(a, list):
            for i in a[::-1]:
                if isinstance(i, list):
                    quotesToPush.append(i)
                    instructions.insert(0, 's')
                else:
                    instructions.insert(0, i)
        else:
            raise Exception("Guess that didn't work!")
    elif c == 's':
        stack.append(quotesToPush.pop())
    else:
        stack.append(c)

### push combinator x:  == x
##print(emulate('[]').replace(',','').replace("'",''))
##print(emulate('[k]').replace(',','').replace("'",''))
##print(emulate('[c]').replace(',','').replace("'",''))
##
# k: [[]] [[]] == []
emulate('[[]][[]][][]zz',[])

# c: [[]] [[]] == [[[]] []] [[] [[]]]
emulate('[[]][[]][][][[][][]zz[][]zz]z',[])

# zap: [[]] == 
emulate('[[]][][][]zz',[])

# dip: [[]] [[]] == [] [[]]
emulate('[[]][[]][][][[][][]zz[][]zz]z[][]zz',[])

# cons: [[]] [[]] == [[[]] []]
emulate('[[]][[]][][][[][][]zz[][]zz]z[][][]zz',[])

# unit: [] == [[]]
emulate('[][][][][[][][]zz[][]zz]z[][][]zz',[])

# i: [[]] == []
emulate('[[]][[]][][][[][][]zz[][]zz]z[][]zz[][]zz',[])

# dup: [] == [] []
emulate('[][][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz',[])

# hello world:
emulate('@\n@!@d@l@r@o@W@ @,@o@l@l@e@H..............',[])

# print a single character of input:
emulate('>.',[])

# a simple infinite loop:
emulate('[[][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz@\n@!@d@l@r@o@W@ @,@o@l@l@e@H..............[[]][][][[][][]zz[][]zz]z[][]zz[][]zz][][][][[][][]zz[][]zz]z[][][[][][]zz[][]zz]z[][]zz[][][[][][]zz[][]zz]z[][]zz[[]][][][[][][]zz[][]zz]z[][]zz[][]zz',[])

print("[CaKe]: ", end="")
line = sys.stdin.readline().strip('\n')
stack = []
while line != "quit":
    emulate(line, stack)
    print("[CaKe]: ", end="")
    line = sys.stdin.readline().strip('\n')
