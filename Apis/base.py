import logging

import webapp2

from webapp2_extras import sessions

logging.getLogger().setLevel(logging.DEBUG)


class ShingHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    def dispatch(self):  # override dispatch
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)       # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend="datastore")


class ApiChecker():
	pass


def request_logger():
	pass