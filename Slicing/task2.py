import sys
from antlr4 import *
from gen.CLexer import CLexer
from gen.CParser import CParser
from gen.CVisitor import CVisitor

usemap = {}
defmap = {}

def removeConstant(useset, defset):
    i = 0

    while i < len(useset):
        usetemp = []
        deftemp = []
        # if(len(defset[i])>0):
        # 	deftemp.insert(len(deftemp), defset[i])
        s = useset[i]
        # print(s)
        temp = ""
        for j in range(len(s)):
            if (s[j] != ','):
                temp += s[j]
            else:
                # print(temp)
                if (temp == "true" or temp == "false"):
                    temp = ""
                    continue
                elif (len(temp) >= 1 and (temp[0] >= '0' and temp[0] <= '9')):
                    temp = ""
                    continue
                else:
                    usetemp.insert(len(usetemp), temp)
                    temp = ""
        if (temp == "true" or temp == "false"):
            temp = ""
        elif (len(temp) >= 1 and (temp[0] >= '0' and temp[0] <= '9')):
            temp = ""
        else:
            usetemp.insert(len(usetemp), temp)
            temp = ""
        usetemp = keepdistinct(usetemp)
        # print(len(usetemp))
        if (len(usetemp) == 1):
            if (len(usetemp[0]) == 0):
                usetemp = []

        s1 = defset[i]
        # print(s)
        temp1 = ""
        for j in range(len(s1)):
            if (s1[j] != ','):
                temp1 += s1[j]
            else:
                # print(temp)
                if (temp1 == "true" or temp1 == "false"):
                    temp1 = ""
                    continue
                elif (len(temp1) >= 1 and (temp1[0] >= '0' and temp1[0] <= '9')):
                    temp1 = ""
                    continue
                else:
                    deftemp.insert(len(deftemp), temp1)
                    temp1 = ""
        if (temp1 == "true" or temp1 == "false"):
            temp1 = ""
        elif (len(temp1) >= 1 and (temp1[0] >= '0' and temp1[0] <= '9')):
            temp1 = ""
        else:
            deftemp.insert(len(deftemp), temp1)
            temp1 = ""
        deftemp = keepdistinct(deftemp)
        # print(len(usetemp))
        if (len(deftemp) == 1):
            if (len(deftemp[0]) == 0):
                deftemp = []

        usemap[i] = usetemp
        defmap[i] = deftemp
        i += 1


def keepdistinct(list1):
    unique_list = []

    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


