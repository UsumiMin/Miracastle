def handle_collisions(entity, platforms, camera, velocity_x, velocity_y, old_x, old_y):
    entity_rect = entity.rect
    entity.on_ground = False
    entity_rect.x += velocity_x
    for platform in platforms:
        platform_rect = platform['rect']  # Используем мировые координаты
        if entity_rect.colliderect(platform_rect):
            if velocity_x > 0:
                entity_rect.right = platform_rect.left
                entity.velocity_x = 0
            elif velocity_x < 0:
                entity_rect.left = platform_rect.right
                entity.velocity_x = 0
                
    entity_rect.y += velocity_y
    for platform in platforms:
        platform_rect = platform['rect']  # Используем мировые координаты
        if entity_rect.colliderect(platform_rect):
            if velocity_y > 0 and old_y + entity_rect.height <= platform_rect.top:
                entity_rect.bottom = platform_rect.top
                entity.velocity_y = 0
                entity.on_ground = True
            elif velocity_y < 0 and old_y >= platform_rect.bottom:
                entity_rect.top = platform_rect.bottom
                entity.velocity_y = 0  # Отладка
    return entity_rect.x, entity_rect.y