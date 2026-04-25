"""
Ark Programming Language - Basic Interpreter
Executes AST and produces output (simple version for immediate functionality)
This is a temporary interpreter until Batch 4 provides the full one.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import sys


class ValueType(Enum):
    """Data types in Ark"""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    NIL = "nil"
    FUNCTION = "function"
    LIST = "list"
    DICT = "dict"


@dataclass
class ArkValue:
    """Represents a value in Ark"""
    type: ValueType
    value: Any
    
    def __repr__(self) -> str:
        if self.type == ValueType.STRING:
            return self.value
        elif self.type == ValueType.NIL:
            return "nil"
        elif self.type == ValueType.BOOLEAN:
            return "true" if self.value else "false"
        else:
            return str(self.value)
    
    def is_truthy(self) -> bool:
        """Check if value is truthy"""
        if self.type == ValueType.NIL:
            return False
        elif self.type == ValueType.BOOLEAN:
            return self.value
        elif self.type == ValueType.NUMBER:
            return self.value != 0
        elif self.type == ValueType.STRING:
            return len(self.value) > 0
        else:
            return True


class BasicInterpreter:
    """
    Basic interpreter for Ark that executes simple programs.
    Designed to work with the lexer from Batch 1.
    This is a simplified version - the full interpreter comes in Batch 4.
    """
    
    def __init__(self):
        self.globals: Dict[str, any] = {}
        self.locals_stack: List[Dict[str, ArkValue]] = []
        self.functions: Dict[str, List] = {}  # Store function bodies as token lists
    
    def execute_code(self, code: str) -> None:
        """Execute Ark code string"""
        from lexer import lex, TokenType
        
        try:
            tokens = lex(code)
            self.execute_tokens(tokens)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
    
    def execute_tokens(self, tokens) -> None:
        """Execute a list of tokens"""
        from lexer import TokenType
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Skip newlines and whitespace
            if token.type in (TokenType.NEWLINE, TokenType.EOF):
                i += 1
                continue
            
            # Handle print statements
            if token.type == TokenType.PRINT:
                i = self.handle_print(tokens, i)
                continue
            
            # Handle variable declarations
            if token.type == TokenType.LET:
                i = self.handle_let(tokens, i)
                continue
            
            # Handle function definitions
            if token.type == TokenType.FN:
                i = self.handle_function(tokens, i)
                continue
            
            # Handle if statements
            if token.type == TokenType.IF:
                i = self.handle_if(tokens, i)
                continue
            
            # Handle while loops
            if token.type == TokenType.WHILE:
                i = self.handle_while(tokens, i)
                continue
            
            # Handle return
            if token.type == TokenType.RETURN:
                i += 1
                continue
            
            # Handle function calls
            if token.type == TokenType.IDENTIFIER:
                # Look ahead for function call
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LPAREN:
                    i = self.handle_function_call(tokens, i)
                    continue
            
            i += 1
    
    def handle_print(self, tokens, start_idx) -> int:
        """Handle print() statements"""
        from lexer import TokenType
        
        i = start_idx + 1  # Skip 'print'
        
        # Expect (
        if i >= len(tokens) or tokens[i].type != TokenType.LPAREN:
            return i
        
        i += 1  # Skip (
        
        # Evaluate the full expression (handles concatenation with +)
        value, next_i = self.evaluate_print_args(tokens, i)
        i = next_i
        
        # Skip )
        if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
            i += 1
        
        # Print the result
        if value is not None:
            print(value, end='')
        
        return i
    
    def handle_let(self, tokens, start_idx) -> int:
        """Handle variable declarations (let x = value)"""
        from lexer import TokenType
        
        i = start_idx + 1  # Skip 'let'
        
        # Get variable name
        if i >= len(tokens) or tokens[i].type != TokenType.IDENTIFIER:
            return i
        
        var_name = tokens[i].value
        i += 1
        
        # Expect =
        if i >= len(tokens) or tokens[i].type != TokenType.ASSIGN:
            return i
        
        i += 1  # Skip =
        
        # Evaluate the expression
        value, next_i = self.evaluate_expression(tokens, i)
        i = next_i
        
        # Store the variable
        if value is not None:
            self.globals[var_name] = value
        
        return i
    
    def handle_function(self, tokens, start_idx) -> int:
        """Handle function definitions (fn name() (...))"""
        from lexer import TokenType
        
        i = start_idx + 1  # Skip 'fn'
        
        # Get function name
        if i >= len(tokens) or tokens[i].type != TokenType.IDENTIFIER:
            return i
        
        func_name = tokens[i].value
        i += 1
        
        # Skip parameters for now (simplified)
        while i < len(tokens) and tokens[i].type != TokenType.LPAREN:
            i += 1
        
        if i >= len(tokens):
            return i
        
        # Skip the opening (
        i += 1
        
        # Find the closing ) which marks the end of the body
        paren_count = 1
        body_start = i
        
        while i < len(tokens) and paren_count > 0:
            if tokens[i].type == TokenType.LPAREN:
                paren_count += 1
            elif tokens[i].type == TokenType.RPAREN:
                paren_count -= 1
                if paren_count == 0:
                    break
            i += 1
        
        # Store function body (tokens between opening and closing paren)
        body_tokens = tokens[body_start:i]
        self.functions[func_name] = body_tokens
        
        # Skip the closing )
        if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
            i += 1
        
        return i
    
    def handle_function_call(self, tokens, start_idx) -> int:
        """Handle function calls"""
        from lexer import TokenType
        
        func_name = tokens[start_idx].value
        i = start_idx + 1
        
        # Skip (
        if i >= len(tokens) or tokens[i].type != TokenType.LPAREN:
            return i
        i += 1
        
        # Skip arguments for now
        args = []
        while i < len(tokens) and tokens[i].type != TokenType.RPAREN:
            i += 1
        
        # Skip )
        if i < len(tokens) and tokens[i].type == TokenType.RPAREN:
            i += 1
        
        # If function exists, execute it
        if func_name in self.functions:
            body_tokens = self.functions[func_name]
            self.execute_tokens(body_tokens)
        
        return i
    
    def handle_if(self, tokens, start_idx) -> int:
        """Handle if statements (simplified)"""
        from lexer import TokenType
        
        i = start_idx + 1  # Skip 'if'
        
        # Skip the condition for now (simplified)
        while i < len(tokens) and tokens[i].type != TokenType.LPAREN:
            i += 1
        
        # Skip condition and body
        paren_count = 0
        in_condition = False
        
        while i < len(tokens):
            if tokens[i].type == TokenType.LPAREN:
                paren_count += 1
                in_condition = True
            elif tokens[i].type == TokenType.RPAREN:
                paren_count -= 1
                if paren_count == 0 and in_condition:
                    break
            i += 1
        
        if i < len(tokens):
            i += 1
        
        return i
    
    def handle_while(self, tokens, start_idx) -> int:
        """Handle while loops (simplified)"""
        from lexer import TokenType
        
        i = start_idx + 1  # Skip 'while'
        
        # Skip condition and body
        paren_count = 0
        
        while i < len(tokens):
            if tokens[i].type == TokenType.LPAREN:
                paren_count += 1
            elif tokens[i].type == TokenType.RPAREN:
                paren_count -= 1
                if paren_count == 0:
                    break
            i += 1
        
        if i < len(tokens):
            i += 1
        
        return i
    
    def evaluate_expression(self, tokens, start_idx) -> tuple:
        """Evaluate a simple expression and return (value, next_index)"""
        from lexer import TokenType
        
        i = start_idx
        
        if i >= len(tokens):
            return None, i
        
        token = tokens[i]
        
        # String literal
        if token.type == TokenType.STRING:
            value = ArkValue(ValueType.STRING, token.value)
            return value, i + 1
        
        # Number literal
        if token.type == TokenType.NUMBER:
            try:
                if '.' in token.value:
                    num = float(token.value)
                else:
                    num = int(token.value)
                value = ArkValue(ValueType.NUMBER, num)
                return value, i + 1
            except ValueError:
                return None, i + 1
        
        # Boolean
        if token.type == TokenType.TRUE:
            return ArkValue(ValueType.BOOLEAN, True), i + 1
        
        if token.type == TokenType.FALSE:
            return ArkValue(ValueType.BOOLEAN, False), i + 1
        
        # Nil
        if token.type == TokenType.NIL:
            return ArkValue(ValueType.NIL, None), i + 1
        
        # Identifier (variable reference)
        if token.type == TokenType.IDENTIFIER:
            var_name = token.value
            if var_name in self.globals:
                return self.globals[var_name], i + 1
            else:
                # Unknown variable - return as is
                return ArkValue(ValueType.STRING, var_name), i + 1
        
        return None, i + 1
    
    def evaluate_print_args(self, tokens, start_idx) -> tuple:
        """Evaluate print arguments, handling concatenation with +"""
        from lexer import TokenType
        
        i = start_idx
        result_str = ""
        
        while i < len(tokens) and tokens[i].type != TokenType.RPAREN:
            if tokens[i].type == TokenType.COMMA:
                i += 1
                continue
            
            # Get the next value
            value, next_i = self.evaluate_expression(tokens, i)
            
            if value is not None:
                result_str += str(value)
                i = next_i
                
                # Check for + operator (concatenation)
                if i < len(tokens) and tokens[i].type == TokenType.PLUS:
                    i += 1  # Skip +
                    continue
            else:
                i += 1
        
        return result_str, i
