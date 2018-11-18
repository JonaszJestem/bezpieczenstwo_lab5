import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


with open("sample.html") as page:
    page_content = page.read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            filename = 'sample.html'
        else:
            filename = self.path[1:]

        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            self.send_header('Content-type', 'image/x-icon')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(filename, 'rb') as fh:
                html = fh.read()
                # html = bytes(html, 'utf8')
                self.wfile.write(html)
        except IOError:
            pass
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


httpd = HTTPServer(('localhost', 8080), RequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="privkeyA.pem",
        certfile='certA.crt', server_side=True)

httpd.serve_forever()