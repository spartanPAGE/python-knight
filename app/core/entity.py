class Entity:

    
    def __init__(self, scene_config, name):
        self.internal = scene_config['entities'][name]
        self.name = name


    def _states_stack(self):
        return self.internal['states_stack']

    
    def is_alive(self):
        return self.internal['alive']


    def die(self):
        self.internal['alive'] = False
        while len(self._states_stack()) > 1:
            self.pop_state()

    def state(self):
        states = self.states_stack()
        return states[-1] if len(states) > 0 else None


    def push_state(self, state):
        self.internal['states_stack'].append(state)


    def pop_state(self):
        return self.internal['states_stack'].pop()
