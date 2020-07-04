from http.server import BaseHTTPRequestHandler, HTTPServer
import re

def handler( handle, connection_timeout=None ):
	def send(request,code,headers,body):

		request.send_response(code)

		for header, value in headers.items():
			request.send_header(header,value)
		request.end_headers()

		request.wfile.write(body)

	class Handler(BaseHTTPRequestHandler):
		timeout = connection_timeout
		method = None
		def __getattr__(self,name):
			self.method = re.match(r'do_(.*)',name).group(1) # raises AttributeError if no match
			return lambda: send(self,**handle(self))
	return Handler

def response(body=b'',code=200,headers={}):
	defaultHeaders = {
		'Content-type': 'text/html; charset=utf-8',
		'Content-Length': len(body),
	}
	defaultHeaders.update(headers)

	return {
		'code':code,
		'headers': defaultHeaders,
		'body': body,
	}

from urllib.parse import urlparse, parse_qsl
import cgi
def getBody(request):
	print(request.headers)
	return request.rfile.read(int(request.headers['Content-Length']))
def query(request):
	if request.command == 'GET':
		return dict(parse_qsl(urlparse(request.path).query))
	else:
		return cgi.FieldStorage(
			request.rfile,
			request.headers,
			environ={
				'REQUEST_METHOD':request.command,
			},
			keep_blank_values=1,
		)
import mimetypes
mimetypes.init()
def static(path):
	type_,encoding = mimetypes.guess_type(path)
	with open(path,'rb') as fp:
		return response(
			fp.read(),
			200,
			{
				'Content-type':type_,
			}
		)
def server( ip, port, get, post, certDir =None ):
	output  = HTTPServer(
		(ip,port),
		handler(get=get,post=post)
	)
	if certDir != None:
		import  ssl
		server.socket = ssl.wrap_socket(
			server.socket,
			keyfile = certDir+'privkey.pem',
			certfile = certDir+'cert.pem',
			server_side = True,
		)
	return output


from socketserver import ThreadingMixIn
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def hello(request):
	name = getQuery(request.path)['name']
	return  response(f"hello {name}".encode())

def echo(request):
	return response(getBody(request));

