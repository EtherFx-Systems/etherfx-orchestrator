from __future__ import print_function
import logging

import grpc

import TaskMetadata_pb2
import TaskService_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    # string module = 1;
    # string function = 2;
    # int32 args = 3;
    # repeated string kwargs = 4;
    # string task_id = 5;
    # string _class = 6;

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = TaskService_pb2_grpc.TaskServiceStub(channel)
        response = stub.AddTask(TaskMetadata_pb2.TaskMetadata(module='numpy', function='inverse', args=1, kwargs=None, task_id=None, _class='linalg'))
    print("Test client received status: %s and task_id: %s" % (response.status, response.task_id))


if __name__ == '__main__':
    logging.basicConfig()
    run()