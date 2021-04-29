import sys

# Basic Block class
class BasicBlock:
    def __init__(self , name ,start , end):
        self.name = name
        self.start = start
        self.end = end
        self.connections = set()
        self.incoming = set()
        self.code = []
    def addConnection(self , name):
        self.connection.append(name)
# Partition function to find leaders, gotos ,Code and lines of code
def Partition(filename):
    Leaders = set()
    Leaders.add(1)
    sc = 0
    gotos = {}
    code = []
    with open(filename , mode = 'r' , encoding = 'utf-8') as file:
        # statement type 1. a = b+c
        # statement type 2. if cond then goto 1
        for statement in file:
            sc +=1
            code.append(statement)
            if statement.find('goto') != -1:
                if statement.find('if') != -1:
                    statement = statement.split()
                    leader = int(statement[-1])
                    Leaders.add(leader)
                    current = int(statement[0][:-1])
                    Leaders.add(current+1)
                    if current not in gotos:
                        gotos[current] = [False , set()]
                    gotos[current][1].add(leader)
                    gotos[current][1].add(current+1)
                else:
                    statement = statement.split()
                    leader = int(statement[-1])
                    Leaders.add(leader)
                    current = int(statement[0][:-1])
                    Leaders.add(current+1)
                    if current not in gotos:
                        gotos[current] = [True , set()]
                    gotos[current][1].add(leader)
    if sc+1 in Leaders:
        Leaders.remove(sc+1)
    Leaders = list(sorted(Leaders))

    for i,e in enumerate(Leaders):
        if e not in gotos:
            gotos[e] = [False , set()]
        if i+1 < len(Leaders):
            if gotos[e][0]==False:
                gotos[e][1].add(Leaders[i+1])
        else:
            gotos[e][1].add('END')
    for e in gotos:
        if sc+1 in gotos[e]:
            gotos[e][1].remove(sc+1)
            gotos[e][1].add('END')
    new_gotos = {}
    for e in gotos:
        new_gotos[e] = gotos[e][1]
    return  Leaders, new_gotos , sc , code

# Function to find the basic block containing the given line
def findBasicBlock(Blocks , line):
    if line == 'END':
        return 'END'
    for e in Blocks:
        block = Blocks[e]
        if block.start <= line <= block.end:
            return e
    return 'END'


# Function to calculate the distance from the start of each basic block
def distanceFromStart(BuildingBlock):
    a = None
    for e in BuildingBlock['START'].connections:
        a = e
    queue = [(a , 1)]
    Distances = {}
    BlockDistance = {}
    visited = set()
    while queue:
        bb , d = queue.pop(0)
        if d not in Distances:
            Distances[d] = set()
        Distances[d].add(bb.name)
        BlockDistance[bb.name] = d
        for e in bb.connections:
            if e.name not in visited:
                visited.add(e.name)
                queue.append([e , d+1])
    for bl in BasicBlocks:
        if bl not in BlockDistance:
            BlockDistance[bl] = float('inf')
    return Distances , BlockDistance





#  Correct Checked
# Function to find the dominators of all the basic blocks
def findDominators(BasicBlocks):
    distances , blockDistances = distanceFromStart(BasicBlocks)
    dist_keys = sorted(distances)
    Dominators = {}
    for e in dist_keys:
        blocks = distances[e]
        # print(blocks)
        for block_name in blocks:
            Dominators[block_name] = set()
            Dominators[block_name].add(block_name)
            s = set(BasicBlocks.keys())
            lst = BasicBlocks[block_name].incoming
            for inc_name in BasicBlocks[block_name].incoming:
                if inc_name != 'START':
                    if blockDistances[inc_name] < e:
                        s = s.intersection(Dominators[inc_name])
                else:
                    s = set()
            Dominators[block_name] = Dominators[block_name].union(s)
    return Dominators



    for block_name in BasicBlocks:
        Dominators[block_name] = set()
        Dominators[block_name].add(block_name)
        s = set(BasicBlocks.keys())
        for inc_name in BasicBlocks[block_name].incoming:
            if inc_name != 'FIRST':
                s.intersection(Dominators[inc_name])
        Dominators[block_name] = Dominators[block_name].union(s)
    return Dominators


# Function to show the code
def showCode(BasicBlocks):
    print("\n **************************. Printing Code. **************************\n")
    for block_name in BasicBlocks:
        block = BasicBlocks[block_name]
        print('\t\t\t\t------- Basic Block' , block.name)
        for e in block.code:
            stmt = e[0].split()
            stmt = " ".join(stmt)
            print(stmt)


# Function to find a dead code inside a basic block
def findDeadCodeinBlock(block):
    nextUse = {}
    for e in block.code[::-1]:
        stmt = e[0].split()
        if len(stmt) == 6:
            op = stmt[1]

            if op not in nextUse:
                nextUse[op] = [False , -1]
            elif nextUse[op][0]==False:
                e[1] = True
                nextUse[op] = [False , -1]
            else:
                nextUse[op] = [False , -1]
            
            op1 = stmt[3]
            if op1.isnumeric() == False:
                nextUse[op1] = [True , int(stmt[0][:-1])]
            
            op2 = stmt[5]

            if op2.isnumeric() == False:
                nextUse[op2] = [True , int(stmt[0][:-1])]
        if len(stmt) == 4 :
            op = stmt[1]
            if op not in nextUse:
                nextUse[op] = [False , -1]
            elif nextUse[op][0]==False:
                e[1] = True
                nextUse[op] = [False , -1]
            else:
                nextUse[op] = [False , -1]
            
            op1 = stmt[3]
            if op1.isnumeric() == False:
                nextUse[op1] = [True , int(stmt[0][:-1])]
    return nextUse



