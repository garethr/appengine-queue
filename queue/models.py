from google.appengine.ext import db

import properties

class Task(db.Model):
    action = db.StringProperty()
    action_id = db.StringProperty()
    args = db.StringListProperty()
    kw = properties.DictProperty()
    expire = db.DateTimeProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    key_template = 'task/%(action)s/%(action_id)s'
    
    @classmethod
    def key_from(cls, **kw):
        if hasattr(cls, 'key_template'):
            try:
                return cls.key_template % kw
            except KeyError:
                pass
        return None