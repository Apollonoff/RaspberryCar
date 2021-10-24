"""It's a try of creating server on Raspberry pi"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from motors import robot
import json
from threading import Condition
from io import BytesIO
from socketserver import ThreadingMixIn
from picamera import PiCamera
from logging import warning


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # global html

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(html)))
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', '0')
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(frame)))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

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


class StreamingServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def server_thread(port):
    with PiCamera(resolution='640x480', framerate=24) as camera:
        camera.start_recording(output, format='mjpeg')
        try:
            server_address = ('', port)
            httpd = StreamingServer(server_address, ServerHandler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
        finally:
            camera.stop_recording()


if __name__ == '__main__':
    port = 80
    output = StreamingOutput()

    with open('index.html', 'r') as file:
        html = file.read()

    server_thread(port)