# Function to find Unreachable code
def unreachableCode(BasicBlock):
    dead_block = set()
    for block_name in BasicBlock:
        if len(BasicBlock[block_name].incoming) == 0:
            for e in BasicBlock[block_name].code:
                e[1] = True
                dead_block.add(BasicBlock[block_name])
    print("\n\n Unreachable Code \n\n")
    for block in dead_block:
        print('\t\t\t\t------------- Unreachable Basic Block' , block.name)
        for e in block.code:
            stmt = e[0].split()
            stmt = [' U.R --> '] + stmt
            stmt = " ".join(stmt)
            print(stmt)



# Function to show the dead code inside the basic blocks
def showDeadCode(BasicBlock):
    print("\n **************************. Showing Dead Code. **************************\n")
    blocks = []
    for block_name in BasicBlock:
        if len(BasicBlock[block_name].incoming) == 0:
            for e in BasicBlock[block_name].code:
                e[1] = True
                blocks.append([BasicBlock[block_name], True])
        else:
            blocks.append([BasicBlock[block_name] , False])

    for e in blocks:
        if e[1] == False:
            findDeadCodeinBlock(e[0])
            print('\t\t\t\t------- Basic Block' , e[0].name)
            for cd in e[0].code:
                stmt = cd[0].split()
                if cd[1] == True:
                    stmt = ['* Dead Code --> '] + stmt
                stmt = " ".join(stmt)
                print(stmt)
        else:
            print('\t\t\t\t------- Basic Block' , e[0].name)
            for cd in e[0].code:
                stmt = cd[0].split()
                stmt = [' Dead Code --> '] + stmt
                stmt = " ".join(stmt)
                print(stmt)

    

# Function to find a back edge
def findBackEdge(block , dominators):
    lst = []
    for e in block.connections:
        if e.name in dominators:
            lst.append(e.name)
    return lst


# Function to find the natural loops of a basic block
def findNaturalLoopOfBlock(block , dominators , BasicBlocks):
    lst = findBackEdge(block , dominators)
    if len(lst)>0:
        for block_name in lst:
            print("Natural Loop from Basic Block" , block_name , "are : " , end='\n\t\t')
            body = {block_name}
            stk = [block.name]
            while stk:
                bne = BasicBlocks[stk.pop()]
                if bne.name not in body:
                    body.add(bne.name)
                    for pred in bne.incoming:
                        stk.append(pred)
            for loop_name in body:
                print('BasicBlock : ' , loop_name , end = " --> ")
            print('BasicBlock : ' , block_name)
                        

# Function to find all the natural loops
def findNaturalLoops(BasicBlocks):
    print('\n\n Printing Natural Loops ' , end = '\n\n\t')
    dominators = findDominators(BasicBlocks)
    for block_name in BasicBlocks:
        if block_name != "START" and block_name != "END" and block_name in dominators:
            findNaturalLoopOfBlock(BasicBlocks[block_name] , dominators[block_name] , BasicBlocks)


# Function to generate basic blocks and control flow graph
def generateBuildingBlocks(filename):
    leaders , gotos , lines , code = Partition(filename)
    BuildingBlocks = {}
    BuildingBlocks['START'] = BasicBlock('START' , -1 , -1)
    BuildingBlocks['END'] = BasicBlock('END' , -1 , -1)

    for i,e in enumerate(leaders):
        start = e
        end = lines
        if i+1 < len(leaders):
            end = leaders[i+1]-1
        block = BasicBlock(i+1 , start , end)
        for c in code[start-1:end]:
            block.code.append([c , False])
        BuildingBlocks[i+1] = block
    
    for e in gotos:
        # print(e)
        block1_name = findBasicBlock(BuildingBlocks , e)
        block1 = BuildingBlocks[block1_name]
        for ee in gotos[e]:
            # print(ee , type(ee))
            block_name = findBasicBlock(BuildingBlocks , ee)
            neghibour = BuildingBlocks[block_name]
            block1.connections.add(neghibour)
            neghibour.incoming.add(block1.name)
        
    b1 = BuildingBlocks[findBasicBlock(BuildingBlocks , 1)]
    b2 = BuildingBlocks['START']
    b2.connections.add(b1)
    b1.incoming.add(b2.name)
    
    return BuildingBlocks

#  trivial function to print information about basic blocks
def printBasicBlocks(BasicBlocks):
    print("\n\nPrinting Information About Basic Blocks\n")
    for e in BasicBlocks:
        print(" ** Basic Block" , BasicBlocks[e].name , "**")
        print('\t Start : ' , BasicBlocks[e].start)
        print('\t End : ' , BasicBlocks[e].end)

# Function to Print in the control flow graph
def printControlFlow(BasicBlocks):
    print("\n\nPrinting Control Flow Of Basic Blocks \n")
    for e in BasicBlocks:
        if e == 'END':
            continue
        b1 = BasicBlocks[e]
        print(" Basic Block name : " , b1.name , ' ----->  ' , end='')
        connections = list(b1.connections)
        for i in range(len(connections)):
            if i== len(connections)-1:
                break
            print(' Basic Block : ' , connections[i].name , end = ' ,')
        print(' Basic Block : ' , connections[-1].name)










if len(sys.argv) != 2 :
    print('Usage python3 assignment3.py [filename]')
    sys.exit()
filename = sys.argv[1]

BasicBlocks = generateBuildingBlocks(filename)

printBasicBlocks(BasicBlocks)
printControlFlow(BasicBlocks)


print("\n *** Finding Dominators *** \n")
dominators = findDominators(BasicBlocks)
print(dominators)



showCode(BasicBlocks)
unreachableCode(BasicBlocks)

showDeadCode(BasicBlocks)


findNaturalLoops(BasicBlocks)



