from tf_rl.utils.getch import getch
from redis import StrictRedis



class HumanController(object):
    def __init__(self, mapping):
        self.mapping = mapping
        self.r = StrictRedis()
        self.experience = []

    def action(self, o):
        action = self.mapping[self.r.get("action")]
        self.r.delete("action")
        return action

    def store(self, observation, action, reward, newobservation):
        pass

    def training_step(self):
        pass



def control_me():
    r = StrictRedis()
    while True:
        c = getch()
        if ord(c) == 3: #^C
            exit()
        else:
            if c == 'a' or c == 's' or c == 'd' or c == 'w':
                r.set("action", c)
            else:
                print("use a s d f key to control or ^C to exit")


if __name__ == '__main__':
    control_me()
