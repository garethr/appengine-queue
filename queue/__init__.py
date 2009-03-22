from datetime import datetime, timedelta

from google.appengine.ext import db

from api import PublicApi
from models import Task
import settings
import exceptions
  
def task_process():

    query = Task.gql('WHERE expire = :1 ORDER BY created_at', None)

    task_ref = None
    task_more = None
    
    for fake_task_ref in query.fetch(1):
        task_ref = task_get(fake_task_ref.action, fake_task_ref.action_id)

    if not task_ref:
        raise exceptions.ApiNoTasks

    method_ref = PublicApi.get_method(task_ref.action)

    rv = method_ref(*task_ref.args, 
                    **task_ref.kw)
                    
    task_remove(task_ref.action, task_ref.action_id)

    query = Task.gql('WHERE expire < :1', datetime.utcnow())
    t_ref = query.fetch(1)
    if t_ref:
        task_more = True

    return task_more
    
def task_get(action, action_id, expire=settings.DEFAULT_TASK_EXPIRE):

    key_name = Task.key_from(action=action, action_id=action_id)

    def _attempt_lock(key, expire):
        qi = db.get(key)
        now = datetime.utcnow()
        if qi.expire and qi.expire > now:
            raise exceptions.ApiTaskExpired
        qi.expire = now + timedelta(seconds=expire)
        qi.put()
        
    qu = Task.get_by_key_name(key_name)
    if not qu:
        raise exceptions.ApiMethodUnavailable

    try:
        db.run_in_transaction(_attempt_lock, qu.key(), expire)
        return Task.get_by_key_name(key_name)
    except db.TransactionFailedError:
        raise exceptions.ApiLockError

    return qu
    
def task_create(action, action_id, args=None, kw=None, expire=None):
    if args is None:
        args = []
    if kw is None:
        kw = {}

    key_name = Task.key_from(action=action, action_id=action_id)
    task_ref = Task(
        key_name="task/%s/%s" % (action, action_id),
        action=action,
        action_id=action_id,
        expire=expire,
        args=args,
        kw=kw,
    )
    task_ref.put()
    return task_ref
    
def task_remove(action, action_id):

    key_name = Task.key_from(action=action, action_id=action_id)

    q = Task.get_by_key_name(key_name)
    if not q:
        raise exceptions.ApiTaskDoesntExist

    q.delete()

    return True