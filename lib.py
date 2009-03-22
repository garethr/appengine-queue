from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class BaseRequest(webapp.RequestHandler):
    def _extra_context(self, context):        
        extras = {
        }
        context.update(extras)
        return context
        
    def render(self, template_file, context={}):
        path = os.path.join(os.path.dirname(__file__), 'templates',
            template_file)
        # render the template with the provided context
        output = template.render(path, self._extra_context(context))
        return output