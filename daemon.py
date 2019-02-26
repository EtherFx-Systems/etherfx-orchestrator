import grpc
from worker import Worker
TaskService = __import__("etherfx-core.ether.net.proto.TaskService_pb2_grpc.TaskService")

class Daemon(TaskService):

    def __init__(self):
        self.args = None
        self.task_id = None
        self.task_metadata = None
        pass

    def generateTaskID(self, TaskMetaData):
        pass

    def spinUpNewNode(self):
        pass

    def add_task(self, request, response):
        pass

    def add_argument(self, request, response):
        # p = ThreadPool(self.task_metadata.noofargs)
        # self.args.append(p.map(Worker, request.<stream-name>))
        pass

    def poll_task(self, request, response):
        pass

    def exec_task(self, request, response):
        pass

    def serve(self):
        pass

if __name__ == "__main__":
    	worker = Daemon()
    	worker.serve()