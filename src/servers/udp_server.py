import socketserver

from src.server_config import UDP_PORT


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        print(data[:1])


if __name__ == "__main__":
    with socketserver.ThreadingUDPServer(("0.0.0.0", UDP_PORT), UDPHandler) as server:
        server.allow_reuse_address = True
        print(f"UDP Server listening on 0.0.0.0:{UDP_PORT}")
        server.serve_forever()
