from typing import Any, Optional
from lexer import Token, TokenType, tokenize
from ast import (
    ASTNode, ProgramNode, BlockNode, FunctionNode, ParameterNode,
    IdentifierNode, NumberNode, StringNode, BooleanNode,
    BinaryNode, UnaryNode, GroupingNode, AssignmentNode, CallNode,
    IfNode, WhileNode, ForNode, ReturnNode, PrintNode, TypeNode,
    ListNode, DictNode, IndexNode, TryNode, ImportNode,
    BreakNode, ContinueNode, PassNode, NodeType, dump_ast
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def check_next(self, type: TokenType) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == type
    
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str = None) -> Token:
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"{message or 'Expected'} {type} at {self.peek().line}:{self.peek().column}")
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE:
                return
            if self.check(TokenType.FN) or self.check(TokenType.IF) or self.check(TokenType.WHILE):
                return
            self.advance()
    
    def parse(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            statements.append(self.statement())
        return ProgramNode(statements)
    
    def statement(self) -> ASTNode:
        if self.match(TokenType.FN):
            return self.function()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.TRY):
            return self.try_statement()
        if self.match(TokenType.BREAK):
            return BreakNode(self.previous().line, self.previous().column)
        if self.match(TokenType.CONTINUE):
            return ContinueNode(self.previous().line, self.previous().column)
        if self.match(TokenType.PRINT, TokenType.TYPE):
            return self._parse_builtin_call(self.previous())
        if self.match(TokenType.IMPORT):
            return self.import_statement()
        return self.expression_statement()
    
    def function(self) -> FunctionNode:
        name_token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        name = name_token.value
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        parameters = self.parameters()
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        self.consume(TokenType.LPAREN, "Expected '(' for function body")
        body = self.block()
        self.consume(TokenType.RPAREN, "Expected ')' to close function body")
        return FunctionNode(name, parameters, body, name_token.line, name_token.column)
    
    def parameters(self) -> list[ParameterNode]:
        params = []
        if not self.check(TokenType.RPAREN):
            while True:
                param_token = self.consume(TokenType.IDENTIFIER, "Expected parameter name")
                default_value = None
                if self.match(TokenType.EQUAL):
                    default_value = self.expression()
                params.append(ParameterNode(param_token.value, default_value))
                if not self.match(TokenType.COMMA):
                    break
        return params
    
    def block(self) -> BlockNode:
        statements = []
        while not self.check(TokenType.RPAREN) and not self.is_at_end():
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            if self.check(TokenType.RPAREN):
                break
            statements.append(self.statement())
        return BlockNode(statements)
    
    def if_statement(self) -> IfNode:
        self.consume(TokenType.LPAREN, "Expected '(' after if")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        self.consume(TokenType.LPAREN, "Expected '(' for if body")
        while self.match(TokenType.NEWLINE):
            pass
        then_branch = self.block()
        self.consume(TokenType.RPAREN, "Expected ')' to close if body")
        
        elif_branches = []
        while self.match(TokenType.ELIF):
            self.consume(TokenType.LPAREN, "Expected '(' after elif")
            elif_condition = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after elif condition")
            self.consume(TokenType.LPAREN, "Expected '(' for elif body")
            while self.match(TokenType.NEWLINE):
                pass
            elif_body = self.block()
            self.consume(TokenType.RPAREN, "Expected ')' to close elif body")
            elif_branches.append((elif_condition, elif_body))
        
        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LPAREN, "Expected '(' for else body")
            while self.match(TokenType.NEWLINE):
                pass
            else_branch = self.block()
            self.consume(TokenType.RPAREN, "Expected ')' to close else body")
        
        return IfNode(condition, then_branch, elif_branches, else_branch)
    
    def while_statement(self) -> WhileNode:
        self.consume(TokenType.LPAREN, "Expected '(' after while")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        self.consume(TokenType.LPAREN, "Expected '(' for while body")
        while self.match(TokenType.NEWLINE):
            pass
        body = self.block()
        self.consume(TokenType.RPAREN, "Expected ')' to close while body")
        return WhileNode(condition, body)
    
    def for_statement(self) -> ForNode:
        variable = self.consume(TokenType.IDENTIFIER, "Expected loop variable").value
        self.consume(TokenType.IN, "Expected 'in'")
        iterable = self.expression()
        # For loop uses single statement, not block
        stmt = self.statement()
        return ForNode(variable, iterable, BlockNode([stmt]))
    
    def return_statement(self) -> ReturnNode:
        value = None
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.RPAREN):
            value = self.expression()
        return ReturnNode(value)
    
    def try_statement(self) -> TryNode:
        self.consume(TokenType.LPAREN, "Expected '(' after try")
        while self.match(TokenType.NEWLINE):
            pass
        try_body = self.block()
        self.consume(TokenType.RPAREN, "Expected ')' to close try body")
        if not self.match(TokenType.CATCH):
            raise SyntaxError(f"Expected 'catch' at {self.peek().line}:{self.peek().column}")
        variable = "error"
        if self.check(TokenType.IDENTIFIER):
            variable = self.advance().value
        print(f"TRY: about to consume LPAREN, current is {self.peek().type.name} at {self.peek().line}:{self.peek().column}")
        if not self.check(TokenType.LPAREN):
            print(f"TRY: ERROR - not at LPAREN!")
            # List next few tokens
            for i in range(5):
                idx = self.current + i
                if idx < len(self.tokens):
                    print(f"  tokens[{idx}] = {self.tokens[idx].type.name}")
        else:
            self.advance()
            print(f"TRY: consumed LPAREN, now at {self.peek().type.name}")
        while self.match(TokenType.NEWLINE):
            pass
        catch_body = self.block()
        self.consume(TokenType.RPAREN, "Expected ')' to close catch body")
        return TryNode(try_body, catch_body, variable)
    
    def import_statement(self) -> ImportNode:
        # Check if it's import("path") syntax
        if self.check(TokenType.LPAREN):
            self.consume(TokenType.LPAREN, "Expected '('")
            module = self.consume(TokenType.STRING, "Expected module path").value
            self.consume(TokenType.RPAREN, "Expected ')'")
            return ImportNode(module, None)
        
        # import x from y syntax
        names = []
        while True:
            names.append(self.consume(TokenType.IDENTIFIER, "Expected name").value)
            if not self.match(TokenType.COMMA):
                break
        self.consume(TokenType.FROM, "Expected 'from'")
        module = self.consume(TokenType.STRING, "Expected module name").value
        return ImportNode(module, names)
    
    def print_statement(self) -> PrintNode:
        self.consume(TokenType.LPAREN, "Expected '(' after print")
        args = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')' after print args")
        return PrintNode(args)
    
    def type_statement(self) -> TypeNode:
        self.consume(TokenType.LPAREN, "Expected '(' after type")
        arg = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after type arg")
        return TypeNode(arg)
    
    def expression_statement(self) -> ASTNode:
        expr = self.expression()
        if self.match(TokenType.EQUAL):
            if isinstance(expr, IdentifierNode):
                value = self.expression()
                return AssignmentNode(expr, value)
        return expr
    
    def expression(self) -> ASTNode:
        return self.or_expression()
    
    def or_expression(self) -> ASTNode:
        left = self.and_expression()
        while self.match(TokenType.OR):
            right = self.and_expression()
            left = BinaryNode("or", left, right)
        return left
    
    def and_expression(self) -> ASTNode:
        left = self.equality()
        while self.match(TokenType.AND):
            right = self.equality()
            left = BinaryNode("and", left, right)
        return left
    
    def equality(self) -> ASTNode:
        left = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous().value
            right = self.comparison()
            left = BinaryNode(operator, left, right)
        return left
    
    def comparison(self) -> ASTNode:
        left = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous().value
            right = self.term()
            left = BinaryNode(operator, left, right)
        return left
    
    def term(self) -> ASTNode:
        left = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous().value
            right = self.factor()
            left = BinaryNode(operator, left, right)
        return left
    
    def factor(self) -> ASTNode:
        left = self.exponent()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self.previous().value
            right = self.exponent()
            left = BinaryNode(operator, left, right)
        return left
    
    def exponent(self) -> ASTNode:
        left = self.call()
        while self.match(TokenType.STAR_STAR):
            right = self.unary()
            left = BinaryNode("**", left, right)
        return left
    
    def unary(self) -> ASTNode:
        if self.match(TokenType.BANG, TokenType.MINUS, TokenType.NOT):
            operator = self.previous().value
            operand = self.unary()
            return UnaryNode(operator, operand)
        return self.exponent()
    
    def call(self) -> ASTNode:
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA):
                            break
                self.consume(TokenType.RPAREN, "Expected ')' after arguments")
                if isinstance(expr, IdentifierNode):
                    return CallNode(expr.name, args)
                return CallNode(str(expr), args)
            elif self.match(TokenType.LBRACKET):
                index = self.expression()
                self.consume(TokenType.RBRACKET, "Expected ']' after index")
                return IndexNode(expr, index)
            else:
                break
        return expr
    
    def primary(self) -> ASTNode:
        token = self.peek()
        
        if self.match(TokenType.NUMBER):
            return NumberNode(token.value)
        if self.match(TokenType.STRING):
            return StringNode(token.value)
        if self.match(TokenType.TRUE):
            return BooleanNode(True)
        if self.match(TokenType.FALSE):
            return BooleanNode(False)
        if self.match(TokenType.IDENTIFIER):
            return IdentifierNode(token.value)
        if self.match(TokenType.PRINT, TokenType.TYPE):
            return self._parse_builtin_call(token)
        if self.match(TokenType.IMPORT):
            path_token = self.consume(TokenType.STRING, "Expected module path")
            return ImportNode(path_token.value)
        
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return GroupingNode(expr)
        
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']'")
            return ListNode(elements)
        
        if self.match(TokenType.LBRACE):
            pairs = {}
            if not self.check(TokenType.RBRACE):
                while True:
                    key = self.expression()
                    self.consume(TokenType.COLON, "Expected ':'")
                    value = self.expression()
                    pairs[key] = value
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACE, "Expected '}'")
            return DictNode(pairs)
        
        raise SyntaxError(f"Unexpected token: {token.type.name} at {token.line}:{token.column}")
    
    def _parse_builtin_call(self, token: Token) -> ASTNode:
        self.consume(TokenType.LPAREN, "Expected '('")
        args = []
        if not self.check(TokenType.RPAREN):
            while True:
                args.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expected ')'")
        
        if token.type == TokenType.PRINT:
            return PrintNode(args)
        elif token.type == TokenType.TYPE:
            return TypeNode(args[0] if args else None)
        return CallNode(token.value, args)
        
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACKET, "Expected ']'")
            return ListNode(elements)
        
        if self.match(TokenType.LBRACE):
            pairs = {}
            if not self.check(TokenType.RBRACE):
                while True:
                    key = self.expression()
                    self.consume(TokenType.COLON, "Expected ':'")
                    value = self.expression()
                    pairs[key] = value
                    if not self.match(TokenType.COMMA):
                        break
            self.consume(TokenType.RBRACE, "Expected '}'")
            return DictNode(pairs)
        
        raise SyntaxError(f"Unexpected token: {token.type.name} at {token.line}:{token.column}")


def parse(source: str) -> ProgramNode:
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    test_code = '''
fn add(a, b) (
    return a + b
)

fn factorial(n) (
    if (n <= 1) (
        return 1
    ) else (
        return n * factorial(n - 1)
    )
)

result = add(5, 10)
print(result)
print("Hello World")

x = [1, 2, 3]
print(x[0])

person = {"name": "Alice"}
print(person["name"])
'''
    
    program = parse(test_code)
    print(dump_ast(program))