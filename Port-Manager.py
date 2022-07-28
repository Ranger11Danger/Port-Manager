import socket
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p",metavar="port", type=int ,required=True, help="Port to listen for connections on")
args = parser.parse_args()

def forward(src, dst):
    while True:
        data = src.recv(1024)
        dst.send(data)

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('127.0.0.1', args.p))
        s.listen(5)
        print(f"[+] Listening for connections on 127.0.0.1:{args.p}")
    except:
        print(f"[+] Unable to bind to 127.0.0.1:{args.p}")


    while True:
        client_socket, client_address = s.accept()

        print(f"[+] Incomming Connection on Port {args.p}")
        response = input("Do you want to forward this connection?(y/n): ")
        if response == 'y':

            address = input("Where do you want to forward this connection?(ip:port): ")
            address = address.split(":")

            while True:
                try:
                    remote_socket = socket.create_connection((address[0], int(address[1])))
                    print(f"[+] Connected to {address[0]}:{address[1]}")
                    break
                except:
                    print(f"[+] Unable to connect to {address[0]}:{address[1]}")
                    response = input('Do you want to connect to a different address?(y/n): ')
                    if response == 'y':
                        address = input("Where do you want to forward this connection?(ip:port): ")
                        address = address.split(":")
                    else:
                        client_socket.close()
                        continue


            Thread1 = threading.Thread(target=forward, args=(client_socket, remote_socket))
            Thread2 = threading.Thread(target=forward, args=(remote_socket, client_socket))
            Thread1.daemon = True
            Thread2.daemon = True
            Thread1.start()
            Thread2.start()
            print(f"[+] Forwarding connection from 127.0.0.1:{args.p} -> {address[0]}:{address[1]}")
        else:
            print("[+] Dropping Connection...")
            client_socket.close()
if __name__ == "__main__":
    main()
