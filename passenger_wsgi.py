from a2wsgi import ASGIMiddleware
from init import app
application = ASGIMiddleware(app)