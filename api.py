from models import Dummy

def test(*args):
    dummy = Dummy(
        content = "testing %s" % args[0],
    )
    dummy.put()

class PublicApi(object):
    methods = {
        "test": test,
    }

    @classmethod
    def get_method(cls, name):
        if name in cls.methods:
            return cls.methods[name]
        return None
        
