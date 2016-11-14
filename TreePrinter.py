import AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    @addToClass(AST.Program)
    def printTree(self, space=0):
        return self.segments.printTree(space)

    @addToClass(AST.Segments)
    def printTree(self, space=0):
        return "".join(map(lambda e: e.printTree(space), self.segments))

    @addToClass(AST.Segment)
    def printTree(self, space=0):
        return self.content.printTree(space)

    # TODO -------- Is it Correct Now ? --------
    @addToClass(AST.Declarations)
    def printTree(self, space):
        return "".join(map(lambda e: e.printTree(space), self.declarations))

    @addToClass(AST.Declaration)
    def printTree(self, space=0):
        return ("| " * space + "DECL\n" +
                self.inits.printTree(space + 1))

    @addToClass(AST.Inits)
    def printTree(self, space=0):
        return "".join(map(lambda e: e.printTree(space), self.inits))

    @addToClass(AST.Init)
    def printTree(self, space=0):
        return ("| " * space + "=\n" +
                "| " * (space + 1) + str(self.variable) + "\n" +
                self.expression.printTree(space + 1))

    @addToClass(AST.Instructions)
    def printTree(self, space=0):
        return "".join(map(lambda e: e.printTree(space), self.instructions))

    @addToClass(AST.PrintInstruction)
    def printTree(self, space=0):
        return ("| " * space + "PRINT\n" +
                self.args.printTree(space))

    @addToClass(AST.LabeledInstruction)
    def printTree(self, space=0):
        return ("| " * space + "LABEL\n" +
                "| " * (space + 1) + str(self.identifier) + "\n" +
                self.instruction.printTree(space))

    @addToClass(AST.Assignment)
    def printTree(self, space=0):
        return ("| " * space + "=\n" +
                "| " * (space + 1) + str(self.variable) + "\n" +
                self.expression.printTree(space + 1))

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, space=0):
        if self.instruction_false is None:
            return ("| " * space + "IF\n" +
                    self.condition.printTree(space + 1) + self.instruction_true.printTree(space + 1))
        else:
            return ("| " * space + "IF\n" +
                    self.condition.printTree(space + 1) + self.instruction_true.printTree(space + 1) +
                    "| " * space + "ELSE\n" +
                    self.instruction_false.printTree(space + 1))

    @addToClass(AST.WhileInstruction)
    def printTree(self, space=0):
        return ("| " * space + "WHILE\n" +
                self.condition.printTree(space + 1) + self.instruction.printTree(space))

    @addToClass(AST.RepeatInstruction)
    def printTree(self, space=0):
        return ("| " * space + "REPEAT\n" +
                self.instructions.printTree(space) +
                "| " * (space + 1) + "UNTIL\n" +
                self.condition.printTree(space + 2))

    @addToClass(AST.ReturnInstruction)
    def printTree(self, space=0):
        return ("| " * space + "RETURN\n" +
                self.expression.printTree(space + 1))

    @addToClass(AST.BreakInstruction)
    def printTree(self, space=0):
        return "| " * space + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, space=0):
        return "| " * space + "CONTINUE\n"

    @addToClass(AST.CompoundInstruction)
    def printTree(self, space=0):
        if self.instructions is None:
            return ""
        else:
            return self.instructions.printTree(space + 1)

    # TODO -------- Is it Correct Now ? --------
    @addToClass(AST.CompoundSegments)
    def printTree(self, space):
        return "".join(map(lambda e: e.printTree(space), self.segments))

    # TODO -------- IS IT NECESSARY ??? --------
    @addToClass(AST.CompoundSegment)
    def printTree(self, space):
        pass

    # TODO -------- IS IT NECESSARY ??? --------
    @addToClass(AST.Condition)
    def printTree(self, space):
        pass

    @addToClass(AST.Const)
    def printTree(self, space):
        return ("| " * space + str(self.value) + "\n")

    # TODO --------  REMOVE IT ??? --------
    @addToClass(AST.Integer)
    def printTree(self, space):
        pass

    # TODO --------  REMOVE IT ??? --------
    @addToClass(AST.Float)
    def printTree(self, space):
        pass

    # TODO --------  REMOVE IT ??? --------
    @addToClass(AST.String)
    def printTree(self, space):
        pass

    # TODO -------- IS IT NECESSARY ??? --------
    @addToClass(AST.Expression)
    def printTree(self, space):
        pass

    @addToClass(AST.BinExpr)
    def printTree(self, space=0):
        return ("| " * space + self.op + "\n" +
                self.left.printTree(space + 1) +
                self.right.printTree(space + 1))

    @addToClass(AST.BracketExpression)
    def printTree(self, space=0):
        return self.expression.printTree(space)

    @addToClass(AST.FunctionCallExpression)
    def printTree(self, space):
        return ("| " * space + "FUNCALL\n" +
                "| " * (space + 1) + str(self.identifier) + "\n" +
                self.arguments.printTree(space + 1))

    @addToClass(AST.ExpressionList)
    def printTree(self, space=0):
        return "".join(map(lambda e: e.printTree(space + 1), self.expressions))

    # TODO -------- Is it Correct Now ? --------
    @addToClass(AST.FunctionDefinitions)
    def printTree(self, space):
        return "".join(map(lambda e: e.printTree(space), self.function_definitions))

    @addToClass(AST.FunctionDefinition)
    def printTree(self, space=0):
        return ("| " * space + "FUNDEF\n" +
                "| " * (space + 1) + str(self.identifier) + "\n" +
                "| " * (space + 2) + "RET " + str(self.type) + "\n" +
                self.arguments.printTree(space + 1) +
                self.instructions.printTree(space))

    @addToClass(AST.ArgumentsList)
    def printTree(self, space=0):
        return "".join(map(lambda e: e.printTree(space + 1), self.arguments))

    @addToClass(AST.Argument)
    def printTree(self, space=0):
        return "| " * space + "ARG " + self.argument_identifier + "\n"

    # TODO -------- IS IT NECESSARY ??? --------
    @addToClass(AST.Variable)
    def printTree(self, space):
        pass
