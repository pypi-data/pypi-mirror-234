from traceback import extract_stack

def prindent(*args, **kwargs):
    if 'indent' in kwargs:
        indent = kwargs['indent']
        del kwargs['indent']
    else:
        indent = '    '

    line = extract_stack()[-2]._original_line
    if line.startswith(' '):
        depth = (len(line) - len(line.lstrip(' '))) // 4
    elif line.startswith('\t'):
        depth = len(line) - len(line.lstrip('\t'))
    else:
        depth = 0

    indent_str = indent * depth
    new_line_indent = '\n' + indent_str
    args = [str(arg).replace('\n', new_line_indent) for arg in args]
    if args:
        args[0] = indent_str + args[0]

    print(*args, **kwargs)
