class HumanController(object):
    def __init__(self, frontend):
        self.frontend = frontend 
        self.experience = []
        self.last_action = None

    def action(self, o):
        action_codes = {"w":3, "a":2, "s":1, "d":0, None: 4}
        wasd = self.frontend.get_keys()
        action = None
        if len(wasd) == 0:
            action = None 
        elif len(wasd) == 1:
            action = wasd[-1]
        elif len(wasd) == 2:
            if wasd[-1] != self.last_action:
                action = wasd[-1]
            else:
                action = wasd[0]

        self.last_action = action

        return action_codes[action]


    def store(self, observation, action, reward, newobservation):
        pass

    def training_step(self):
        pass

if __name__ == '__main__':
    pass
