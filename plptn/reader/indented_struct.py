"""read a configuration file as nested dict
for a structure foo, it starts with a line "structure foo", and ends with "endstructure"
assignment of attribute is done with "=" sign
"""
from typing import Dict, Union, Iterator, Any, Tuple, Optional

Token = Tuple[str, Optional[str], Union[type(None), str, Tuple[str, Any]]]


def atom(next_func: Iterator[str], token: Token) -> (str, Union[float, int, str, Dict]):
    if token[0] == 'struct_start':
        out_key = token[1]
        out = dict()
        token = read_line(next_func)
        while token[0] != 'struct_end':
            key, value = atom(next_func, token)
            out[key] = value
            token = read_line(next_func)
        return out_key, out
    elif token[0] == 'assignment':
        return token[1], token[2]
    raise SyntaxError("malformed expression ({0})".format(token[0]))


def convert(x: str) -> Union[str, int, float]:
    try:
        result = int(x)
    except ValueError:
        try:
            result = float(x)
        except ValueError:
            result = x
    return result


def read_line(source: Iterator[str]) -> Token:
    line = next(source)
    tokens = line.split()
    while len(tokens) == 0:
        line = next(source)
        tokens = line.split()
    # noinspection SpellCheckingInspection
    if len(tokens) > 1 and tokens[0] == 'structure':
        return 'struct_start', tokens[1], None
    elif len(tokens) == 1 and tokens[0] == 'endstructure':
        return 'struct_end', None, None
    else:
        tokens = [token.strip(' \'\"') for token in ''.join(tokens).split('=')]
        return 'assignment', tokens[0], convert(tokens[1])


def read(file_path: str) -> Dict:
    fp = open(file_path, 'r')
    key, value = atom(fp, read_line(fp))
    assert key == 'state'
    return value
