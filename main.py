from antlr4.FileStream import FileStream
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.tree.Tree import ParseTreeWalker

from PascalLexer import PascalLexer
from PascalListener import PascalListener
from PascalParser import PascalParser


class Listener(PascalListener):
    def __init__(self):
        self.var_ls = {}
        self.spaces = 0

    def exitVariableDeclaration(self, ctx: PascalParser.VariableDeclarationContext):
        # var_type = ctx.varType()
        for i in ctx.identifierList().children[::2]:  # todo replace children
            self.var_ls[str(i)] = 'int'
        print(' ' * self.spaces, '# ', self.var_ls, sep='')

    def exitCallFunction(self, ctx: PascalParser.CallFunctionContext):
        func = str(ctx.ID())
        if func == 'readln':
            for i in ctx.parameterList().children[::2]:
                var = str(i)
                var_type = self.var_ls[var]
                if var_type == 'int':
                    print(' ' * self.spaces, '%s = int(input())' % var, sep='')
                else:
                    raise NotImplementedError(var_type)
        else:
            raise NotImplementedError(func)


def main(filename):
    lexer = PascalLexer(FileStream(filename))
    stream = CommonTokenStream(lexer)
    parser = PascalParser(stream)
    tree = parser.program()
    listener = Listener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


if __name__ == '__main__':
    # todo replace '\bVAR\b' -> 'var'
    main('test1.pas')