class DotheThing:
    def __init__(self):
        #self.nodeCount = 0;
        self.useset = {}
        self.defset = {}
        self.linemap = {}
        #self.useSet = {}
        #self.textDict = {}
        self.linemap1 = {}
        #self.defSet = {}

    def getCrudeCfg(self):
      return self.crude_cfg

    def getdict(self):
        return self.linemap1

    def getVarList(self):
      return self.VarList

    def getUseset(self):
        return self.useset

    def getDefset(self):
        return self.defset

    def checkOperator(self, expr):
        if (expr == '+' or expr == '-' or expr == '*' or expr == '/' or expr == '%' or expr == '|' or expr == '&' or expr == '^'):
            return True
        return False

    def checkAlphanumeric(self, ch):
        if(ch>='a' and ch<='z'):
            return True
        elif(ch>='A' and ch<='Z'):
            return True
        elif(ch>='0' and ch<='9'):
            return True
        elif (ch == '_'):
            return True
        else:
            return False


    def handleSpaces(self, s):
        i=0
        new_str=""
        while(i<len(s)):
            if(s[i]!=' '):
                break
            i+=1
        new_str+=s[i]
        i+=1
        while(i<len(s)-1):
            if(s[i]==' '):
                if(self.checkAlphanumeric(s[i-1])==False or self.checkAlphanumeric(s[i+1])==False):
                    i+=1
                    continue
                else:
                    new_str+=s[i]
            else:
                new_str+=s[i]
            i+=1
        return new_str



    def handlefor(self, s, nodeCount):
        s1 = s[:s.index(';')]
        s = s[s.index(';') + 1:]
        s2 = s[:s.index(';')]
        s3 = s[s.index(';') + 1:]
        self.getUF(s1, nodeCount)
        # print(str(self.defset[nodeCount]) + " " + str(self.useset[nodeCount]))
        s2_1 = ""
        for x in range(len(s2)):
            if (s2[x] == '<' or s2[x] == '>' or s2[x] == '=' or s2[x] == '!'):
                s2_1 += ','
            else:
                s2_1 += s2[x]
        self.useset[nodeCount] = self.useset[nodeCount] + ',' + s2_1
        # print(self.useset[nodeCount])
        s3_1 = ""
        if (s3.count('++') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('++')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('++')]
        elif (s3.count('--') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('--')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('--')]
        elif (s3.count('+=') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('+=')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('+=')] + ',' + s3[s3.index('=') + 1:]
        elif (s3.count('-=') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('-=')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('-=')] + ',' + s3[s3.index('=') + 1:]
        elif (s3.count('*=') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('*=')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('*=')] + ',' + s3[s3.index('=') + 1:]
        elif (s3.count('/=') > 0):
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('/=')]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3[:s3.index('/=')] + ',' + s3[s3.index('=') + 1:]
        else:
            self.defset[nodeCount] = self.defset[nodeCount] + ',' + s3[:s3.index('=')]
            s3 = s3[s3.index('=') + 1:]
            s3_1 = ""
            for x in range(len(s3)):
                if (s3[x] == '+' or s3[x] == '-' or s3[x] == '*' or s3[x] == '/'):
                    s3_1 += ','
                else:
                    s3_1 += s3[x]
            self.useset[nodeCount] = self.useset[nodeCount] + ',' + s3_1

    # print(str(self.defset[nodeCount]) + " " + str(self.useset[nodeCount]))

    # self.getUF(s3, nodeCount)

    def handleBrackets(self, s):
        n_s = ""
        for i in range(len(s)):
            if (s[i] == '('):
                continue
            elif (s[i] == ')'):
                continue
            else:
                n_s += s[i]
        return n_s

    def handleprintf(self, s, nodeCount):
        t = 0
        new_str = ""
        for i in range(len(s)):
            if (t != 2):
                if (s[i] == '"'):
                    t += 1
                continue
            if (s[i] == '&'):
                continue
            if (s[i] == ')'):
                continue
            if (s[i] == ' '):
                continue
            new_str += s[i]

        self.defset[nodeCount] = ""
        # print(new_str + "   kdjbcskjdhcksjbd")
        new_str = new_str.replace(',', '', 1)
        new_new_str = ""
        for i in range(len(new_str)):
            if (new_str[i] == '['):
                new_new_str += ','
            elif (new_str[i] == ']'):
                continue
            else:
                new_new_str += new_str[i]
        self.useset[nodeCount] = self.handleBrackets(new_new_str)

    def handlescanf(self, s, nodeCount):
        t = 0
        new_str = ""
        for i in range(len(s)):
            if (t != 2):
                if (s[i] == '"'):
                    t += 1
                continue
            if (s[i] == '&'):
                continue
            if (s[i] == ')'):
                continue
            if (s[i] == ' '):
                continue
            new_str += s[i]

        new_str = new_str.replace(',', '', 1)
        new_new_str = ""
        # for i in range(len(new_str)):
        #   if(new_str[i]=='['):
        self.defset[nodeCount] = new_str
        self.useset[nodeCount] = ""

    def checkConditionalOperator(self, expr1, expr2):
        if (expr1 == '>' or expr1 == '<'):
            return True
        if (expr1 == '=' and expr2 == '='):
            return True
        if (expr1 == '!' and expr2 == '='):
            return True
        return False

    def getUF(self, st, nodeCount):
        expr = st
        if (expr.count('++') > 0):
            self.useset[nodeCount] = expr[:expr.index('++')]
            self.defset[nodeCount] = expr[:expr.index('++')]
            return
        elif (expr.count('--') > 0):
            self.useset[nodeCount] = expr[:expr.index('++')]
            self.defset[nodeCount] = expr[:expr.index('++')]
            return
        # print(expr)
        Vivek = False
        for k in range(len(expr)):
            if (self.checkOperator(expr[k]) or expr[k] == '=' or expr[k] == '>' or expr[k] == '<' or expr[k] == '!'):
                Vivek = True
                break

        if (Vivek == False):
            self.useset[nodeCount] = self.handleBrackets(expr)
            self.defset[nodeCount] = ""

        temp = ""
        t = False
        j = 0
        if (Vivek == True):
            for i in range(len(expr) - 1):
                if (self.checkConditionalOperator(expr[i], expr[i + 1])):
                    t = True
                    j = i + 1
                    # self.useset[nodeCount] = temp
                    temp += ","
                    break
                else:
                    temp += expr[i]
            # Checking for condition statement
            if (t):
                while (j < len(expr)):
                    if (expr[j] == '='):
                        j += 1
                        continue
                    if (self.checkOperator(expr[j]) or expr[j] == ';' or expr[j] == '!'):
                        # self.useset[nodeCount] = temp
                        if (self.checkOperator(expr[j - 1]) or expr[j - 1] == '!'):
                            j += 1
                            continue
                        temp += ","
                    else:
                        temp += expr[j]
                    j += 1

            self.useset[nodeCount] = self.handleBrackets(temp)
            self.defset[nodeCount] = ''

        # Checking for other expression
        temp = ""
        if (len(expr) >= 3 and t == False):
            t2 = ""
            t1 = ""
            for i in range(len(st)):
                if (expr[i] == '=' or self.checkOperator(expr[i])):
                    for j in range(len(temp)):
                        arraystats = False
                        if (temp[j] == '['):
                            arraystats = True
                            k = j + 1
                            while (True):
                                if (temp[k] == ']'):
                                    break
                                elif (self.checkOperator(temp[k])):
                                    t2 += ','
                                else:
                                    t2 += temp[k]
                                k += 1;
                            break
                        else:
                            t1 += temp[j]
                    if (arraystats == False):
                        self.defset[nodeCount] = temp
                    else:
                        self.defset[nodeCount] = t1
                        t2 += ','

                    j = i
                    break
                else:
                    temp += expr[i]
            temp = t2
            while (j < len(expr)):
                if (expr[j] == '='):
                    j += 1
                    continue
                if (self.checkOperator(expr[j])):
                    # self.useset[nodeCount] = temp
                    temp += ","
                else:
                    temp += expr[j]
                j += 1

            # print(temp)
            new_str = ""
            for i in range(len(temp)):
                if (temp[i] == '['):
                    new_str += ','
                elif (temp[i] == ']'):
                    continue
                else:
                    new_str += temp[i]
            self.useset[nodeCount] = self.handleBrackets(new_str)


    def dowork(self, argv):
        file1 = open(argv[1], "r")
        lines = [line for line in file1]
        for x in range(len(lines)):
            self.linemap1[x] = lines[x]
            self.linemap[x] = self.handleSpaces(lines[x])
            # print(self.linemap[x])
        # print(lines[x])

        for x in range(len(self.linemap)):
            if (self.linemap[x].count("main()") > 0):
                self.useset[x] = ''
                self.defset[x] = ''
            elif (self.linemap[x].count("printf") > 0):
                s = self.linemap[x][:self.linemap[x].index(';')]
                self.handleprintf(s, x)
            # print(str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("scanf") > 0):
                s = self.linemap[x][:self.linemap[x].index(';')]
                self.handlescanf(s, x)
            # print(str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("else if(") > 0):
                s = self.linemap[x][self.linemap[x].index('(') + 1:self.linemap[x].index(')')]
                # print(s)
                self.getUF(s, x)
            # print(str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("if(") > 0):
                s = self.linemap[x][self.linemap[x].index('(') + 1:self.linemap[x].index(')')]
                # print(s)
                self.getUF(s, x)
            # print(str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("while(") > 0):
                s = self.linemap[x][self.linemap[x].index('(') + 1:self.linemap[x].index(')')]
                # print(s)
                self.getUF(s, x)
            # print(str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("else") > 0 or self.linemap[x].count("}") > 0):
                self.useset[x] = ''
                self.defset[x] = ''
            elif (self.linemap[x].count("for(") > 0):
                s = self.linemap[x][self.linemap[x].index('(') + 1:self.linemap[x].index(')')]
                self.handlefor(s, x)
            # print(str(x) + " " + str(self.defset[x]) + " " + str(self.useset[x]))
            elif (self.linemap[x].count("int ") > 0 or self.linemap[x].count("float ") > 0 or self.linemap[x].count(
                    "long ") > 0 or self.linemap[x].count("double ") > 0):
                self.useset[x] = ''
                self.defset[x] = ''
            else:
                s = self.linemap[x][:self.linemap[x].index(';')]
                self.getUF(s, x)
            # print(str(x) + " " + str(self.defset[x]) + " " + str(self.useset[x]))


