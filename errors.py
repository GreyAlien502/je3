import traceback

from .server import response

class HTTPError(Exception):
	def __init__(self,code,message=None):
		if message == None:
			message = {
				400: '''\
				400 Bad Request

				   The 400 (Bad Request) status code indicates that the server cannot or
				   will not process the request due to something that is perceived to be
				   a client error (e.g., malformed request syntax, invalid request
				   message framing, or deceptive request routing).
				''',
				404: '''\
				404 Not Found

				   The 404 (Not Found) status code indicates that the origin server did
				   not find a current representation for the target resource or is not
				   willing to disclose that one exists.  A 404 status code does not
				   indicate whether this lack of representation is temporary or
				   permanent; the 410 (Gone) status code is preferred over 404 if the
				   origin server knows, presumably through some configurable means, that
				   the condition is likely to be permanent.
				''',
				413: '''\
				413 Payload Too Large

				   The 413 (Payload Too Large) status code indicates that the server is
				   refusing to process a request because the request payload is larger
				   than the server is willing or able to process.  The server MAY close
				   the connection to prevent the client from continuing the request.
				''',
				415: '''\
				415 Unsupported Media Type

				   The 415 (Unsupported Media Type) status code indicates that the
				   origin server is refusing to service the request because the payload
				   is in a format not supported by this method on the target resource.
				   The format problem might be due to the request's indicated
				   Content-Type or Content-Encoding, or as a result of inspecting the
				   data directly.
				''',
				500: '''\
				500 Internal Server Error

				   The 500 (Internal Server Error) status code indicates that the server
				   encountered an unexpected condition that prevented it from fulfilling
				   the request.
				'''
			}[code]
		self.code = code
		self.message =  message
	def response(self):
		return response(self.message.encode(),self.code)

def handle_errors(function):
	def wrapped(*args,**kwargs):
		try:
			return function(*args,**kwargs)
		except HTTPError as e:
			return e.response()
		except Exception as e:
			traceback.print_exc()
			return HTTPError(500).response()
	return wrapped

