'''
manages all servers
'''
from multiprocessing import Process

from rider.tasks.server import TaskServer
from rider.wsgi.server import GunicornWsgiServer, SimpleWsgiServer

#class RegisterServer(type):
    #servers = []
    #def __new__(mcls, name, bases, attrs):
        #mcls.servers.append(name):
        #return type.__new__(mcls, name, bases, attrs)

    #def run(cls)
        #print cls.servers


def run(debug=False):
    http_server = SimpleWsgiServer()
    http_worker = Process(target=http_server.run)

    task_server = TaskServer()
    task_worker = Process(target=task_server.run)

    http_worker.start()
    task_worker.start()

    if debug:
        debug_server = DebugServer()
        debug_worker = Process(target=debug_server.run)
        debug_worker.start()