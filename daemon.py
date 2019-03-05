import grpc
import uuid
import time
import logging
from concurrent import futures
from worker import Worker

from TaskCommon_pb2 import Status
from TaskCommon_pb2 import StatusCode
from TaskMetadata_pb2 import TaskReceived as TaskReceived
from TaskService_pb2_grpc import TaskServiceServicer as TaskService
from TaskService_pb2_grpc import add_TaskServiceServicer_to_server as AddTaskServicer


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
class Daemon(TaskService):

    def __init__(self, args=None, task_metadata=None):
        self.args = args
        self.task_metadata = task_metadata
        pass

    def generateTaskID(self, TaskMetaData):
        pass

    def spinUpNewNode(self):
        pass

    def AddTask(self, request, context):
        task_metadata = {
            "module": request.module, 
            "function": request.function, 
            "args": request.args,
            "kwargs": request.kwargs,
            "task_id": request.task_id,
            "_class": request._class
        }
        task_metadata["task_id"] = str(uuid.uuid4())
        self.task_metadata = task_metadata
        return TaskReceived(status=Status(status=StatusCode.Value('OK'), message='Task Metadata received!' ), task_id= task_metadata["task_id"])


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