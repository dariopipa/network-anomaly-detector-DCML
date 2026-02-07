import socketserver
from src.server_config import TCP_PORT

# https://realpython.com/python-sockets/#tcp-sockets
# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingTCPServer


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(4096)
            print(data[:1])
            if not data:
                break


if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("0.0.0.0", TCP_PORT), TCPHandler) as server:
        server.allow_reuse_address = True
        print(f"TCP Server listening on 0.0.0.0:{TCP_PORT}")
        server.serve_forever()
