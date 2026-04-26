"""
Ark Programming Language - Batch 5: Memory & Variables
Scoped variable storage: global vs. local scope.
"""

from typing import Any, Callable, Optional
from lexer import tokenize
from parser import parse
from ast import (
    ProgramNode, BlockNode, FunctionNode, ParameterNode,
    IdentifierNode, NumberNode, StringNode, BooleanNode,
    BinaryNode, UnaryNode, GroupingNode, AssignmentNode, CallNode,
    IfNode, WhileNode, ForNode, ReturnNode, PrintNode, TypeNode,
    ListNode, DictNode, IndexNode, TryNode, ImportNode,
    BreakNode, ContinueNode, PassNode, ASTNode, NodeType, FunctionNode
)


class ArkRuntimeError(Exception):
    def __init__(self, message: str, node: ASTNode = None):
        self.message = message
        self.node = node
        super().__init__(message)


class Function:
    def __init__(self, node: FunctionNode, closure: 'Scope'):
        self.node = node
        self.closure = closure
        self.name = node.name
        self.parameters = [p.name for p in node.parameters]
    
    def __repr__(self):
        return f"<fn {self.name}>"
    
    def __call__(self, interpreter: 'Interpreter', *args) -> Any:
        return interpreter.call_user_function(self, args)


class Scope:
    def __init__(self, parent: 'Scope' = None, is_function: bool = False):
        self.parent = parent
        self.values = {}
        self.is_function = is_function
        self.depth = 0 if parent is None else parent.depth + 1
    
    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise ArkRuntimeError(f"Undefined variable: '{name}'")
    
    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def assign(self, name: str, value: Any) -> bool:
        if name in self.values:
            self.values[name] = value
            return True
        if self.parent:
            return self.parent.assign(name, value)
        return False
    
    def get_depth(self, name: str) -> int:
        if name in self.values:
            return self.depth
        if self.parent:
            return self.parent.get_depth(name)
        return -1
    
    def copy(self) -> 'Scope':
        new_scope = Scope(self.parent, self.is_function)
        new_scope.values = self.values.copy()
        new_scope.depth = self.depth
        return new_scope