class MyCVisitor(CVisitor):

    def __init__(self):
        self.nodeCount = 0
        self.useSet = {}
        self.textDict = {}
        self.defSet = {}
        self.varList = []
    def getVarList(self):
        return self.VarList

    def visitDirectDeclarator(self, ctx):
        if(ctx.getChildCount()==1):
            self.VarList.append(ctx.getText())

    def visitDeclaration(self, ctx):
      if ctx.getChildCount() > 1:
    	  self.textDict[self.nodeCount] = ctx.getText()
    	  self.useSet[self.nodeCount] = ""
    	  self.defSet[self.nodeCount] = ""
    	  self.nodeCount = self.nodeCount + 1

    def visitAssignmentExpression(self, ctx):
      if ctx.getChildCount() > 1:
          #print(nodeCount, "\n", ctx.getText())                        # <------node
          self.textDict[self.nodeCount] = ctx.getText()
          self.useSet[self.nodeCount] = ""
          self.defSet[self.nodeCount] = ""
          self.nodeCount = self.nodeCount + 1

    def visitSelectionStatement(self, ctx):  # if
        if (str(ctx.children[0]) == "if"):
            self.visit(ctx.children[2])
            self.visit(ctx.children[4])
            if (ctx.getChildCount() > 5 and str(ctx.children[5]) == "else"):
                self.visit(ctx.children[6])

    def visitExpression(self, ctx):
        expr = ctx.getText()
        self.textDict[self.nodeCount] = ctx.getText()
        # print(expr)
        self.textDict[self.nodeCount] = ctx.getText()
        # self.crude_cfg = self.crude_cfg + str(self.nodeCount) + " "
        self.nodeCount = self.nodeCount + 1


