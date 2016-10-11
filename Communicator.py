from subprocess import Popen, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
from sys import platform
import os

class Communicator(object):
    def __init__(self):
        self.ChildProcess = None

    def isChildProcessNotNone(self):
        if(self.ChildProcess is None):
            return False
        else:
            return True

    def CreateChildProcess(self,Execution_Command,Executable_File, args_list):
        if platform == "darwin" or platform == "linux" or platform == "linux2":
            self.ChildProcess = Popen ([Execution_Command, Executable_File] + args_list, stdin = PIPE, stdout = PIPE, bufsize=0,preexec_fn=os.setsid)
        else:
            self.ChildProcess = Popen ([Execution_Command, Executable_File] + args_list, stdin = PIPE, stdout = PIPE, bufsize=0)
        self.ModifiedOutStream = NBSR(self.ChildProcess.stdout)

    def RecvDataOnPipe(self,TIMEOUT):
        data = None
        if(self.isChildProcessNotNone()):
            try:
                data = self.ModifiedOutStream.readline(TIMEOUT)
            except:
                pass
        return data

    def SendDataOnPipe(self,data):
        success_flag = False
        if(self.isChildProcessNotNone()):
            try:
                self.ChildProcess.stdin.write(data)
                success_flag = True
            except:
                pass
        return success_flag

    def closeChildProcess(self):
        if(self.isChildProcessNotNone()):
            if platform == "darwin" or platform == "linux" or platform == "linux2":
                try:
                    os.killpg(os.getpgid(self.ChildProcess.pid), 15)
                except:
                    pass
            else:
                self.ChildProcess.kill()
            self.ChildProcess = None


if __name__ == '__main__':
    c = Communicator()
    c.CreateChildProcess('sh','run.sh')
    counter = 1
    # snair: testing Communicator
    try:
        while(counter != 100):
            c.SendDataOnPipe(str(counter) + '\n')
            data = c.RecvDataOnPipe(1)
            print "Parent Recieved",data
            data = data.strip()
            counter += 1

        c.SendDataOnPipe("end")

    except:
        c.closeChildProcess()






