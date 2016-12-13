class Node(object):
    #def __str__(self):
    #    return self.printTree(0)

    def __init__(self, line):
        self.lineno = line

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, line, segments):
        super().__init__(line)
        self.segments = segments


class Declaration(Node):
    def __init__(self, line, variable_type, inits):
        super().__init__(line)
        self.variable_type = variable_type
        self.inits = inits


class Init(Node):
    def __init__(self, line, identifier, expression):
        """:arg identifier : AST.Identifier
           :arg expression : AST.Expression"""
        super().__init__(line)
        self.identifier = identifier
        self.expression = expression


class PrintInstruction(Node):
    def __init__(self, line, args):
        """:arg args : AST.ExpressionList"""
        super().__init__(line)
        self.args = args


class LabeledInstruction(Node):
    def __init__(self, line, identifier, instruction):
        """:arg identifier : string
           :arg instruction : AST.Instruction"""
        super().__init__(line)
        self.identifier = identifier
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, line, identifier, expression):
        """:arg identifier : AST.Identifier
           :arg expression : AST.Expression"""
        super().__init__(line)
        self.identifier = identifier
        self.expression = expression


class ChoiceInstruction(Node):
    def __init__(self, line, condition, instruction_true, instruction_false):
        super().__init__(line)
        self.condition = condition
        self.instruction_true = instruction_true
        self.instruction_false = instruction_false


class WhileInstruction(Node):
    def __init__(self, line, condition, instruction):
        super().__init__(line)
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, line, instruction, condition):
        super().__init__(line)
        self.instruction = instruction
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, line, expression):
        super().__init__(line)
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class CompoundInstructions(Node):
    def __init__(self, line, instructions, end_lineno):
        super().__init__(line)
        self.instructions = instructions
        self.end_lineno = end_lineno


class Const(Node):
    def __init__(self, line, value):
        super().__init__(line)
        self.value = value


# Terminal
class Integer(Const):
    pass


# Terminal
class Float(Const):
    pass


# Terminal
class String(Const):
    pass


class Identifier(Node):
    """Matches ID terminals when they are associated with a identifier
        Also, matches the production: expression -> ID"""
    def __init__(self, line, identifier):
        """:arg identifier : string"""
        super().__init__(line)
        self.identifier = identifier


class FunctionCallExpression(Node):
    def __init__(self, line, identifier, arguments):
        """:arg identifier : string
           :arg arguments : AST.ExpressionList"""
        super().__init__(line)
        self.identifier = identifier
        self.arguments = arguments


class BinExpr(Node):
    def __init__(self, line, left, op, right):
        """:arg left : AST.Expression
           :arg op : string
           :arg right : AST.Expression"""
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class FunctionDefinition(Node):
    def __init__(self, line, return_type, identifier, arguments, instructions, end_lineno):
        """:arg return_type : string
           :arg identifier : string"""
        super().__init__(line)
        self.type = return_type
        self.identifier = identifier
        self.arguments = arguments
        self.instructions = instructions
        self.end_lineno = end_lineno


class Argument(Node):
    def __init__(self, line, argument_type, argument_identifier):
        """:arg argument_type : string
           :arg argument_identifier : string"""
        super().__init__(line)
        self.argument_type = argument_type
        self.argument_identifier = argument_identifier


class Variable(Node):
    def __init__(self, line, identifier, type):
        super().__init__(line)
        self.identifier = identifier
        self.type = type
