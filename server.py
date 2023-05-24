import socket
from config import IP, PORT, receive_data, send_data, generate_request
from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, PORT))
    s.listen(5)
    while True:
        client_socket, address = s.accept()
        print(f"CONNECTED WITH {address[0]}:{address[1]}")


        def hello_from_client():
            hello_from_client = receive_data(client_socket).strip()
            hello_from_client = hello_from_client.replace(r"SEND\r\nmess: ", "")
            print(hello_from_client)


        def hello_to_client():
            hello_to_client = generate_request(mode="send", message=f"HELLO")
            send_data(client_socket, hello_to_client)


        def get_request_from_client():
            request_from_client = receive_data(client_socket).strip()
            request_from_client = request_from_client.replace(r"CALCULATE\r\n", "")
            request_from_client = request_from_client.split(r"\r\n")
            function = request_from_client[0][6:]
            low_limit = request_from_client[1][5:]
            upper_limit = request_from_client[2][5:]
            return function, low_limit, upper_limit


        def calculate_integral(function, low_limit, upper_limit):
            result = quad(lambda x: eval(function), float(low_limit), float(upper_limit))[0]
            return result


        def display_result_integral(result):
            result = f"Całka wynosi {result}"
            response = generate_request(mode="send", message=result)
            send_data(client_socket, response)


        def draw_integral(function, lower_limit, upper_limit):
            lower_limit = float(lower_limit)
            upper_limit = float(upper_limit)
            x = np.linspace(lower_limit, upper_limit, 1000)
            y = lambda x: eval(function)
            y_values = y(x)
            plt.plot(x, y_values)
            plt.fill_between(x, y_values, where=[(x > lower_limit) & (x < upper_limit) for x in x], alpha=0.5)
            plt.title(f"Wykres funkcji f(x) oraz całki w przedziale [{int(lower_limit)}, {int(upper_limit)}]")
            chart_filename = "chart.png"
            plt.savefig(chart_filename)

            with open(chart_filename, "rb") as f:
                binary_image = f.read()
                print()
                request = generate_request(mode="send_image", message=binary_image)
                send_data(client_socket, request, mode='img')


        hello_to_client()
        hello_from_client()
        function, low_limit, upper_limit = get_request_from_client()
        print(f"Wzór funckji: {function}\r\nDolna granica: {low_limit}\r\nGórna granica: {upper_limit}")
        result = calculate_integral(function, low_limit, upper_limit)
        display_result_integral(result)
        draw_integral(function, low_limit, upper_limit)
