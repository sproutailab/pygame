import json


class Bot(object):
    """
    The Bot class that applies the Qlearning logic to Flappy bird game
    After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    After every DUMPING_N iterations, dumps the Q values to the local JSON file
    """

    def __init__(self):
        self.games = 0  # Game count of current run, incremented after every death
        self.DUMPING_N = 1000  # Number of iterations to dump Q values to JSON after
        self.discount = 1.0
        self.r = {0: 1, 1: -1000}  # Reward function
        self.lr = 0.7
        self.load_qvalues()
        self.last_state = "420_240_0"
        self.last_action = 0
        self.moves = []

    def load_qvalues(self):
        """
        Load q values from a JSON file
        """
        self.qvalues = {}
        try:
            fil = open("data/qvalues.json", "r")
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    def act(self, xdif, ydif, vel):
        """
        Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        """
        state = self.map_state(xdif, ydif, vel)

        self.moves.append(
            (self.last_state, self.last_action, state)
        )  # Add the experience to the history

        self.last_state = state  # Update the last_state with the current state
        self.qvalues[state] = self.qvalues.get(state,[0, 0])

        if self.qvalues[state][0] >= self.qvalues[state][1]:
            self.last_action = 0
            return 0
        else:
            self.last_action = 1
            return 1

    def update_scores(self, dump_qvalues=True):
        """
        Update qvalues via iterating over experiences
        """
        history = list(reversed(self.moves))

        # Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split("_")[1]) > 120 else False

        # Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]

            # Select reward
            if t == 1 or t == 2:
                cur_reward = self.r[1]
            elif high_death_flag and act:
                cur_reward = self.r[1]
                high_death_flag = False
            else:
                cur_reward = self.r[0]

            # Update
            self.qvalues[state][act] = (1-self.lr) * (self.qvalues[state][act]) + \
                                       self.lr * ( cur_reward + self.discount*max(self.qvalues[res_state]) )

            t += 1

        self.games += 1  # increase game count
        if dump_qvalues:
            self.dump_qvalues()  # Dump q values (if game count % DUMPING_N == 0)
        self.moves = []  # clear history after updating strategies

    def map_state(self, xdif, ydif, vel):
        """
        Map the (xdif, ydif, vel) to the respective state, with regards to the grids
        The state is a string, "xdif_ydif_vel"

        X -> [-40,-30...120] U [140, 210 ... 420]
        Y -> [-300, -290 ... 160] U [180, 240 ... 420]
        """
        xdif = int(xdif) - (int(xdif) % 10)
        ydif = int(ydif) - (int(ydif) % 10)

        return str(int(xdif)) + "_" + str(int(ydif)) + "_" + str(vel)

    def dump_qvalues(self, force=False):
        """
        Dump the qvalues to the JSON file
        """
        if self.games % self.DUMPING_N == 0 or force:
            fil = open("data/qvalues.json", "w")
            json.dump(self.qvalues, fil)
            fil.close()
            print("Q-values updated on local file.")
