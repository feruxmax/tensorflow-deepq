class HumanController(object):
    def __init__(self, frontend):
        self.frontend = frontend 
        self.experience = []

    def action(self, o):
        action_codes = {"w":3, "a":2, "s":1, "d":0, None: 4}
        wasd = self.frontend.get_keys()
        action = None
        if len(wasd) > 0:
            action = wasd[-1]
        else:
            action = None 

        return action_codes[action]


    def store(self, observation, action, reward, newobservation):
        pass

    def training_step(self):
        pass

if __name__ == '__main__':
    pass
