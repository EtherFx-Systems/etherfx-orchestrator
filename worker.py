import threading, subprocess, sys

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
        argument = []
        for peace in self.stream:
            argument += peace.arg
        self.parent.args.append(argument)