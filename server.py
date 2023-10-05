import socket
import threading
import random
import time

ip = '127.0.0.1'
port = 8888
system_clock = 0
total_sum = 0


def update_system_clock():
    global system_clock
    while system_clock < 30:
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
    while system_clock < 30:
        problem, correct_answer = generate_problem()
        client_socket.send(problem.encode())

        if isinstance(correct_answer, int):
            response = float(client_socket.recv(1024).decode())

            if response == correct_answer:
                print(
                    f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered correctly: {problem} = {response}")
                time.sleep(random.randint(1, 5))
            else:
                print(
                    f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered incorrectly: {problem} = {response}. Repeating problem.")
                time.sleep(1)
                client_socket.send(problem.encode())
                response = client_socket.recv(1024).decode()
                if response == correct_answer:
                    print(f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam success!!!")
                else:
                    print(f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam fail!!!")

            total_sum += response

        if isinstance(correct_answer, float):
            response = float(client_socket.recv(1024).decode())
            correct_answer = round(correct_answer, 6)

            if response == correct_answer:
                print(
                    f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered correctly: {problem} = {response}")
                time.sleep(random.randint(1, 5))
            else:
                print(
                    f"System Clock {system_clock}s: Client {client_socket.getpeername()} answered incorrectly: {problem} = {response}. Repeating problem.")
                time.sleep(1)
                client_socket.send(problem.encode())
                response = float(client_socket.recv(1024).decode())
                if response == correct_answer:
                    print(f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam success!!!")
                else:
                    print(f"System Clock {system_clock}s: {client_socket.getpeername()} : Re-exam fail!!!")

            total_sum += response


def handle_client(client_socket):
    global system_clock
    try:
        while system_clock < 30:
            system_clock += 1
            generate_and_send_problem(client_socket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(4)

    print("Server is listening...")

    threads = []
    clock_thread = threading.Thread(target=update_system_clock)
    clock_thread.daemon = True
    clock_thread.start()

    for _ in range(4):
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        threads.append(client_handler)

    for thread in threads:
        thread.join()

    print("total_sum:", round(total_sum, 6))
    print("time:", system_clock)
    server.close()


if __name__ == "__main__":
    main()
