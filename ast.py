"""
Ark Programming Language - Batch 2: AST Node Definitions
Creating a tree structure that understands nested () blocks.
"""

from __future__ import annotations
from enum import Enum, auto
from typing import Any, Optional


class NodeType(Enum):
    PROGRAM = auto()
    FUNCTION = auto()
    PARAMETER_LIST = auto()
    PARAMETER = auto()
    CALL = auto()
    ARGUMENT_LIST = auto()
    BLOCK = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    RETURN = auto()
    ASSIGNMENT = auto()
    EXPRESSION = auto()
    BINARY = auto()
    UNARY = auto()
    GROUPING = auto()
    INDEX = auto()
    SLICE = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    LIST = auto()
    DICT = auto()
    LIST_LITERAL = auto()
    DICT_LITERAL = auto()
    TRY = auto()
    CATCH = auto()
    IMPORT = auto()
    PRINT = auto()
    TYPE = auto()
    BREAK = auto()
    CONTINUE = auto()
    PASS = auto()


class ASTNode:
    __slots__ = ("node_type", "line", "column")
    
    def __init__(self, node_type: NodeType, line: int = 1, column: int = 1):
        self.node_type = node_type
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"{self.node_type.name}(line={self.line})"


class ProgramNode(ASTNode):
    __slots__ = ("statements",)
    
    def __init__(self, statements: list[ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.PROGRAM, line, column)
        self.statements = statements


class FunctionNode(ASTNode):
    __slots__ = ("name", "parameters", "body")
    
    def __init__(self, name: str, parameters: list[ParameterNode], body: BlockNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.FUNCTION, line, column)
        self.name = name
        self.parameters = parameters
        self.body = body


class ParameterNode(ASTNode):
    __slots__ = ("name", "default")
    
    def __init__(self, name: str, default: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.PARAMETER, line, column)
        self.name = name
        self.default = default


class BlockNode(ASTNode):
    __slots__ = ("statements",)
    
    def __init__(self, statements: list[ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements


class IdentifierNode(ASTNode):
    __slots__ = ("name",)
    
    def __init__(self, name: str, line: int = 1, column: int = 1):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


class NumberNode(ASTNode):
    __slots__ = ("value",)
    
    def __init__(self, value: float, line: int = 1, column: int = 1):
        super().__init__(NodeType.NUMBER, line, column)
        self.value = value


class StringNode(ASTNode):
    __slots__ = ("value",)
    
    def __init__(self, value: str, line: int = 1, column: int = 1):
        super().__init__(NodeType.STRING, line, column)
        self.value = value


class BooleanNode(ASTNode):
    __slots__ = ("value",)
    
    def __init__(self, value: bool, line: int = 1, column: int = 1):
        super().__init__(NodeType.BOOLEAN, line, column)
        self.value = value


class BinaryNode(ASTNode):
    __slots__ = ("operator", "left", "right")
    
    def __init__(self, operator: str, left: ASTNode, right: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.BINARY, line, column)
        self.operator = operator
        self.left = left
        self.right = right


class UnaryNode(ASTNode):
    __slots__ = ("operator", "operand")
    
    def __init__(self, operator: str, operand: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.UNARY, line, column)
        self.operator = operator
        self.operand = operand


class GroupingNode(ASTNode):
    __slots__ = ("expression",)
    
    def __init__(self, expression: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.GROUPING, line, column)
        self.expression = expression


class AssignmentNode(ASTNode):
    __slots__ = ("target", "value")
    
    def __init__(self, target: IdentifierNode, value: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.target = target
        self.value = value


class CallNode(ASTNode):
    __slots__ = ("name", "arguments")
    
    def __init__(self, name: str, arguments: list[ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.CALL, line, column)
        self.name = name
        self.arguments = arguments


class IfNode(ASTNode):
    __slots__ = ("condition", "then_branch", "elif_branches", "else_branch")
    
    def __init__(self, condition: ASTNode, then_branch: BlockNode, elif_branches: list[tuple[ASTNode, BlockNode]], else_branch: Optional[BlockNode] = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.IF, line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.elif_branches = elif_branches
        self.else_branch = else_branch


class WhileNode(ASTNode):
    __slots__ = ("condition", "body")
    
    def __init__(self, condition: ASTNode, body: BlockNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.WHILE, line, column)
        self.condition = condition
        self.body = body


class ForNode(ASTNode):
    __slots__ = ("variable", "iterable", "body")
    
    def __init__(self, variable: str, iterable: ASTNode, body: BlockNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.FOR, line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body


class ReturnNode(ASTNode):
    __slots__ = ("value",)
    
    def __init__(self, value: Optional[ASTNode] = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.RETURN, line, column)
        self.value = value


class PrintNode(ASTNode):
    __slots__ = ("arguments",)
    
    def __init__(self, arguments: list[ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.PRINT, line, column)
        self.arguments = arguments


class TypeNode(ASTNode):
    __slots__ = ("argument",)
    
    def __init__(self, argument: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.TYPE, line, column)
        self.argument = argument


class ListNode(ASTNode):
    __slots__ = ("elements",)
    
    def __init__(self, elements: list[ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.LIST, line, column)
        self.elements = elements


class DictNode(ASTNode):
    __slots__ = ("pairs",)
    
    def __init__(self, pairs: dict[ASTNode, ASTNode], line: int = 1, column: int = 1):
        super().__init__(NodeType.DICT, line, column)
        self.pairs = pairs


class IndexNode(ASTNode):
    __slots__ = ("value", "index")
    
    def __init__(self, value: ASTNode, index: ASTNode, line: int = 1, column: int = 1):
        super().__init__(NodeType.INDEX, line, column)
        self.value = value
        self.index = index


class TryNode(ASTNode):
    __slots__ = ("try_body", "catch_body", "variable")
    
    def __init__(self, try_body: BlockNode, catch_body: BlockNode, variable: str = "error", line: int = 1, column: int = 1):
        super().__init__(NodeType.TRY, line, column)
        self.try_body = try_body
        self.catch_body = catch_body
        self.variable = variable


class ImportNode(ASTNode):
    __slots__ = ("module", "names")
    
    def __init__(self, module: str, names: Optional[list[str]] = None, line: int = 1, column: int = 1):
        super().__init__(NodeType.IMPORT, line, column)
        self.module = module
        self.names = names


class BreakNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(NodeType.BREAK, line, column)


class ContinueNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(NodeType.CONTINUE, line, column)


class PassNode(ASTNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(NodeType.PASS, line, column)


class ASTVisitor:
    def visit(self, node: ASTNode) -> Any:
        method_name = f"visit_{node.node_type.name}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> Any:
        raise NotImplementedError(f"No visit_{node.node_type.name} method")


def dump_ast(node: ASTNode, indent: int = 0) -> str:
    prefix = "  " * indent
    result = f"{prefix}{node.node_type.name}"
    
    if isinstance(node, ProgramNode):
        result += f" ({len(node.statements)} statements)"
        for stmt in node.statements:
            result += "\n" + dump_ast(stmt, indent + 1)
    elif isinstance(node, FunctionNode):
        result += f" {node.name}"
        if node.parameters:
            result += "\n" + f"{prefix}  Parameters:"
            for param in node.parameters:
                result += "\n" + dump_ast(param, indent + 2)
        result += "\n" + dump_ast(node.body, indent + 1)
    elif isinstance(node, BlockNode):
        result += f" ({len(node.statements)} statements)"
        for stmt in node.statements:
            result += "\n" + dump_ast(stmt, indent + 1)
    elif isinstance(node, BinaryNode):
        result += f" {node.operator}"
        result += "\n" + dump_ast(node.left, indent + 1)
        result += "\n" + dump_ast(node.right, indent + 1)
    elif isinstance(node, IdentifierNode):
        result += f" {node.name}"
    elif isinstance(node, NumberNode):
        result += f" {node.value}"
    elif isinstance(node, StringNode):
        result += f" {repr(node.value)}"
    elif isinstance(node, BooleanNode):
        result += f" {node.value}"
    elif isinstance(node, CallNode):
        result += f" {node.name}"
        if node.arguments:
            result += " args:"
            for arg in node.arguments:
                result += "\n" + dump_ast(arg, indent + 1)
    elif isinstance(node, AssignmentNode):
        result += f" {node.target.name}"
        result += "\n" + dump_ast(node.value, indent + 1)
    elif isinstance(node, IfNode):
        result += "\n" + dump_ast(node.condition, indent + 1)
        result += "\n" + f"{prefix}  Then:"
        result += "\n" + dump_ast(node.then_branch, indent + 1)
        if node.else_branch:
            result += "\n" + f"{prefix}  Else:"
            result += "\n" + dump_ast(node.else_branch, indent + 1)
    elif isinstance(node, WhileNode):
        result += "\n" + dump_ast(node.condition, indent + 1)
        result += "\n" + dump_ast(node.body, indent + 1)
    elif isinstance(node, PrintNode):
        for arg in node.arguments:
            result += "\n" + dump_ast(arg, indent + 1)
    elif isinstance(node, ReturnNode):
        if node.value:
            result += "\n" + dump_ast(node.value, indent + 1)
    elif isinstance(node, ListNode):
        result += f" ({len(node.elements)} elements)"
        for elem in node.elements:
            result += "\n" + dump_ast(elem, indent + 1)
    elif isinstance(node, DictNode):
        result += f" ({len(node.pairs)} pairs)"
        for key, val in node.pairs.items():
            result += "\n" + f"{prefix}  {dump_ast(key, indent + 1)}: "
            result += dump_ast(val, indent + 2)
    else:
        result += f" ({type(node).__name__})"
    
    return result


if __name__ == "__main__":
    program = ProgramNode([
        FunctionNode(
            "add",
            [ParameterNode("a"), ParameterNode("b")],
            BlockNode([
                ReturnNode(BinaryNode("+", IdentifierNode("a"), IdentifierNode("b")))
            ])
        ),
        CallNode("print", [
            NumberNode(10)
        ])
    ])
    
    print(dump_ast(program))