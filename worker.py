import threading, subprocess, sys
import dill as pickle
class Worker(threading.Thread):

    def __init__(self, stream, parent):
        threading.Thread.__init__(self)
        self.stream = stream
        self.parent = parent
    
    def run(self):
        self.construct_argument()

    # remove from class in-case something doesnt work
    def construct_argument(self):
        # if removed from the class, pass self.stream to construct_argument() inside run method
        
        next(self.stream)
        argument = b''
        for i in self.stream:
            argument += i.arg
        
        print(pickle.loads(argument))
        # for peace in self.stream:
        #     argument += peace.arg
        self.parent.args.append(argument)