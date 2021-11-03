import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

timeout = 42

class SessionMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if request.user.is_authenticated:
			request.session.set_expiry(60 * 60 * 24 * 30)
			return

		if not request.session.get("session_timeout"):
			request.session["session_timeout"] = time.time()
		expired_time = time.time() - request.session["session_timeout"]
		if expired_time > timeout:
			request.session.flush()
		else:
			request.session.set_expiry(int(timeout - expired_time))
