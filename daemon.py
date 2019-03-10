import grpc
import uuid
import time
import logging
from concurrent import futures
from worker import Worker
from _thread import start_new_thread
import dill as pickle


from core.net.proto.TaskCommon_pb2 import Status as Status
from core.net.proto.TaskCommon_pb2 import StatusCode as StatusCode
from core.net.proto.TaskMetadata_pb2 import TaskReceived as TaskReceived
from core.net.proto.TaskMetadata_pb2 import TaskResponse as TaskResponse
from core.net.proto.TaskService_pb2_grpc import TaskServiceServicer as TaskService
from core.net.proto.TaskService_pb2_grpc import add_TaskServiceServicer_to_server as AddTaskServicer
from core.redis_interface import GDSClient
from core.rabbitmq_interface import RabbitMQInterface



_ONE_DAY_IN_SECONDS = 60 * 60 * 24
class Daemon(TaskService):

    def __init__(self, args=[], task_metadata=None):
        self.args = args #[b'0x56', b'0x56'...]
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
        print("triggered AddTask")
        return TaskReceived(status=Status(code=StatusCode.Value('OK'), message='Task Metadata received!' ), task_id= task_metadata["task_id"])


    def AddArgument(self, request_iterator, context):
        # p = ThreadPool(1)
        # self.args.append(p.map(Worker, request_iterator))

        thread = Worker(request_iterator, self)
        thread.start()
        thread.join()
        if len(self.args) == int(self.task_metadata["args"]):
            #Send to GDS 
            gds.add_args_to_gds(self.task_metadata["task_id"], self.args)
            #TEMPORARY FIX FOR THIS DEMO
            self.task_metadata['kwargs'] = None
            rabbitMQ.publish_taskMetadata_to_queue_from_orchestrator(self.task_metadata)
            self.args = []
            print(self.task_metadata)
            return Status(code=StatusCode.Value('OK'), message='Task Pending!' )
        else:
            return Status(code=StatusCode.Value('OK'), message='Task Argument Received!' )
        

    def PollTask(self, request, context):
        #query 
        computation_result = None #This is going to be the result value that needs to be sent to client
        #if task is done then
        if(computation_result):
            # Get the result of the computation form the GDS here and put it into computation_result
            gds.get_result_from_gds(self.task_metadata["task_id"])
            bin_arg = pickle.dumps(computation_result)
            return TaskResponse(result=bin_arg)
        else:
            return Status(code=StatusCode.Value('Wait'), message='Fuck Off!' )

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
    gds = GDSClient()
    rabbitMQ = RabbitMQInterface()
    serve()