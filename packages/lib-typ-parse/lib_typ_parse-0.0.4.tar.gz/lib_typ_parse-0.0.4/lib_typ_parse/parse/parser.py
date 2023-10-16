import lib_typ_parse.utils.exceptions as exceptions
import lib_typ_parse.utils.parsing_utils as parsing_utils

def parse_fxn(code, index, scope):
    K1 = 4
    assert code[index:index+K1] == 'def '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid fxn declaration, closing colon not found')
    s1 = code[index:i1]
    i2 = s1.find('(', 0)
    if i2 == -1:
        exceptions.raise_exception_msgs(code, index, ['Invalid fxn declaration, parenthesis not found', f'Line: {s1}'])
    name = s1[K1:i2].strip()
    arguments = s1[i2:].strip()
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
        'type' : 'fxn',
        'index' : index,
        'name' : name,
        'arguments' : arguments,
        'statements' : statements,
    }
    # print(result, scope)
    # print('def', index, result)
    return result, end_index

# [inherits] grammar; should be consistent with python:;
# [inherits] should only contains internal expression
# 1.) class [className]([inherits]):
# 2.) class [className]:
# parse: [className], [inherits]
def parse_class(code, index, scope):
    # print(code[index:index+5])
    K1 = 6
    assert code[index:index+K1] == 'class '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid class declaration, closing colon not found')

    className = ''
    inherits = ''
    i2 = code.find('(', index, i1)
    # case: "class [className]:"
    if i2 == -1:
        className = code[index+K1:i1].strip()
    # case: "class [className]([inherits]):"
    else:
        i3 = code.find(')', i2, i1)
        if i3 == -1:
            exceptions.raise_exception_msg(code, index, 'Invalid class declaration, closing parenthesis not found')
        className =  code[index+K1:i2].strip()
        inherits = code[i2+1:i3].strip()
    # print(s1)
    # print(className, inherits)
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
        'type' : 'class',
        'index' : index,
        'name' : className,
        'inherits' : inherits,
        'statements' : statements,
    }
    return result, end_index

def parse_try(code, index, scope):
    # print(code[index:index+5])
    K1 = 4
    assert code[index:index+K1] == 'try:'
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid try declaration, closing colon not found')
    # print(s1)
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
        'type' : 'try',
        'index' : index,
        'statements' : statements,
    }
    return result, end_index

def parse_except(code, index, scope):
    # print(code[index:index+5])
    K1 = 7
    assert code[index:index+K1] == 'except '
    i1 = parsing_utils.read_next_cleared_char(code, index, ':')
    if i1 == -1:
        exceptions.raise_exception_msg(code, index, 'Invalid class declaration, closing colon not found')
    s1 = code[index:i1]
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
        'type' : 'except',
        'index' : index,
        'declaration' : s1,
        'statements' : statements,
    }
    return result, end_index


def parse_L1_CE(code, index, scope, token):
    assert code[index:index+len(token)] == token

    # print(token)
    i1 = parsing_utils.read_next_cleared_char(code, index+len(token), ':')

    if i1 == -1:
        exceptions.raise_exception_msg(code, index, f'Invalid {token} declaration, closing colon not found')

    declaration = code[index+len(token):i1].strip()
    statements, end_index = read_scope(code, i1+1, scope+1)
    result = {
        'type' : token,
        'index' : index,
        'declaration' : declaration,
        'statements' : statements,
    }
    return result, end_index

def parse_L0_statement(code, index, scope):
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')

    # case: end of file
    if i1 == -1:
        i1 = len(code)

    expression = code[index:i1]
    result = {
        'type' : 'instruction',
        'index' : index,
        'expression' : expression,
    }
    return result, i1

def parse_import(code, index, scope):
    assert code[index:index+6] == 'import'
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')

    # case: end of file
    if i1 == -1:
        i1 = len(code)

    result = {
        'type' : 'import',
        'index' : index,
        'expression' : code[index:i1],
    }
    return result, i1

def parse_include(code, index, scope):
    assert code[index:index+7] == 'include'
    i1 = parsing_utils.read_next_cleared_char(code, index, '\n')

    # case: end of file
    if i1 == -1:
        i1 = len(code)

    result = {
        'type' : 'include',
        'index' : index,
        'expression' : code[index:i1],
    }
    return result, i1

def parse_abstract_statement(code, index, scope, start_token):
    L2_router = {
        'class' : parse_class,
        'def' : parse_fxn,
    }
    L1_CE_router = {
        'for' : 1,
        'while' : 1,
        'if' : 1,
        'elif' : 1,
        'else' : 1,
    }
    L1_special_items = {
        'try' : parse_try,
        'except' : parse_except,
    }
    L0_misc_router = {
        'import' : parse_import,
        'include' : parse_include,
    }
    if start_token in L2_router:
        return L2_router[start_token](code, index, scope)
    if start_token in L1_special_items:
        return L1_special_items[start_token](code, index, scope)
    if start_token in L1_CE_router:
        return parse_L1_CE(code, index, scope, start_token)
    if start_token in L0_misc_router:
        return L0_misc_router[start_token](code, index, scope)

    return parse_L0_statement(code, index, scope)

def read_scope(code, index, scope):
    result = []
    # print(code[index - 5 : index + 5])
    # print('\n' * 10)
    N = int(10 ** 4)
    ctr = 0
    while True and ctr < N:
        start_token, i1 = parsing_utils.read_init_token(code, index, scope)
        # print(code[i1-len(start_token):i1], scope)
        # print(start_token, scope)
        # print(start_token)
        # print(i1)
        if start_token == '#':
            i1 = code.find('\n', i1)
            if i1 == -1:
                return result, len(code)
            index = i1
            continue
        if start_token in ['EOF', 'EOS']:
            return result, i1
        assert start_token == code[i1-len(start_token):i1]
        abstract_statement, index = parse_abstract_statement(code, i1 - len(start_token), scope, start_token)
        # print(abstract_statement)
        # print(index)
        result.append(abstract_statement)
        ctr += 1

    raise Exception('parse timeout')
    # print(code)
