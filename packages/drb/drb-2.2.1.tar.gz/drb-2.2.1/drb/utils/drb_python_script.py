from drb.core import DrbNode
import ast
import copy


# code from https://stackoverflow.com/questions/33409207
def _convert_expr2expression(expr) -> ast.Expression:
    expr.lineno = 0
    expr.col_offset = 0
    result = ast.Expression(expr.value, lineno=0, col_offset=0)
    return result


# code from https://stackoverflow.com/questions/33409207
# updated to include the current node in the execution context
def exec_with_return(code: str, node: DrbNode, **kwargs):
    code_ast = ast.parse(code)

    init_ast = copy.deepcopy(code_ast)
    init_ast.body = code_ast.body[:-1]

    last_ast = copy.deepcopy(code_ast)
    last_ast.body = code_ast.body[-1:]

    my_globals = globals()
    my_globals['node'] = node
    for k, v in kwargs.items():
        my_globals[k] = v

    exec(compile(init_ast, "<ast>", "exec"), my_globals)
    if type(last_ast.body[0]) is ast.Expr:
        return eval(compile(_convert_expr2expression(last_ast.body[0]),
                            "<ast>", "eval"), my_globals)
    else:
        exec(compile(last_ast, "<ast>", "exec"), my_globals)
