from __future__ import print_function
import logging

import grpc

import core.net.proto.TaskMetadata_pb2 as TaskMetadata_pb2
import core.net.proto.TaskService_pb2_grpc as TaskService_pb2_grpc


def streamer():
    key = bytes([0x13, 0x00, 0x00, 0x00, 0x08, 0x00])
    for part in key:
        yield TaskMetadata_pb2.TaskArgument(arg=bytes([part]))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    

    with grpc.insecure_channel('localhost:50051') as channel:
        print(channel)
        stub = TaskService_pb2_grpc.TaskServiceStub(channel)
        temp = TaskMetadata_pb2.TaskMetadata(module='numpy', function='inverse', args=5, kwargs=None, task_id=None, _class='linalg')
        response = stub.AddTask(temp)
        print("Test client received status: %s and task_id: %s" % (response.status, response.task_id))
        for i in range(5):
            temp = streamer()
            argument = stub.AddArgument(temp)
            print(argument.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()