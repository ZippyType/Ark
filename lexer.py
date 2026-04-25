"""
Ark Programming Language - Advanced Lexer/Scanner
Tokenizes Ark source code into a stream of tokens for the parser.
Handles parentheses-based scoping, strings, numbers, keywords, and operators.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    """Token types for the Ark language."""
    
    # Literals
    NUMBER = auto()           # 42, 3.14
    STRING = auto()           # "hello", 'world'
    IDENTIFIER = auto()       # variable_name, function_name
    
    # Keywords
    FN = auto()               # fn
    IF = auto()               # if
    ELSE = auto()             # else
    ELIF = auto()             # elif
    WHILE = auto()            # while
    FOR = auto()              # for
    LET = auto()              # let
    RETURN = auto()           # return
    PRINT = auto()            # print
    TYPE = auto()             # type
    TRUE = auto()             # true
    FALSE = auto()            # false
    NIL = auto()              # nil
    IN = auto()               # in
    BREAK = auto()            # break
    CONTINUE = auto()         # continue
    
    # Operators
    PLUS = auto()             # +
    MINUS = auto()            # -
    STAR = auto()             # *
    SLASH = auto()            # /
    PERCENT = auto()          # %
    POWER = auto()            # **
    
    # Comparison
    EQ = auto()               # ==
    NE = auto()               # !=
    LT = auto()               # <
    LE = auto()               # <=
    GT = auto()               # >
    GE = auto()               # >=
    
    # Logical
    AND = auto()              # and
    OR = auto()               # or
    NOT = auto()              # not
    
    # Assignment & Delimiters
    ASSIGN = auto()           # =
    LPAREN = auto()           # (
    RPAREN = auto()           # )
    LBRACKET = auto()         # [
    RBRACKET = auto()         # ]
    LBRACE = auto()           # {
    RBRACE = auto()           # }
    COMMA = auto()            # ,
    DOT = auto()              # .
    COLON = auto()            # :
    SEMICOLON = auto()        # ;
    ARROW = auto()            # ->
    
    # Special
    NEWLINE = auto()          # \n (significant in some contexts)
    EOF = auto()              # End of file
    
    # Comments (for tracking, but typically stripped)
    COMMENT = auto()          # // or #


@dataclass
class Token:
    """Represents a single token in the source code."""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}, {self.column})"


class Lexer:
    """
    Advanced lexer for the Ark programming language.
    Tokenizes source code into a stream of Token objects.
    """
    
    KEYWORDS = {
        'fn': TokenType.FN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'elif': TokenType.ELIF,
        'while': TokenType.WHILE,
        'for': TokenType.FOR,
        'let': TokenType.LET,
        'return': TokenType.RETURN,
        'print': TokenType.PRINT,
        'type': TokenType.TYPE,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'nil': TokenType.NIL,
        'in': TokenType.IN,
        'and': TokenType.AND,
        'or': TokenType.OR,
        'not': TokenType.NOT,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
    }
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The Ark source code as a string.
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.current_char = self.source[0] if source else None
    
    def error(self, message: str) -> None:
        """Raise a lexical error with line and column information."""
        raise SyntaxError(f"Lexical Error at line {self.line}, column {self.column}: {message}")
    
    def advance(self) -> None:
        """Move to the next character in the source."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Look ahead at the next character(s) without consuming."""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self) -> None:
        """Skip whitespace characters except newlines (newlines are significant)."""
        while self.current_char is not None and self.current_char in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> None:
        """Skip single-line comments (// or #)."""
        # Skip the comment markers
        if self.current_char == '/' and self.peek() == '/':
            self.advance()
            self.advance()
        elif self.current_char == '#':
            self.advance()
        else:
            return
        
        # Skip until newline
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
    
    def read_string(self, quote_char: str) -> str:
        """
        Read a string literal.
        
        Args:
            quote_char: The quote character (' or ").
        
        Returns:
            The string value (without quotes).
        """
        result = ""
        self.advance()  # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    self.error("Unterminated string literal")
                
                escape_chars = {
                    'n': '\n',
                    't': '\t',
                    'r': '\r',
                    '\\': '\\',
                    '"': '"',
                    "'": "'",
                    '0': '\0',
                }
                result += escape_chars.get(self.current_char, self.current_char)
                self.advance()
            else:
                result += self.current_char
                self.advance()
        
        if self.current_char != quote_char:
            self.error("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return result
    
    def read_number(self) -> str:
        """
        Read a numeric literal (integer or float).
        
        Returns:
            The numeric value as a string.
        """
        result = ""
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        return result
    
    def read_identifier(self) -> str:
        """
        Read an identifier or keyword.
        
        Returns:
            The identifier as a string.
        """
        result = ""
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        return result
    
    def add_token(self, token_type: TokenType, value: str = "") -> None:
        """Add a token to the token list."""
        # Adjust column for the start of the token
        token_col = self.column - len(value) - 1 if value else self.column
        token = Token(token_type, value, self.line, max(1, token_col))
        self.tokens.append(token)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            A list of Token objects.
        """
        while self.current_char is not None:
            # Skip whitespace
            self.skip_whitespace()
            
            if self.current_char is None:
                break
            
            # Handle comments
            if (self.current_char == '/' and self.peek() == '/') or self.current_char == '#':
                self.skip_comment()
                continue
            
            # Handle newlines (significant for statement separation)
            if self.current_char == '\n':
                self.add_token(TokenType.NEWLINE, '\n')
                self.advance()
                continue
            
            # Handle strings
            if self.current_char in '"\'':
                quote = self.current_char
                string_value = self.read_string(quote)
                self.add_token(TokenType.STRING, string_value)
                continue
            
            # Handle numbers
            if self.current_char.isdigit():
                number = self.read_number()
                self.add_token(TokenType.NUMBER, number)
                continue
            
            # Handle identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                identifier = self.read_identifier()
                token_type = self.KEYWORDS.get(identifier, TokenType.IDENTIFIER)
                self.add_token(token_type, identifier)
                continue
            
            # Handle operators and delimiters
            if self.current_char == '+':
                self.add_token(TokenType.PLUS, '+')
                self.advance()
            elif self.current_char == '-':
                if self.peek() == '>':
                    self.add_token(TokenType.ARROW, '->')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.MINUS, '-')
                    self.advance()
            elif self.current_char == '*':
                if self.peek() == '*':
                    self.add_token(TokenType.POWER, '**')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.STAR, '*')
                    self.advance()
            elif self.current_char == '/':
                self.add_token(TokenType.SLASH, '/')
                self.advance()
            elif self.current_char == '%':
                self.add_token(TokenType.PERCENT, '%')
                self.advance()
            elif self.current_char == '=':
                if self.peek() == '=':
                    self.add_token(TokenType.EQ, '==')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.ASSIGN, '=')
                    self.advance()
            elif self.current_char == '!':
                if self.peek() == '=':
                    self.add_token(TokenType.NE, '!=')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.NOT, '!')
                    self.advance()
            elif self.current_char == '<':
                if self.peek() == '=':
                    self.add_token(TokenType.LE, '<=')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.LT, '<')
                    self.advance()
            elif self.current_char == '>':
                if self.peek() == '=':
                    self.add_token(TokenType.GE, '>=')
                    self.advance()
                    self.advance()
                else:
                    self.add_token(TokenType.GT, '>')
                    self.advance()
            elif self.current_char == '(':
                self.add_token(TokenType.LPAREN, '(')
                self.advance()
            elif self.current_char == ')':
                self.add_token(TokenType.RPAREN, ')')
                self.advance()
            elif self.current_char == '[':
                self.add_token(TokenType.LBRACKET, '[')
                self.advance()
            elif self.current_char == ']':
                self.add_token(TokenType.RBRACKET, ']')
                self.advance()
            elif self.current_char == '{':
                self.add_token(TokenType.LBRACE, '{')
                self.advance()
            elif self.current_char == '}':
                self.add_token(TokenType.RBRACE, '}')
                self.advance()
            elif self.current_char == ',':
                self.add_token(TokenType.COMMA, ',')
                self.advance()
            elif self.current_char == '.':
                self.add_token(TokenType.DOT, '.')
                self.advance()
            elif self.current_char == ':':
                self.add_token(TokenType.COLON, ':')
                self.advance()
            elif self.current_char == ';':
                self.add_token(TokenType.SEMICOLON, ';')
                self.advance()
            else:
                self.error(f"Unexpected character: {self.current_char!r}")
        
        # Add EOF token
        self.add_token(TokenType.EOF, "")
        return self.tokens


def lex(source: str) -> List[Token]:
    """
    Convenience function to tokenize Ark source code.
    
    Args:
        source: The Ark source code as a string.
    
    Returns:
        A list of Token objects.
    """
    lexer = Lexer(source)
    return lexer.tokenize()


if __name__ == "__main__":
    # Example: Test the lexer with simple Ark code
    test_code = """
    fn greet(name) (
        print("Hello, " + name)
    )
    
    let x = 42
    let message = "Welcome to Ark!"
    
    if (x > 10) (
        print("x is greater than 10")
    ) else (
        print("x is 10 or less")
    )
    
    while (x > 0) (
        print(x)
        x = x - 1
    )
    """
    
    tokens = lex(test_code)
    for token in tokens:
        print(token)
