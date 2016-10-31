from Communicator import Communicator
from Enivronment import Environment
import os, argparse


class Interactor(Communicator):

    def __init__(self):
        super(Interactor, self).__init__()
        pass

    def CheckExeFile(self, Execution_Command, Executable_File):
        """ Checks the Existence of the Executable File and
            if the extension of the file matches the command used to run it
        Args:
            Execution_Command : Command used to execute the Executable File (sh, python ./ etc)
            Executable_File : The Executable File
        Returns:
            None
         """
        Extension = Executable_File.split('.')
        if (len(Extension) == 1):
            return False
        Extension = Extension[-1]
        if (os.path.isfile(Executable_File)):
            if (Execution_Command == './' or Execution_Command == 'sh'):
                if (Extension == 'sh' or Extension == 'o'):
                    return True
                else:
                    return False
            elif (Execution_Command == 'java'):
                if (Extension == 'java'):
                    return True
                else:
                    return False
            elif (Execution_Command == 'python'):
                if (Extension == 'py'):
                    return True
                else:
                    return False
        else:
            return False

    def CreateChildProcess(self, Execution_Command, Executable_File, args_list):
        """ Creates a Process, with which the Simulator communicates.
            Checks the existance of the Executable_File and some basic
            checks for whether the Execution_Command used to run the code
            matches the extension of the Executable File
            Prints if error is found
        Args:
            Execution_Command : Command used to execute the Executable File (sh, python ./ etc)
            Executable_File : The Executable File
            args_list : list of arguments (N, K, p, q, r, t_u)
        Returns:
            None
        """
        if (self.CheckExeFile(Execution_Command, Executable_File)):
            super(Interactor, self).CreateChildProcess(Execution_Command, Executable_File, args_list)
        else:
            print 'ERROR : EITHER FILE ', Executable_File, ' DOES NOT EXIST',
            print 'OR THE EXECUTION COMMAND TO RUN THE FILE ', Execution_Command, ' IS INCORRECT'

    def RecvDataFromProcess(self, t_u, first_time=False):
        """
        Receives Data from the process. Waits 30 minutes for the first '0', then t_u every time
        For both the above cases, prints the error msg and closes the connection to the process.

        Args:
            t_u : time unit as specified in the problem statement
            first_time : if receiving data for the first time, timeout = 30 minutes and t_u from then

        Returns:
            retData : array of length K with action for every elevator
                      string "ERROR" in case of an error
        """
        FIRST_TIMEOUT = 30*60

        if first_time:
            data = super(Interactor, self).RecvDataOnPipe(FIRST_TIMEOUT)
        else:
            data = super(Interactor, self).RecvDataOnPipe(t_u)

        retData = None
        if (data == None):
            print 'ERROR : AGENT TIMED OUT'
            super(Interactor, self).closeChildProcess()
            retData = 'ERROR'

        else:
            if data.strip() == '0':
                retData = '0'
            else:
                retData = data.strip().split(' ')

        return retData

    def SendData2Process(self, data):
        """ Sends Data (State) to the process. Handles the case if the process being communicated with has closed.
        Args:
            data : string data, to send the process (buttons pressed)
        Returns:
            success_flag : A boolean flag to denote the data transfer to the process was successful or not.
        """

        if data[-1] != '\n':
            data += '\n'
        success_flag = super(Interactor, self).SendDataOnPipe(data)
        if not success_flag:
            print 'ERROR : FAILED TO SEND DATA TO PROCESS'
            super(Interactor, self).closeChildProcess()
        return success_flag


def simulate(args):
    args_list = [str(args.N), str(args.K), str(args.p), str(args.q), str(args.r), str(args.t)]
    interactor = Interactor()

    if args.exe.endswith('.py'):
        interactor.CreateChildProcess('python', args.exe, args_list)
    elif args.exe.endswith('.sh'):
        interactor.CreateChildProcess('sh', args.exe, args_list)
    else:
        interactor.CreateChildProcess('sh', args.exe, args_list)

    ready = interactor.RecvDataFromProcess(args.t, first_time=True)

    if ready != '0':
        return

    env = Environment(args.N, args.K, args.p, args.q, args.r, args.t)
    interactor.SendData2Process('0')
    if args.mode != 'None':
        print(env)
    sim_log = str(env) + '\n'

    for episode in range(args.ep):
        actions = interactor.RecvDataFromProcess(args.t, first_time=False)
        if actions == 'ERROR':
            sim_log += 'ERROR\n'
            break

        new_buttons_pressed = env.apply_action([''.join([i for i in x if not i.isdigit()]) for x in actions])
        if new_buttons_pressed == 'INVALID ACTION' or len(actions) != args.K:
            print('~'*len(new_buttons_pressed) + '\n' + new_buttons_pressed + '\n' + '~'*len(new_buttons_pressed))
            sim_log += 'INVALID ACTION\n'
            break

        interactor.SendData2Process(new_buttons_pressed)

        sim_log += '\n' + '=' * len('EPISODE ' + str(episode + 1)) + '\n'
        sim_log += 'EPISODE ' + str(episode + 1) + '\n'
        sim_log += '=' * len('EPISODE ' + str(episode + 1)) + '\n'
        sim_log += '\n' + '=> Actions taken : ' + ' '.join(actions) + '\n'
        sim_log += str(env) + '\n'
        sim_log += '=> Updates sent : ' + new_buttons_pressed + '\n'

        if args.mode != 'None':
            print('')
            print('=' * len('EPISODE ' + str(episode + 1)))
            print('EPISODE ' + str(episode+1))
            print('='*len('EPISODE ' + str(episode+1))+'\n')
            print('=> Actions taken : ' + ' '.join(actions))
            print(env)
            print('=> Update sent : ' + new_buttons_pressed)

    print('FINAL TOTAL COST (at the end of ' + str(episode+1) + ' simulations) : ' + str(env.total_cost))

    interactor.closeChildProcess()
    f = open(args.log, 'w')
    f.write(sim_log)
    f.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Elevator Control Simulator')
    parser.add_argument('exe', metavar='run.sh', type=str, help='your executable')
    parser.add_argument('N', metavar='5', type=int, help='number of floors')
    parser.add_argument('K', metavar='2', type=int, help='number of elevators')
    parser.add_argument('p', metavar='0.8', type=float, help='prob person arrives')
    parser.add_argument('q', metavar='0.7', type=float, help='prob person arrives at ground floor, if s/he arrives')
    parser.add_argument('r', metavar='0.9', type=float, help='prob person gets down at first floor')
    parser.add_argument('t', metavar='1', type=float, help='time unit')
    parser.add_argument('-ep', dest='ep', type=int, default=1000, help='number of episodes to play, default 1000')
    parser.add_argument('-mode', dest='mode', type=str, default='CUI', help='display settings')
    parser.add_argument('-log', dest='log', type=str, default='simulation.txt', help='name for simulation log file, default simulation.txt')
    args = parser.parse_args()

    simulate(args)