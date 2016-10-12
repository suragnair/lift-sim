import argparse
import sys

def get_params():
    parser = argparse.ArgumentParser(description='Stationary Controller')
    parser.add_argument('N', metavar='5', type=int, help='number of floors')
    parser.add_argument('K', metavar='2', type=int, help='number of elevators')
    parser.add_argument('p', metavar='0.8', type=float, help='prob person arrives')
    parser.add_argument('q', metavar='0.7', type=float, help='prob person arrives at ground floor, if s/he arrives')
    parser.add_argument('r', metavar='0.9', type=float, help='prob person gets down at first floor')
    parser.add_argument('t', metavar='1', type=float, help='time unit')

    args = parser.parse_args()
    return args

def simpleAgent(args):
    ready = sys.stdin.readline().strip()

    repeat = ['AU','AOU']*(args.N-1)
    repeat[-1] = 'AOD'
    repeat += ['AD','AOD']*(args.N-1)
    repeat[-1] = 'AOU'

    i = 0

    while(True):
        actions = ['AOU' + str(k+1) for k in range(args.K)]

        for l in range(args.K):
            if i>(args.N/args.K+1)*l*2:
                actions[l] = repeat[(i - (args.N/args.K+1)*l*2 - 1) % len(repeat)] + str(l+1)

        i+=1
        # sys.stderr.write(' '.join(actions) + '\n')
        sys.stdout.write(' '.join(actions) + '\n')
        sys.stdout.flush()
        updates = sys.stdin.readline().strip()


if __name__=="__main__":
    args = get_params()

    sys.stdout.write('0\n')
    sys.stdout.flush()
    simpleAgent(args)

  