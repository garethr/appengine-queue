#!/usr/bin/env python

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import settings
from queue import task_process, task_create, exceptions
from lib import BaseRequest
    
class Process(BaseRequest):
    def get(self):
        try:
            rv = task_process()
            self.response.out.write("Processed a task")
        except exceptions.ApiNoTasks:
            self.response.out.write("No tasks to process")
        
class Seed(BaseRequest):
    def get(self):
        task_create('test', '1', ['test argument 1'])
        task_create('test', '2', ['test argument 2'])
        task_create('test', '3', ['test argument 3'])
        task_create('test', '4', ['test argument 4'])
        task_create('test', '5', ['test argument 5'])
        task_create('test', '6', ['test argument 6'])
        self.response.out.write("Seeded a few tasks")
                     
# Log a message each time this module get loaded.
logging.info('Loading %s, app version = %s',
    __name__, os.getenv('CURRENT_VERSION_ID'))
                        
def main():
    "Run the application"
    # wire up the views
    ROUTES = [
        ('/', Process),
        ('/seed/?', Seed),
    ]
    application = webapp.WSGIApplication(ROUTES, debug=settings.DEBUG)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()