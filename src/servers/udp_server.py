import socketserver

from src.server_config import UDP_PORT


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        print(data[:1])


if __name__ == "__main__":
    try:
        with socketserver.ThreadingUDPServer(
            ("0.0.0.0", UDP_PORT), UDPHandler
        ) as server:
            server.allow_reuse_address = True
            print(f"UDP Server listening on 0.0.0.0:{UDP_PORT}")
            server.serve_forever()
    except KeyboardInterrupt:
        print("Script stopped")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
