import socket
import random
import time
import threading


# server_ip = "ec2-15-164-95-106.ap-northeast-2.comp ute.amazonaws.com"
# server_port = 55555
server_ip = "127.0.0.1"
server_port = 8888


def client(client_id):
    time.sleep(random.randint(1, 5))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print(f"Client {client_id}: start!!")

    try:
        with open(f"Client{client_id}.txt", "w") as f:

            while True:
                problem = client_socket.recv(1024).decode()
                if not problem:
                    break

                r_line = f"Client {client_id}: Received problem: {problem}"
                print(r_line)
                f.write(r_line + ', ')
                time.sleep(random.randint(1, 5))
                result = eval(problem)

                if isinstance(result, int):
                    s_line = f"Client {client_id}: Solved problem: {problem} = {result}"
                    print(s_line)
                    f.write(s_line + '\n')
                    client_socket.send(str(result).encode())
                if isinstance(result, float):
                    result_f = round(result, 6)
                    s_line = f"Client {client_id}: Solved problem: {problem} = {result_f}"
                    print(s_line)
                    f.write(s_line + '\n')
                    client_socket.send(str(result_f).encode())

    except ConnectionResetError:
        with open(f"Client{client_id}.txt", "w") as f:
            e_line = f"Client {client_id}: Connection to the server was forcibly closed."
            print(e_line)
            f.write(e_line)
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
