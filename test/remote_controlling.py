"""It's a try of creating server on Raspberry pi"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from motors import robot
import json


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global html

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        try:
            if self.path == "/motors":
                data_dict = json.loads(body.decode('utf-8'))
                if data_dict['direction'] == 1:
                    robot.forward()

                elif data_dict['direction'] == 2:
                    robot.backward()

                elif data_dict['direction'] == 3:
                    robot.right()

                elif data_dict['direction'] == 4:
                    robot.left()

                else:
                    robot.stop()

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(400, 'Bad Request: Method does not exist')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
        except Exception as err:
            print("do_POST exception: %s" % str(err))


def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    port = 4444

    with open('index.html', 'r') as file:
        html = file.read()

    server_thread(port)
