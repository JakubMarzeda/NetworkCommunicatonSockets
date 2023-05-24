from sympy import Symbol, sympify, Expr

IP = '127.0.0.1'
PORT = 55874


def receive_data(socket, mode="text"):
    if mode == "text":
        data = b""
        while b"\r\n\r\n" not in data:
            data += socket.recv(1)

        return data.decode()
    else:
        data = b""
        while b"\r\n\r\n" not in data:
            data += socket.recv(1)

        return data


def send_data(socket, message, mode='text'):
    if mode == 'text':
        message = message.encode()
        message += b"\r\n\r\n"
        socket.sendall(message)
    if mode == 'img':
        message += b"\r\n\r\n"
        socket.sendall(message)


def is_math_function(string):
    try:
        x = Symbol('x')
        expr = sympify(string)
        variables = expr.free_symbols
        for variable in variables:
            if str(variable) != "x":
                return False
        return isinstance(expr, Expr)
    except:
        return False


def generate_request(mode=None, function=None, lower_limit=None, upper_limit=None, message=None):
    request = ""
    if mode == "calculate":
        request += r"CALCULATE\r\n"
        if function is not None:
            if is_math_function(function):
                request += rf"FUNC: {function}\r\n"
            else:
                return "Incorrect function"
        else:
            return "Incorrect function"

        if lower_limit and (lower_limit[1:].isdigit() if lower_limit.startswith("-") else lower_limit.isdigit()):
            request += rf"LOW: {lower_limit}\r\n"
        else:
            return "Incorrect compartment"

        if upper_limit and (upper_limit[1:].isdigit() if upper_limit.startswith("-") else upper_limit.isdigit()):
            request += rf"UPP: {upper_limit}"
        else:
            return "Incorrect compartment"
    elif mode == "send":
        request += r"SEND\r\n"
        if message:
            request += f"mess: {message}"
    elif mode == "send_image":
        request += rf"SEND_IMAGE\r\nIMG: {message}"
        request = request.encode()
    return request

# print(generate_request(mode="calculate", function="x**3", lower_limit="12", upper_limit="100"))
# CALCULATE/r/nFUNC: x**3/r/nLOW: 12/r/nUPP: 100