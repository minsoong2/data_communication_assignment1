import socket
import random
import time
import threading


# server_ip = "ec2-15-164-95-106.ap-northeast-2.compute.amazonaws.com"
# server_port = 55555
server_ip = "127.0.0.1"
server_port = 8888


def client(client_id):
    time.sleep(random.randint(1, 5))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_id}: start!!")

    try:
        while True:
            problem = client_socket.recv(1024).decode()
            if not problem:
                break

            print(f"Client {client_id}: Received problem: {problem}")
            time.sleep(random.randint(1, 5))
            result = eval(problem)

            if isinstance(result, int):
                print(f"Client {client_id}: Solved problem: {problem} = {result}")
                client_socket.send(str(result).encode())
            if isinstance(result, float):
                result_f = round(result, 6)
                print(f"Client {client_id}: Solved problem: {problem} = {result_f}")
                client_socket.send(str(result_f).encode())

    except ConnectionResetError:
        print(f"Client {client_id}: Connection to the server was forcibly closed.")
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    client_threads = []
    for i in range(1, 5):
        client_thread = threading.Thread(target=client, args=(i,))
        client_threads.append(client_thread)

    for thread in client_threads:
        thread.start()
        print(thread, "start!!!")

    for thread in client_threads:
        thread.join()
