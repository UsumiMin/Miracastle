
class Camera:
    def __init__(self, screen_width, screen_height, level_width, level_height):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_width = level_width
        self.level_height = level_height
    
    def update(self, target):
        """Обновляет положение камеры, следуя за целью"""
        # Центрируем камеру на цели
        self.offset_x = target.rect.centerx - self.screen_width // 2
        self.offset_y = target.rect.centery - self.screen_height // 2
        
        # Ограничиваем камеру границами уровня
        self.offset_x = max(0, min(self.offset_x, self.level_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.level_height - self.screen_height))
    
    def apply(self, rect):
        """Применяет смещение камеры к прямоугольнику"""
        return rect.move(-self.offset_x, -self.offset_y)