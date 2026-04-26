

from enum import Enum, auto


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    DOT = auto()
    
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    STAR_STAR = auto()
    STAR_EQUAL = auto()
    SLASH_SLASH = auto()
    
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    FN = auto()
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RETURN = auto()
    PRINT = auto()
    TYPE = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    TRY = auto()
    CATCH = auto()
    IMPORT = auto()
    FROM = auto()
    BREAK = auto()
    CONTINUE = auto()
    PASS = auto()
    
    NEWLINE = auto()
    EOF = auto()


RESERVED_KEYWORDS = {
    "fn": TokenType.FN,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "elif": TokenType.ELIF,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "return": TokenType.RETURN,
    "print": TokenType.PRINT,
    "type": TokenType.TYPE,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "try": TokenType.TRY,
    "catch": TokenType.CATCH,
    "import": TokenType.IMPORT,
    "from": TokenType.FROM,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "pass": TokenType.PASS,
}


class Token:
    __slots__ = ("type", "value", "line", "column")
    
    def __init__(self, type: TokenType, value: any, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    
    def advance(self) -> str:
        if self.is_at_end():
            return "\0"
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        return char
    
    def add_token(self, type: TokenType, value: any = None):
        if value is None:
            value = self.source[self.start:self.current]
        self.tokens.append(Token(type, value, self.line, self.column))
    
    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                raise SyntaxError(f"Unterminated string at line {self.line}")
            self.advance()
        
        if self.is_at_end():
            raise SyntaxError(f"Unterminated string at line {self.line}")
        
        self.advance()
        
        value = self.source[self.start + 1:self.current - 1]
        value = value.replace("\\n", "\n").replace("\\t", "\t").replace("\\\"", '"').replace("\\\\", "\\")
        self.add_token(TokenType.STRING, value)
    
    def number(self):
        while self.peek().isdigit():
            self.advance()
        
        is_float = False
        if self.peek() == "." and self.peek_next().isdigit():
            is_float = True
            self.advance()
            while self.peek().isdigit():
                self.advance()
        
        text = self.source[self.start:self.current]
        if is_float:
            self.add_token(TokenType.NUMBER, float(text))
        else:
            self.add_token(TokenType.NUMBER, int(text))
    
    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        
        text = self.source[self.start:self.current]
        
        if text in RESERVED_KEYWORDS:
            self.add_token(RESERVED_KEYWORDS[text])
        else:
            self.add_token(TokenType.IDENTIFIER, text)
    
    def skip_comment(self):
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()
    
    def scan_token(self):
        char = self.peek()
        
        if char == "(":
            self.advance()
            self.add_token(TokenType.LPAREN, "(")
        elif char == ")":
            self.advance()
            self.add_token(TokenType.RPAREN, ")")
        elif char == "[":
            self.advance()
            self.add_token(TokenType.LBRACKET, "[")
        elif char == "]":
            self.advance()
            self.add_token(TokenType.RBRACKET, "]")
        elif char == "{":
            self.advance()
            self.add_token(TokenType.LBRACE, "{")
        elif char == "}":
            self.advance()
            self.add_token(TokenType.RBRACE, "}")
        elif char == ",":
            self.advance()
            self.add_token(TokenType.COMMA, ",")
        elif char == ":":
            self.advance()
            self.add_token(TokenType.COLON, ":")
        elif char == ".":
            self.advance()
            self.add_token(TokenType.DOT, ".")
        elif char == "+":
            self.advance()
            self.add_token(TokenType.PLUS, "+")
        elif char == "-":
            self.advance()
            self.add_token(TokenType.MINUS, "-")
        elif char == "*":
            self.advance()
            if self.peek() == "*":
                self.advance()
                self.add_token(TokenType.STAR_STAR, "**")
            else:
                self.add_token(TokenType.STAR, "*")
        elif char == "/":
            self.advance()
            self.add_token(TokenType.SLASH, "/")
        elif char == "%":
            self.advance()
            self.add_token(TokenType.PERCENT, "%")
        elif char == "=" and self.peek_next() == "=":
            self.advance()
            self.advance()
            self.add_token(TokenType.EQUAL_EQUAL, "==")
        elif char == "=":
            self.advance()
            self.add_token(TokenType.EQUAL, "=")
        elif char == "!" and self.peek_next() == "=":
            self.advance()
            self.advance()
            self.add_token(TokenType.BANG_EQUAL, "!=")
        elif char == "!":
            self.advance()
            self.add_token(TokenType.BANG, "!")
        elif char == "<" and self.peek_next() == "=":
            self.advance()
            self.advance()
            self.add_token(TokenType.LESS_EQUAL, "<=")
        elif char == "<":
            self.advance()
            self.add_token(TokenType.LESS, "<")
        elif char == ">" and self.peek_next() == "=":
            self.advance()
            self.advance()
            self.add_token(TokenType.GREATER_EQUAL, ">=")
        elif char == ">":
            self.advance()
            self.add_token(TokenType.GREATER, ">")
        elif char == "\n":
            self.advance()
            self.add_token(TokenType.NEWLINE, "\n")
        elif char == '"':
            self.advance()
            self.string()
        elif char.isdigit():
            self.number()
        elif char.isalpha() or char == "_":
            self.identifier()
        elif char == " " or char == "\t":
            self.advance()
        elif char == "#":
            self.skip_comment()
        elif char == "/" and self.peek_next() == "/":
            self.advance()
            self.advance()
            self.skip_comment()
        else:
            self.advance()
    
    def scan(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.add_token(TokenType.EOF)
        return self.tokens


def tokenize(source: str) -> list[Token]:
    lexer = Lexer(source)
    return lexer.scan()


if __name__ == "__main__":
    test_code = '''
fn main() (
    x = 10
    y = 20
    if (x < y) (
        print("x is less than y")
    )
)

result = add(5, 10)
'''
    
    tokens = tokenize(test_code)
    for token in tokens:
        print(token)