class Interpreter:
    def __init__(self):
        self.global_scope = Scope()
        self.scopes: list[Scope] = [self.global_scope]
        self.current_scope_idx = 0
        self.functions: dict[str, Function] = {}
        self._register_natives()
    
    @property
    def current_scope(self) -> Scope:
        return self.scopes[self.current_scope_idx]
    
    def _register_natives(self):
        self.global_scope.define("print", self._native_print)
        self.global_scope.define("type", self._native_type)
        self.global_scope.define("len", self._native_len)
        self.global_scope.define("str", self._native_str)
        self.global_scope.define("int", self._native_int)
        self.global_scope.define("float", self._native_float)
        self.global_scope.define("bool", self._native_bool)
        self.global_scope.define("list", self._native_list)
        self.global_scope.define("dict", self._native_dict)
        self.global_scope.define("input", self._native_input)
        self.global_scope.define("range", self._native_range)
        self.global_scope.define("abs", self._native_abs)
        self.global_scope.define("min", self._native_min)
        self.global_scope.define("max", self._native_max)
        self.global_scope.define("sum", self._native_sum)
        self.global_scope.define("sorted", self._native_sorted)
        self.global_scope.define("reversed", self._native_reversed)
        self.global_scope.define("enumerate", self._native_enumerate)
        self.global_scope.define("zip", self._native_zip)
        self.global_scope.define("map", self._native_map)
        self.global_scope.define("filter", self._native_filter)
        
        self.global_scope.define("True", True)
        self.global_scope.define("False", False)
    
    def _native_print(self, *args) -> None:
        output = []
        for arg in args:
            if isinstance(arg, list):
                output.append(str(arg))
            elif isinstance(arg, dict):
                output.append(str(arg))
            else:
                output.append(str(arg))
        print(" ".join(output))
        return None
    
    def _native_type(self, value: Any) -> str:
        t = type(value).__name__
        if t == "bool":
            return "bool"
        if t == "int":
            return "int"
        if t == "float":
            return "float"
        if t == "str":
            return "str"
        if t == "list":
            return "list"
        if t == "dict":
            return "dict"
        return t
    
    def _native_len(self, value: Any) -> int:
        if isinstance(value, (str, list, dict, tuple)):
            return len(value)
        if hasattr(value, '__len__'):
            return len(value)
        raise ArkRuntimeError(f"object has no len(): {type(value)}")
    
    def _native_str(self, value: Any) -> str:
        return str(value)
    
    def _native_int(self, value: Any) -> int:
        return int(value)
    
    def _native_float(self, value: Any) -> float:
        return float(value)
    
    def _native_bool(self, value: Any) -> bool:
        return bool(value)
    
    def _native_list(self, value: Any = None) -> list:
        if value is None:
            return []
        return list(value)
    
    def _native_dict(self, value: Any = None) -> dict:
        if value is None:
            return {}
        return dict(value)
    
    def _native_input(self, prompt: str = "") -> str:
        return input(str(prompt))
    
    def _native_range(self, *args) -> range:
        return range(*args)
    
    def _native_abs(self, value: Any) -> Any:
        return abs(value)
    
    def _native_min(self, *args) -> Any:
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            return min(args[0])
        return min(*args)
    
    def _native_max(self, *args) -> Any:
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            return max(args[0])
        return max(*args)
    
    def _native_sum(self, iterable: Any, start: int = 0) -> Any:
        return sum(iterable, start)
    
    def _native_sorted(self, iterable: Any, reverse: bool = False) -> list:
        return sorted(iterable, reverse=reverse)
    
    def _native_reversed(self, iterable: Any) -> list:
        return list(reversed(iterable))
    
    def _native_enumerate(self, iterable: Any, start: int = 0):
        return list(enumerate(iterable, start))
    
    def _native_zip(self, *iterables):
        return list(zip(*iterables))
    
    def _native_map(self, func: Callable, iterable: Any):
        return list(map(func, iterable))
    
    def _native_filter(self, func: Callable, iterable: Any):
        return list(filter(func, iterable))
    
    def interpret(self, program: ProgramNode) -> Any:
        result = None
        for statement in program.statements:
            result = self.execute(statement)
        return result
    
    def execute(self, node: Optional[ASTNode]) -> Any:
        if node is None:
            return None
        
        node_type = node.node_type
        
        if node_type == NodeType.PROGRAM:
            return self.interpret(node)
        
        elif node_type == NodeType.ASSIGNMENT:
            return self._visit_assignment(node)
        
        elif node_type == NodeType.IDENTIFIER:
            return self._visit_identifier(node)
        
        elif node_type == NodeType.NUMBER:
            return node.value
        
        elif node_type == NodeType.STRING:
            return node.value
        
        elif node_type == NodeType.BOOLEAN:
            return node.value
        
        elif node_type == NodeType.BINARY:
            return self._visit_binary(node)
        
        elif node_type == NodeType.UNARY:
            return self._visit_unary(node)
        
        elif node_type == NodeType.GROUPING:
            return self.execute(node.expression)
        
        elif node_type == NodeType.CALL:
            return self._visit_call(node)
        
        elif node_type == NodeType.BLOCK:
            return self._visit_block(node)
        
        elif node_type == NodeType.FUNCTION:
            return self._visit_function(node)
        
        elif node_type == NodeType.IF:
            return self._visit_if(node)
        
        elif node_type == NodeType.WHILE:
            return self._visit_while(node)
        
        elif node_type == NodeType.FOR:
            return self._visit_for(node)
        
        elif node_type == NodeType.RETURN:
            return self._visit_return(node)
        
        elif node_type == NodeType.PRINT:
            return self._visit_print(node)
        
        elif node_type == NodeType.TYPE:
            return self._visit_type(node)
        
        elif node_type == NodeType.LIST:
            return self._visit_list(node)
        
        elif node_type == NodeType.DICT:
            return self._visit_dict(node)
        
        elif node_type == NodeType.INDEX:
            return self._visit_index(node)
        
        elif node_type == NodeType.TRY:
            return self._visit_try(node)
        
        elif node_type == NodeType.BREAK:
            raise BreakLoop()
        
        elif node_type == NodeType.CONTINUE:
            raise ContinueLoop()
        
        elif node_type == NodeType.PASS:
            return None
        
        else:
            raise ArkRuntimeError(f"Unknown node: {node.node_type}", node)
    
    def _visit_assignment(self, node):
        value = self.execute(node.value)
        
        depth = self.current_scope.get_depth(node.target.name)
        
        if depth > 0 and depth == self.current_scope.depth:
            self.current_scope.assign(node.target.name, value)
        else:
            self.current_scope.define(node.target.name, value)
        
        return value
    
    def _visit_identifier(self, node):
        try:
            return self.current_scope.get(node.name)
        except ArkRuntimeError:
            raise ArkRuntimeError(f"Undefined variable: '{node.name}'", node)
    
    def _visit_binary(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)
        op = node.operator
        
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise ArkRuntimeError("Division by zero", node)
            return left / right
        elif op == "%":
            return left % right
        elif op == "**":
            return left ** right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "<":
            return left < right
        elif op == "<=":
            return left <= right
        elif op == ">":
            return left > right
        elif op == ">=":
            return left >= right
        elif op == "and":
            return self._is_truthy(left) and self._is_truthy(right)
        elif op == "or":
            return self._is_truthy(left) or self._is_truthy(right)
        else:
            raise ArkRuntimeError(f"Unknown operator: {op}", node)
    
    def _visit_unary(self, node):
        operand = self.execute(node.operand)
        op = node.operator
        
        if op == "-":
            return -operand
        elif op == "not" or op == "!":
            return not self._is_truthy(operand)
        else:
            raise ArkRuntimeError(f"Unknown unary: {op}", node)
    
    def _visit_call(self, node):
        callee = None
        
        try:
            callee = self.current_scope.get(node.name)
        except ArkRuntimeError:
            if node.name in self.functions:
                callee = self.functions[node.name]
        
        if callee is None:
            raise ArkRuntimeError(f"Undefined: '{node.name}'", node)
        
        args = [self.execute(arg) for arg in node.arguments]
        
        if callable(callee) and not isinstance(callee, Function):
            return callee(*args)
        
        if isinstance(callee, Function):
            return callee(self, *args)
        
        raise ArkRuntimeError(f"Cannot call: {node.name}", node)
    
    def call_user_function(self, func: Function, args: list) -> Any:
        old_scope_idx = self.current_scope_idx
        func_scope = Scope(self.global_scope, is_function=True)
        
        for param_name, arg_value in zip(func.parameters, args):
            func_scope.define(param_name, arg_value)
        
        self.scopes.append(func_scope)
        self.current_scope_idx = len(self.scopes) - 1
        
        try:
            result = None
            for stmt in func.node.body.statements:
                result = self.execute(stmt)
            return result
        except ReturnValue as ret:
            return ret.value
        finally:
            self.scopes.pop()
            self.current_scope_idx = old_scope_idx
    
    def _visit_block(self, node):
        old_scope_idx = self.current_scope_idx
        block_scope = Scope(self.current_scope)
        self.scopes.append(block_scope)
        self.current_scope_idx = len(self.scopes) - 1
        
        result = None
        for stmt in node.statements:
            result = self.execute(stmt)
        
        self.scopes.pop()
        self.current_scope_idx = old_scope_idx
        
        return result
    
    def _visit_function(self, node):
        func = Function(node, self.current_scope)
        self.functions[node.name] = func
        self.global_scope.define(node.name, func)
        return None
    
    def _visit_if(self, node):
        condition = self.execute(node.condition)
        
        if self._is_truthy(condition):
            return self._visit_block(node.then_branch)
        
        for elif_cond, elif_body in node.elif_branches:
            if self._is_truthy(self.execute(elif_cond)):
                return self._visit_block(elif_body)
        
        if node.else_branch:
            return self._visit_block(node.else_branch)
        
        return None
    
    def _visit_while(self, node):
        while self._is_truthy(self.execute(node.condition)):
            old_scope_idx = self.current_scope_idx
            old_scope = self.scopes[old_scope_idx]
            
            for stmt in node.body.statements:
                self.execute(stmt)
            
            if old_scope_idx != self.current_scope_idx:
                self.current_scope_idx = old_scope_idx
        return None
    
    def _visit_for(self, node):
        iterable = self.execute(node.iterable)
        
        if isinstance(iterable, str):
            iterable = list(iterable)
        elif not isinstance(iterable, (list, tuple, dict, range)):
            iterable = list(iterable)
        
        for item in iterable:
            self.current_scope.define(node.variable, item)
            self._visit_block(node.body)
        
        return None
    
    def _visit_return(self, node):
        value = None
        if node.value:
            value = self.execute(node.value)
        raise ReturnValue(value)
    
    def _visit_print(self, node):
        args = [self.execute(arg) for arg in node.arguments]
        output = " ".join(str(a) for a in args)
        print(output)
        return None
    
    def _visit_type(self, node):
        value = self.execute(node.argument)
        print(type(value).__name__)
        return None
    
    def _visit_list(self, node):
        return [self.execute(elem) for elem in node.elements]
    
    def _visit_dict(self, node):
        result = {}
        for key_node, value_node in node.pairs.items():
            key = self.execute(key_node)
            value = self.execute(value_node)
            result[key] = value
        return result
    
    def _visit_index(self, node):
        value = self.execute(node.value)
        index = self.execute(node.index)
        
        if isinstance(value, (list, str, tuple)):
            return value[int(index)]
        elif isinstance(value, dict):
            return value.get(index)
        
        raise ArkRuntimeError(f"Cannot index: {type(value)}", node)
    
    def _visit_try(self, node):
        try:
            self._visit_block(node.try_body)
        except Exception as e:
            old_scope_idx = self.current_scope_idx
            catch_scope = Scope(self.global_scope)
            catch_scope.define(node.variable, str(e))
            self.scopes.append(catch_scope)
            self.current_scope_idx = len(self.scopes) - 1
            
            try:
                self._visit_block(node.catch_body)
            finally:
                self.scopes.pop()
                self.current_scope_idx = old_scope_idx
        
        return None
    
    def _is_truthy(self, value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, (str, list, dict, tuple)):
            return len(value) > 0
        return True


class BreakLoop(Exception):
    pass


class ContinueLoop(Exception):
    pass


class ReturnValue(Exception):
    def __init__(self, value: Any):
        self.value = value
        super().__init__()


def run(source: str) -> Any:
    program = parse(source)
    interpreter = Interpreter()
    return interpreter.interpret(program)


def evaluate(source: str) -> Any:
    program = parse(source)
    interpreter = Interpreter()
    result = None
    for stmt in program.statements:
        result = interpreter.execute(stmt)
    return result


if __name__ == "__main__":
    test_code = '''
x = 10
y = 20

fn add(a, b) (
    return a + b
)

result = add(x, y)
print(result)

if (x < y) (
    print("x is less than y")
)

fn factorial(n) (
    if (n <= 1) (
        return 1
    ) else (
        return n * factorial(n - 1)
    )
)

print(factorial(5))

numbers = [1, 2, 3, 4, 5]
print(numbers[0])
print(len(numbers))
'''
    
    run(test_code)