import grpc
import time
import logging
from concurrent import futures
from worker import Worker

from TaskService_pb2_grpc import TaskServiceServicer as TaskService
from TaskService_pb2_grpc import add_TaskServiceServicer_to_server as AddTaskServicer


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
class Daemon(TaskService):

    def __init__(self):
        # self.args = None
        # self.task_id = None
        # self.task_metadata = None
        pass

    def generateTaskID(self, TaskMetaData):
        pass

    def spinUpNewNode(self):
        pass

    def AddTask(self, request, context):
        print("This is working!!")

    def AddArgument(self, request, context):
        # p = ThreadPool(self.task_metadata.noofargs)
        # self.args.append(p.map(Worker, request.<stream-name>))
        pass

    def PollTask(self, request, context):
        pass

    def ExecTask(self, request, context):
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    AddTaskServicer(Daemon(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    	worker = Daemon()
    	serve()