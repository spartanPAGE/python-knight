class Entity:

    
    def __init__(self, scene_config, name):
        self.scene_sounds = scene_config['sounds']
        self.scene_sprites = scene_config['sprites']
        self.internal = scene_config['entities'][name]
        self.name = name


    def _states_stack(self):
        return self.internal['states_stack']

    
    def is_alive(self):
        return self.internal['alive']


    def die(self):
        if not self.is_alive():
            return
        
        self.internal['alive'] = False
        while len(self._states_stack()) > 1:
            self.pop_state()
        self.play_sound_if_associated_with_state(self.state())


    def remove_state(self, state):
        return self._states_stack().remove(state)

    def state(self):
        states = self._states_stack()
        return states[-1] if len(states) > 0 else None


    def push_state(self, state):
        self._states_stack().append(state)
        self.play_sound_if_associated_with_state(state)


    def play_sound_if_associated_with_state(self, state):
        sprite = self.scene_sprites[state]
        if 'sound' in sprite:
            sound = self.scene_sounds[sprite['sound']]
            sound['res'].play()


    def push_state_if_alive(self, state):
        if self.is_alive():
            self.push_state(state)


    def pop_state(self):
        return self.internal['states_stack'].pop()
