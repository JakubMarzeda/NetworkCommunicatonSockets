import socket
from config import IP, PORT, send_data, receive_data, generate_request

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))


    def hello_from_server():
        hello_from_server = receive_data(s).strip()
        hello_from_server = hello_from_server.replace(r"SEND\r\nmess: ", "")
        print(hello_from_server)


    def hello_to_server():
        hello_to_server = generate_request(mode="send", message="HELLO")
        send_data(s, hello_to_server)


    def send_request(request):
        request = request.split(" ")
        request = generate_request(mode="calculate", function=request[0], lower_limit=request[1],
                                   upper_limit=request[2])
        if request == "Incorrect function":
            return "Incorrect function"
        elif request == "Incorrect compartment":
            return "Incorrect compartment"
        else:
            send_data(s, request)


    def get_result_chart():
        response_integral = receive_data(s).strip()
        response_integral = response_integral.replace(r"SEND\r\nmess: ", "")
        print(response_integral)


    def get_image_chart():
        response_chart = receive_data(s, mode="img")
        response_chart = response_chart.replace("SEND_IMAGE\r\nIMG: ", "")
        with open("chart.png", "wb") as f:
            f.write(response_chart)


    hello_to_server()
    hello_from_server()
    request = input("Podaj wzór funkcji oraz przedział (wzór funkcji, od, do)... ").strip()
    while True:
        if send_request(request) == "Incorrect function" or send_request(request) == "Incorrect compartment":
            request = input("Podaj wzór funkcji oraz przedział (wzór funkcji, od, do)... ").strip()
        else:
            send_request(request)
            break
    get_result_chart()
