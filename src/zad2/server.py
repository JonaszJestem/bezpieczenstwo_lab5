import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


with open("sample.html") as page:
    page_content = page.read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(page_content, 'utf-8'))


    def do_POST(self):
        print(self.headers)
        length = int(self.headers['content-length'])
        postvars = cgi.parse_qs(
                self.rfile.read(length),
                keep_blank_values=1)
        print(postvars)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(page_content, 'utf-8'))


httpd = HTTPServer(('localhost', 3000), RequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="privkeyA.pem",
        certfile='certA.crt', server_side=True)

httpd.serve_forever()