class Node:
    def __init__(self, line, useset, defset, text, nxt, values):
        self.line = line
        self.useset = useset
        self.defset = defset
        self.text = text
        self.nxt = nxt
        self.data_dependence = []
        self.control_dependence = []
        self.program_dependence = []
        self.prev = []
        self.takenxt = []
        self.getnxt = []
        self.comp = []
        self.var_data_dependence = []
        self.values = values


visited = []
visited2 = []
visited3 = []
nodes = []


def find_next_loop():
    for i in range(len(nodes)):
        if i < len(nodes) - 1:
            nodes[i].nxt.append(i + 1)

    stack = []

    for i in range(len(nodes)):
        for value in nodes[i].values:
            if value == "} loop":
                opening = stack[-1]
                stack.pop()
                type = stack[-1]
                stack.pop()
                if type == "while" or type == "for":
                    nodes[opening].takenxt.append(i)
                nodes[opening].comp.append(i)
            elif value == "while" or value == "for":
                stack.append(value)
                stack.append(i)

    for i in range(len(nodes)):
        for x in nodes[i].takenxt:
            for j in nodes[x].nxt:
                nodes[i].nxt.append(j)
            nodes[x].nxt = []
            nodes[x].nxt.append(i)
        nodes[i].takenxt = []


def find_next_conditional():
    stack = []
    buffer = -1

    for i in range(len(nodes)):
        for value in nodes[i].values:
            if value == "} conditional":
                opening = stack[-1]
                stack.pop()
                type = stack[-1]
                stack.pop()
                if type == "if":
                    nodes[i].getnxt.append(opening)
                    nodes[opening].takenxt.append(i)
                    buffer = opening
                elif type == "else if":
                    nodes[i].getnxt.append(buffer)
                    nodes[buffer].takenxt.append(i)
                    nodes[opening].takenxt.append(i)
                elif type == "else":
                    nodes[buffer].takenxt.append(i)
                nodes[opening].comp.append(i)
            elif value == "if" or value == "else if" or value == "else":
                stack.append(value)
                stack.append(i)

    for i in range(len(nodes)):
        for temp in nodes[i].takenxt:
            for j in nodes[temp].nxt:
                nodes[i].nxt.append(j)

    for i in range(len(nodes)):
        for temp in nodes[i].getnxt:
            nodes[i].nxt = []
            nodes[i].nxt.append(nodes[temp].nxt[-1])

    for i in range(len(nodes)):
        if "if" in nodes[i].values:
            while len(nodes[i].nxt) > 2:
                nodes[i].nxt.pop()


def dfs(current, temp, cur_def):
    if (cur_def,temp) in visited:
        return
    visited.append((cur_def,temp))
    if temp == current:
        for x in nodes[current].prev:
            dfs(current, x, cur_def)
    else:
        if cur_def in nodes[temp].defset:
            if temp not in nodes[current].data_dependence:
                nodes[current].data_dependence.append(temp)
            nodes[current].var_data_dependence.append((cur_def,temp))
        else:
            for x in nodes[temp].prev:
                dfs(current, x, cur_def)


def post_dominator(temp, current):
    if temp == current:
        return
    if temp in visited2:
        return
    visited2.append(temp)

    for x in nodes[temp].prev:
        post_dominator(x, current)


