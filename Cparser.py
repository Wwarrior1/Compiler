import AST as ast
from scanner import Scanner


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : segments"""
        if len(p) == 2:
            p[0] = ast.Program(p.lineno(1), p[1])

    # list
    def p_segments(self, p):
        """segments : segments segment
                    | """
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        elif len(p) == 1:
            p[0] = []

    # 1-1
    def p_segment(self, p):
        """segment : declaration
                   | function_definition
                   | instruction """
        if len(p) == 2:
            p[0] = p[1]

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            p[0] = ast.Declaration(p.lineno(1), p[1], p[2])

    # list
    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        elif len(p) == 2:
            p[0] = [p[1]]

    def p_init(self, p):
        """init : ID '=' expression """
        if len(p) == 4:
            p[0] = ast.Init(p.lineno(1), p[1], p[3])

    # # list
    # def p_instructions(self, p):
    #     """instructions : instructions instruction
    #                     | instruction """
    #     if len(p) == 3:
    #         p[0] = p[1]
    #         p[0].append(p[2])
    #     elif len(p) == 2:
    #         p[0] = [p[1]]

    # 1-1
    def p_instruction(self, p):
        """instruction : print_instruction
                       | labeled_instruction
                       | assignment
                       | choice_instruction
                       | while_instruction
                       | repeat_instruction
                       | return_instruction
                       | break_instruction
                       | continue_instruction
                       | compound_instructions
                       | expression ';' """
        if len(p) == 2 or len(p) == 3:
            p[0] = p[1]

    def p_print_instruction(self, p):
        """print_instruction : PRINT expr_list ';'
                             | PRINT error ';' """
        if len(p) == 4:
            p[0] = ast.PrintInstruction(p.lineno(1), p[2])

    def p_labeled_instruction(self, p):
        """labeled_instruction : ID ':' instruction """
        p[0] = ast.LabeledInstruction(p.lineno(1), p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        if len(p) == 5:
            identifier = ast.Identifier(p.lineno(1), p[1])
            p[0] = ast.Assignment(p.lineno(1), identifier, p[3])

    def p_choice_instruction(self, p):
        """choice_instruction : IF '(' condition ')' instruction  %prec IFX
                              | IF '(' condition ')' instruction ELSE instruction
                              | IF '(' error ')' instruction  %prec IFX
                              | IF '(' error ')' instruction ELSE instruction """
        if len(p) >= 6:
            p[0] = ast.ChoiceInstruction(p.lineno(1), p[3], p[5], None)
        if len(p) == 8:
            p[0] = ast.ChoiceInstruction(p.lineno(1), p[3], p[5], p[7])

    def p_while_instruction(self, p):
        """while_instruction : WHILE '(' condition ')' instruction
                             | WHILE '(' error ')' instruction """
        if len(p) == 6:
            p[0] = ast.WhileInstruction(p.lineno(1), p[3], p[5])

    def p_repeat_instruction(self, p):
        """repeat_instruction : REPEAT instruction UNTIL condition ';' """
        if len(p) == 6:
            p[0] = ast.RepeatInstruction(p.lineno(1), p[2], p[4])

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression ';' """
        if len(p) == 4:
            p[0] = ast.ReturnInstruction(p.lineno(1), p[2])

    def p_break_instruction(self, p):
        """break_instruction : BREAK ';' """
        if len(p) == 3:
            p[0] = ast.BreakInstruction(p.lineno(1))

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE ';' """
        if len(p) == 3:
            p[0] = ast.ContinueInstruction(p.lineno(1))

    def p_compound_instructions(self, p):
        """compound_instructions : '{' compound_segments '}' """
        if len(p) == 4:
            p[0] = ast.CompoundInstructions(p.lineno(1), p[2])

    # list
    def p_compound_segments(self, p):
        """compound_segments : compound_segments compound_segment
                             | """
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        elif len(p) == 1:
            p[0] = []

    # 1-1
    def p_compound_segment(self, p):
        """compound_segment : declaration
                            | instruction """
        if len(p) == 2:
            p[0] = p[1]

    # 1-1
    def p_condition(self, p):
        """condition : expression"""
        if len(p) == 2:
            p[0] = p[1]

    # 1-1
    def p_const(self, p):
        """const : integer
                 | float
                 | string """
        if len(p) == 2:
            p[0] = p[1]

    def p_integer(self, p):
        """integer : INTEGER"""
        if len(p) == 2:
            p[0] = ast.Integer(p.lineno(1), p[1])

    def p_float(self, p):
        """float : FLOAT"""
        if len(p) == 2:
            p[0] = ast.Float(p.lineno(1), p[1])

    def p_string(self, p):
        """string : STRING"""
        if len(p) == 2:
            p[0] = ast.String(p.lineno(1), p[1])

    def p_identifier_expression(self, p):
        """identifier_expression : ID"""
        p[0] = ast.Identifier(p.lineno(1), p[1])

    def p_function_call_expression(self, p):
        """function_call_expression : ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        p[0] = ast.FunctionCallExpression(p.lineno(1), p[1], p[3])

    # 1-1
    def p_expression(self, p):
        """expression : binary_expression
                      | '(' expression ')'
                      | '(' error ')'
                      | identifier_expression
                      | function_call_expression
                      | const """
        if len(p) == 4:
            if p[1] == '(':
                p[0] = p[2]
        else:
            p[0] = p[1]

    def p_binary_expression(self, p):
        """binary_expression : expression '+' expression
                             | expression '-' expression
                             | expression '*' expression
                             | expression '/' expression
                             | expression '%' expression
                             | expression '|' expression
                             | expression '&' expression
                             | expression '^' expression
                             | expression AND expression
                             | expression OR expression
                             | expression SHL expression
                             | expression SHR expression
                             | expression EQ expression
                             | expression NEQ expression
                             | expression '>' expression
                             | expression '<' expression
                             | expression LE expression
                             | expression GE expression """
        if len(p) == 4:
            p[0] = ast.BinExpr(p.lineno(2), p[1], p[2], p[3])

    def p_function_definition(self, p):
        """function_definition : TYPE ID '(' args_list_or_empty ')' compound_instructions """
        if len(p) == 7:
            p[0] = ast.FunctionDefinition(p.lineno(1), p[1], p[2], p[4], p[6])

    # list
    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        elif len(p) == 2:
            p[0] = [p[1]]

    def p_arg(self, p):
        """arg : TYPE ID """
        if len(p) == 3:
            p[0] = ast.Argument(p.lineno(1), p[1], p[2])

    # list
    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    # list
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        elif len(p) == 2:
            p[0] = [p[1]]

    # 1-1
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 1:
            p[0] = []
