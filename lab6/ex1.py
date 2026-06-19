import re


def tokenize(expr):
    return re.findall(r'\d+|[+\-*()]', expr)


def parse_factor(tokens, pos):
    if tokens[pos] == '(':
        val, pos = parse_expr(tokens, pos + 1)
        return val, pos + 1
    return int(tokens[pos]), pos + 1


def parse_term(tokens, pos):
    left, pos = parse_factor(tokens, pos)
    if pos < len(tokens) and tokens[pos] == '*':
        right, pos = parse_term(tokens, pos + 1)
        return left * right, pos
    return left, pos


def parse_expr(tokens, pos):
    left, pos = parse_term(tokens, pos)
    # BUG: right-recursive, so "10 - 3 - 2" parses as 10 - (3 - 2) = 9
    # Fix: use a loop for left-associativity
    while pos < len(tokens) and tokens[pos] in ('+', '-'):
        op = tokens[pos]
        right, pos = parse_term(tokens, pos + 1)
        if op == '+':
            left += right
        else:
            left -= right
    return left, pos


def evaluate(expr):
    tokens = tokenize(expr)
    result, _ = parse_expr(tokens, 0)
    return result


tests = [
    ("2 + 3",         5),
    ("2 * 3 + 1",     7),
    ("10 - 3 - 2",    5),
    ("(10 - 3) * 2",  14),
]

for expr, expected in tests:
    result = evaluate(expr)
    status = "OK" if result == expected else "ERROR"
    print(f"{expr:>16} = {result:<4}  expected {expected:<4} [{status}]")
