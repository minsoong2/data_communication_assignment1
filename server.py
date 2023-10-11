import socket
import threading
import random
import time


ip = '127.0.0.1'
port = 8888
system_clock = 0
server_operating_time = 600
total_sum = 0
f = open("Server.txt", "w")


def update_system_clock():
    global system_clock
    while system_clock < server_operating_time:
        time.sleep(1)
        system_clock += 1


def generate_problem():
    num1 = random.randint(0, 100)
    num2 = random.randint(0, 100)
    num3 = random.randint(0, 100)
    oper1 = random.choice(["+", "-", "*", "/"])
    oper2 = random.choice(["+", "-", "*", "/"])

    if oper1 == '/' and num2 == 0:
        num2 = random.randint(1, 100)
    if oper2 == '/' and num3 == 0:
        num3 = random.randint(1, 100)

    problem = f"{num1} {oper1} {num2} {oper2} {num3}"
    return problem, eval(problem)


def generate_and_send_problem(client_socket):
    global system_clock, total_sum
    while system_clock < server_operating_time:
        problem, correct_answer = generate_problem()
        client_socket.send(problem.encode())
        f.write(f"System Clock {system_clock}s: Send problem to Client{client_socket} : {problem}" + '\n')

        if isinstance(correct_answer, int):
            response = int(client_socket.recv(1024).decode())

            if response == correct_answer:
                c_answer = f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered correctly: {problem} = {response}"
                print(c_answer)
                f.write(c_answer + '\n')
                time.sleep(random.randint(1, 5))
            else:
                c_answer = f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered incorrectly: {problem} = {response} Repeating problem."
                print(c_answer)
                f.write(c_answer + '\n')
                time.sleep(1)

                client_socket.send(problem.encode())
                f.write(f"System Clock {system_clock}s: Send problem to Client{client_socket} : {problem}" + '\n')
                response = int(client_socket.recv(1024).decode())
                if response == correct_answer:
                    c_answer = f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam success!!!"
                    print(c_answer)
                    f.write(c_answer + '\n')
                else:
                    c_answer = f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam fail!!!"
                    print(c_answer)
                    f.write(c_answer + '\n')

            total_sum += response

        if isinstance(correct_answer, float):
            response = float(client_socket.recv(1024).decode())
            correct_answer = round(correct_answer, 6)

            if response == correct_answer:
                c_answer = f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered correctly: {problem} = {response}"
                print(c_answer)
                f.write(c_answer + '\n')
                time.sleep(random.randint(1, 5))
            else:
                c_answer = f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered incorrectly: {problem} = {response} Repeating problem."
                print(c_answer)
                f.write(c_answer + '\n')
                time.sleep(1)

                client_socket.send(problem.encode())
                f.write(f"System Clock {system_clock}s: Send problem to Client{client_socket} : {problem}" + '\n')
                response = float(client_socket.recv(1024).decode())
                if response == correct_answer:
                    c_answer = f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam success!!!"
                    print(c_answer)
                    f.write(c_answer + '\n')
                else:
                    c_answer = f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam fail!!!"
                    print(c_answer)
                    f.write(c_answer + '\n')

            total_sum += response


def handle_client(client_socket):
    global system_clock
    try:
        while system_clock < server_operating_time:
            system_clock += 1
            generate_and_send_problem(client_socket)
    except Exception as e:
        e_line = f"Error: {e}"
        print(e_line)
        f.write(e_line + '\n')
    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(4)
    server.settimeout(1)

    listen = "Server is listening..."
    print(listen)
    f.write(listen + '\n')

    threads = []
    clock_thread = threading.Thread(target=update_system_clock)
    clock_thread.daemon = True
    clock_thread.start()

    client_count = 0

    while system_clock < server_operating_time:
        if system_clock >= server_operating_time:
            break
        try:
            client_socket, client_address = server.accept()
            accept = f"Accepted connection from {client_address}"
            print(accept)
            f.write(accept + '\n')
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
            threads.append(client_handler)
            client_count += 1
        except socket.timeout:
            pass

    for thread in threads:
        thread.join()

    print_total_sum = f"total_sum: {round(total_sum, 6)}"
    print_system_clock = f"end_time: {system_clock}"
    print(print_total_sum)
    print(print_system_clock)
    f.write(print_total_sum + '\n')
    f.write(print_system_clock + '\n')
    server.close()
    print("Server closed...")
    f.write("Server closed...")
    if client_count == 0:
        print("No clients connected during the 30 seconds.")
        f.write("No clients connected during the 30 seconds.")


if __name__ == "__main__":
    main()