import ast
import inspect
import os
from typing import Callable, cast


def ast_parse_lambda(f: Callable):
    """This kind of detailed checking is perhaps overkill and it is almost impossible to get
    the source code of a lambda function. We'll just try to get it and ast parse it, if it
    fails, there are other checks beyond this.

    This will check if the expression is a simple Equate
    """
    source = inspect.getsource(f)
    if "lambda:" not in source:
        raise TypeError(f"Function {f} is not a lambda function")
    try:
        lambda_source = _get_short_lambda_source(f)
    except Exception:
        return
    if not lambda_source:
        return
    tree = ast.parse(lambda_source)
    if len(tree.body) != 1:
        raise TypeError
    expression = cast(ast.Expression, tree.body[0])
    if not isinstance(expression.value, ast.Compare):
        raise TypeError
    if not isinstance(expression.value.ops[0], ast.Eq):
        raise TypeError


def _get_short_lambda_source(lambda_func: callable):
    """Return the source of a (short) lambda function.
    If it's impossible to obtain, returns None.

    see http://xion.io/post/code/python-get-lambda-code.html
    """
    try:
        source_lines, _ = inspect.getsourcelines(lambda_func)
    except (IOError, TypeError):
        return None

    # skip `def`-ed functions and long lambdas
    if len(source_lines) != 1:
        return None

    source_text = os.linesep.join(source_lines).strip()

    # find the AST node of a lambda definition
    # so we can locate it in the source code
    source_ast = ast.parse(source_text)
    lambda_node = next((node for node in ast.walk(source_ast) if isinstance(node, ast.Lambda)), None)
    if lambda_node is None:  # could be a single line `def fn(x): ...`
        return None

    # HACK: Since we can (and most likely will) get source lines
    # where lambdas are just a part of bigger expressions, they will have
    # some trailing junk after their definition.
    #
    # Unfortunately, AST nodes only keep their _starting_ offsets
    # from the original source, so we have to determine the end ourselves.
    # We do that by gradually shaving extra junk from after the definition.
    lambda_text = source_text[lambda_node.col_offset :]
    lambda_body_text = source_text[lambda_node.body.col_offset :]
    min_length = len("lambda:_")  # shortest possible lambda expression
    while len(lambda_text) > min_length:
        try:
            # What's annoying is that sometimes the junk even parses,
            # but results in a *different* lambda. You'd probably have to
            # be deliberately malicious to exploit it but here's one way:
            #
            #     bloop = lambda x: False, lambda x: True
            #     get_short_lamnda_source(bloop[0])
            #
            # Ideally, we'd just keep shaving until we get the same code,
            # but that most likely won't happen because we can't replicate
            # the exact closure environment.
            code = compile(lambda_body_text, "<unused filename>", "eval")

            # Thus the next best thing is to assume some divergence due
            # to e.g. LOAD_GLOBAL in original code being LOAD_FAST in
            # the one compiled above, or vice versa.
            # But the resulting code should at least be the same *length*
            # if otherwise the same operations are performed in it.
            if len(lambda_body_text.split(",")) > 1:
                return lambda_body_text.split(",")[0]
            return lambda_body_text
        except SyntaxError:
            pass
        lambda_text = lambda_text[:-1]
        lambda_body_text = lambda_body_text[:-1]

    return None