def slicing(lineslice):
    global visited3
    visited3 = []
    processing = [lineslice]

    while len(processing):
        v = processing[0]
        del processing[0]
        if v not in visited3:
            visited3.append(v)
            for i in nodes[v].comp:
                if i not in visited3:
                    visited3.append(i)
            for i in nodes[v].program_dependence:
                processing.append(i)


def find_statement_type():
    stack = []
    for nod in nodes:
        if "for" in nod.text:
            nod.values.append("for")
            stack.append("loop")
        if "while" in nod.text:
            nod.values.append("while")
            stack.append("loop")
        if "else if" in nod.text:
            nod.values.append("else if")
            stack.append("conditional")
        elif "if" in nod.text:
            nod.values.append("if")
            stack.append("conditional")
        elif "else" in nod.text:
            nod.values.append("else")
            stack.append("conditional")

        if "}" in nod.text:
            if len(stack) > 0:
                topmost = stack[-1]
                stack.pop()
                nod.values.append("} " + topmost)


def main(argv):
    input1 = FileStream(argv[1])
    lexer = CLexer(input1)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    ast = tree.toStringTree(recog=parser)

    V = MyCVisitor()
    V.visit(tree)
    v = DotheThing()
    v.dowork(argv)

    cfg_textdict = v.getdict()

    cfg_useset = v.getUseset()

    cfg_defset = v.getDefset()
    # print("Statement corresponding to Line Nnumber")
    # print(cfg_textdict)
    # print("Line wise Useset:-")
    # print(cfg_useset)
    # print("Line wise Defset")
    # print(cfg_defset)

    removeConstant(cfg_useset, cfg_defset)

    global nodes

    # for i in range(len(usemap)):
    #   print(str(cfg_textdict[i]) + "\t" + str(usemap[i]) + "\t" + str(defmap[i]))

    for i in range(len(usemap)):
        nodes.insert(i, Node(i, usemap[i], defmap[i], cfg_textdict[i], [], []))

    global visited
    global visited2

    find_statement_type()
    find_next_loop()
    find_next_conditional()

    for x in range(len(nodes)):
        for y in nodes[x].nxt:
            nodes[y].prev.append(x)

    for current in range(len(nodes)):
        for cur_def in nodes[current].useset:
            visited = []
            dfs(current, current, cur_def)

    for current in range(len(nodes)):
        visited2 = []
        post_dominator(len(nodes) - 1, current)
        found = 0
        for x in range(len(nodes)):
            if x not in visited2:
                for y in nodes[x].prev:
                    if y in visited2:
                        nodes[current].control_dependence.append(y)
                        found = 1
                        break
        if found == 0:
            nodes[current].control_dependence.append(0)



    f = open("task2.txt", "w")

    f.write("/* The lines containing closing braces ( } ) are not a part of slice but are printed to make slice readable */\n\n")


    for lineslice in range(len(nodes)):
        for varible in nodes[lineslice].useset:
            # visited3 = []
            f.write("Slice for (" + str(lineslice)+","+varible+")\n")

            for current in range(len(nodes)):
                nodes[current].program_dependence = []
                if current == lineslice:
                    # print(str(nodes[current].var_data_dependence))
                    for y,x in nodes[current].var_data_dependence:
                        if y == varible:
                            if x not in nodes[current].program_dependence:
                                nodes[current].program_dependence.append(x)
                else:
                    for x in nodes[current].data_dependence:
                        if x not in nodes[current].program_dependence:
                            nodes[current].program_dependence.append(x)
                for x in nodes[current].control_dependence:
                    if x not in nodes[current].program_dependence:
                        nodes[current].program_dependence.append(x)

            slicing(lineslice)
            for current in range(len(nodes)):
                if current in visited3:
                    f.write(str(nodes[current].line) + ": " + nodes[current].text)
            f.write(str(nodes[len(nodes)-1].line) + ": " + nodes[len(nodes)-1].text + "\n\n")

    # for x in range(len(nodes)):
    #     print(str(x) + ": " + str(nodes[x].nxt) + " " + str(nodes[x].values))

    # print("/* Take reference of line numbers from following indexed code if result is incorrect */")
    #
    # for x in range(len(nodes)):
    #     print(str(x) + ": " + nodes[x].text)


# print(argv[1])
# file1 = open(argv[1], "r")
# lines = [line for line in file1]
# for x in range(len(lines)):
#   print(lines[x])


if __name__ == '__main__':
    main(sys.argv)