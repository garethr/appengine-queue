from google.appengine.ext import db
        
class Dummy(db.Model):
    content = db.StringProperty()