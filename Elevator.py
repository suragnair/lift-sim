class Elevator(object):
    """
    - state representation of the elevator
    """
    def __init__(self, N, K):
        self.N = N                              # number of floors
        self.K = K                              # number of elevators

        self.pos = [0]*K                        # initial positions of all elevators
        self.BU = [0]*N                         # button up on each floor   (always 0 for top floor)
        self.BD = [0]*N                         # button down on each floor (always 0 for first floor)
        self.BF = [[0]*N for i in range(K)]     # floor buttons pressed inside elevator, for each elevator
        self.LU = [0]*K                         # light up indicator for each lift for its current floor (always 0 for top floor)
        self.LD = [0]*K                         # light down indicator for each lift for its current floor (always 0 for first floor)

    def __str__(self):
        """
        - returns a string expression of the current state of the elevator
        """
        state = ''
        state += ' '.join([str(x) for x in self.pos])  + ' '
        state += ''.join([str(x) + ' ' + str(y) + ' ' for x, y in zip(self.BU,self.BD)])
        for e in self.BF:
            state += ' '.join([str(x) for x in e])
            state += ' '
        state += ' '.join([str(x) for x in self.LU]) + ' '
        state += ' '.join([str(x) for x in self.LD]) + ' '

        return state

    # state modifiers

    def modify_pos(self, k, delta):
        """
        - change position of kth lift by delta (+/- 1)
        - validity checks in Simulator
        """
        self.pos[k] += delta

    def modify_floor_button(self, n, direction, status):
        """
        - n : floor number
        - direction : 'U' for up button and 'D' for down button
        - status : 0 to clear and 1 to press
        - returns if status was toggled
        """

        toggled = True

        if direction == 'U':
            if self.BU[n] == status:
                toggled = False
            self.BU[n] = status
        if direction == 'D':
            if self.BD[n] == status:
                toggled = False
            self.BD[n] = status

        return toggled

    def modify_elevator_button(self, k, n, status):
        """
        - k : elevator number
        - n : floor number
        - status : 0 to clear and 1 to press
        - returns if status was toggled
        """
        toggled = True
        if self.BF[k][n] == status:
            toggled = False
        self.BF[k][n] = status

        return toggled

    def reset_lights(self):
        self.LU = [0] * self.K
        self.LD = [0] * self.K

    def modify_lights(self, k, direction, status):
        """
        - k : lift number
        - direction : 'U' for up button and 'D' for down button
        - status : 0 to clear and 1 to press
        """
        if direction == 'U':
            self.LU[k] = status
        if direction == 'D':
            self.LD[k] = status