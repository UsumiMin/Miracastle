from utils.sprite_loader import SpriteLoader

class AnimationManager:
    def __init__(self, character_name, scale=1, default_speed=0.10):
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_speed = default_speed
        self.sprites = SpriteLoader.load_animated_sprites(character_name, scale)
        
    def update(self):
        self.current_frame = (self.current_frame + self.animation_speed) % len(self.sprites[self.current_state])
        current_frame = int(self.current_frame)
        return self.sprites[self.current_state][current_frame]
    
    def set_state(self, state):
        if state in self.sprites and state != self.current_state:
            self.current_state = state
            self.current_frame = 0