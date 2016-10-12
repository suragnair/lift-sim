import argparse
import sys

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Stationary Controller')
    parser.add_argument('N', metavar='5', type=int, help='number of floors')
    parser.add_argument('K', metavar='2', type=int, help='number of elevators')
    parser.add_argument('p', metavar='0.8', type=float, help='prob person arrives')
    parser.add_argument('q', metavar='0.7', type=float, help='prob person arrives at ground floor, if s/he arrives')
    parser.add_argument('r', metavar='0.9', type=float, help='prob person gets down at first floor')
    parser.add_argument('t', metavar='1', type=float, help='time unit')
    args = parser.parse_args()

    sys.stdout.write('0\n')
    sys.stdout.flush()
    ready = sys.stdin.readline().strip()

    repeat = ['AU','AOU']*(args.N-1)
    repeat[-1] = 'AOD'
    repeat += ['AD','AOD']*(args.N-1)
    repeat[-1] = 'AOU'

    i = 0

    while(True):
        actions = ['AS' + str(k+1) for k in range(args.K)]
        actions[0] = repeat[i % len(repeat)] + '1'

        if i>3:
            actions[1] = repeat[(i-4) % len(repeat)] + '2'
        i+=1
        # sys.stderr.write(' '.join(actions) + '\n')
        sys.stdout.write(' '.join(actions) + '\n')
        sys.stdout.flush()
        cur_state = sys.stdin.readline().strip()