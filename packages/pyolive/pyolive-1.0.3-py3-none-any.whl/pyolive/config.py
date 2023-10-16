import os
import yaml


class Config:
    def __init__(self, home, file):
        filepath = os.path.join(home, 'config', file)
        with open(filepath) as f:
            self.cf = yaml.load(f, Loader=yaml.FullLoader)

    def get_value(self, key):
        name = key.split('/')
        size = len(name)
        if size == 1:
            val = self.cf[name[0]]
        elif size == 2:
            val = self.cf[name[0]][name[1]]
        elif size == 3:
            val = self.cf[name[0]][name[1]][name[2]]
        elif size == 4:
            val = self.cf[name[0]][name[1]][name[2]][name[3]]
        else:
            print("Overflow key depth")
        return val
