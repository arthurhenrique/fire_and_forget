# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from bottle import run, response, request, route
import time
import asyncio
import subprocess
import random
import uuid

def fire_and_forget(f):
    '''decorator'''
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError('Task must be a callable')    
    return wrapped

@route('/<_time>')
def test(_time):
    x(_time, uuid.uuid4().__str__())
    return response.status

@fire_and_forget
def x(_time, u):
    print('time:', _time, u)
    time.sleep(int(_time))
    cmd = "ps -A | grep 'python'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print('_time:', _time, u, output)
    y(u, _time)

def y(u, _time):
    _time = int(_time)

    print('focus = ', _time, u)
    time.sleep(_time)
    print('focus = ', _time, u)
    time.sleep(_time)
    print('focus = ', _time, u)
    time.sleep(_time)
    print('focus = ', _time, u)
    z(u, _time)

def z(u, _time):
    print('end', u, _time)

run(host='0.0.0.0', port=8080, debug=True, server='gunicorn', workers=10)
