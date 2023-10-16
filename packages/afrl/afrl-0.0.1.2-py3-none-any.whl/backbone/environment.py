class AbstractEnvironment:
    def __init__(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def step(self, action: Action):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

