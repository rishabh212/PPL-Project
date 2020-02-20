import sys
#from inspect import signature
from antlr4 import *
from gen.CLexer import CLexer
#from CListener import CListener
from gen.CParser import CParser
from gen.CVisitor import CVisitor


class MyCVisitor(CVisitor):
    pass
    '''  def __init__(self):
        self.VarList=[]

    def getVarList(self):
        return self.VarList

    def visitDirectDeclarator(self, ctx):
        if(ctx.getChildCount()==1):
            self.VarList.append(ctx.getText())
            '''

class MyCVisitor2(CVisitor):
    def __init__(self):
        self.nodeCounter = 1
        self.textdict={}
        self.crude_cfg = ""
        self.VarList = []


    def getCrudeCfg(self):
        return self.crude_cfg

    def getdict(self):
        return self.textdict

    def getVarList(self):
        return self.VarList



    def visitTranslationUnit(self, ctx):    # functions
        if(ctx.getChildCount() > 1):
            pass
        else:
            # print("***")
            self.crude_cfg = self.crude_cfg + "[ "
            if (ctx.children[0].children[0].children[1].children[0].getChildCount() > 3):
                self.crude_cfg = self.crude_cfg  + str(self.nodeCounter)
                self.nodeCounter = self.nodeCounter + 1
            else:
                self.crude_cfg = self.crude_cfg + " 0"
        self.crude_cfg = self.crude_cfg + " [ "
        self.visit(ctx.children[0])
        self.crude_cfg = self.crude_cfg + " ]"
        self.crude_cfg = self.crude_cfg + " ]\n"

    def visitSelectionStatement(self, ctx):     #if
        if (str(ctx.children[0]) == "if"):
            #print(self.nodeCounter, "\n", ctx.getText())
            self.crude_cfg = self.crude_cfg + "[ if_"
            self.visit(ctx.children[2])
            self.crude_cfg = self.crude_cfg + "[ "
            self.visit(ctx.children[4])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + "[ "
            if (ctx.getChildCount()>5 and str(ctx.children[5]) == "else"):
                self.visit(ctx.children[6])
            self.crude_cfg = self.crude_cfg + " ] "
            self.crude_cfg = self.crude_cfg + " ] "

    def visitDeclaration(self, ctx):
        if ctx.getChildCount() > 1:
            self.textdict[self.nodeCounter] = ctx.getText()
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.nodeCounter = self.nodeCounter+1


    def visitDirectDeclarator(self, ctx):
        if(ctx.getChildCount()==1):
            self.VarList.append(ctx.getText())



    def visitAssignmentExpression(self, ctx):
        if ctx.getChildCount() > 1:
           #print(self.nodeCounter, "\n", ctx.getText())                        # <------node
            self.textdict[self.nodeCounter] = ctx.getText()
            self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
            self.nodeCounter = self.nodeCounter + 1

    def visitExpression(self, ctx):
        #if ctx.getChildCount() > 1:
        #print(self.nodeCounter, "\n", ctx.getText())                        # <------node
        self.textdict[self.nodeCounter] = ctx.getText()
        self.crude_cfg = self.crude_cfg + str(self.nodeCounter) + " "
        self.nodeCounter = self.nodeCounter + 1







def main(argv):
    input = FileStream(argv[1])
    lexer = CLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()
    ast = tree.toStringTree(recog=parser)
    # print(ast)


    #v = MyCVisitor()
    #v.visit(tree)
    #print(v.getVarList())


    v2 = MyCVisitor2()
    v2.visit(tree)

    #print(v2.getVarList())

    cfg_string = v2.getCrudeCfg()
    print("CFG:-")
    print(cfg_string)

    cfg_textdict = v2.getdict()
    # print(cfg_textdict)




if __name__ == '__main__':
    main(sys.argv)

