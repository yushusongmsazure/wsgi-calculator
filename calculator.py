"""
Yushu Song
Assignment 4
"""

import traceback

def homepage():
    '''
    Display home page
    '''
    body = ['<h1>Here is how to use this page...</h1>']
    body.append('<h3>Add:      http://localhost:8080/add/23/42      </h3>')
    body.append('<h3>Multiply: http://localhost:8080/multiply/12/5  </h3>')
    body.append('<h3>Divide:   http://localhost:8080/divide/75/5    </h3>')
    body.append('<h3>Subtract: http://localhost:8080/subtract/22/2  </h3>')

    return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    total = sum(map(int, args))
    return str(total)

def multiply(*args):
    """ Returns a STRING with the result of the arguments doing multiplication """

    left_op = int(args[0])
    right_op = int(args[1])

    return str(left_op * right_op)

def subtract(*args):
    """ Returns a STRING with the result of the arguments doing subtraction """

    left_op = int(args[0])
    right_op = int(args[1])

    return str(left_op - right_op)

def divide(*args):
    """ Returns a STRING with the division of the arguments """

    left_op = int(args[0])
    right_op = int(args[1])

    return str(left_op / right_op)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': homepage,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Numerator Cannot Be Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
