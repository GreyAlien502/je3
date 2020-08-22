from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import copy

def handler( handle, connection_timeout=None ):
	def send(request,code,headers,body):

		request.send_response(code)

		for header, value in headers.items():
			request.send_header(header,value)
		request.end_headers()

		request.wfile.write(body)

	class Handler(BaseHTTPRequestHandler):
		timeout = connection_timeout
		def __getattr__(self,name):
			if re.match(r'do_(.*)',name):
				return lambda: send(self,**handle(self))
			else:
				raise AttributeError()
	return Handler

def response(body=b'',code=200,headers={}):
	defaults = {
		'Content-type': 'text/html; charset=utf-8',
		'Content-Length': len(body),
	}
	headers = copy.copy(headers)
	for key,value in defaults.items():
		if not key in headers:
			headers[key] = value
	return {
		'code':code,
		'headers': headers,
		'body': body,
	}

from urllib.parse import urlparse, parse_qsl
import cgi
def getBody(request):
	return request.rfile.read(int(request.headers['Content-Length']))
def query(request):
	return dict(parse_qsl(urlparse(request.path).query))
def body(request):
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

