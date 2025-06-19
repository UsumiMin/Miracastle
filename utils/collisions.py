def handle_x_collisions(entity, platforms, velocity_x):
    entity_rect = entity.rect
    entity_rect.x += velocity_x
    for platform in platforms:
        if entity_rect.colliderect(platform['rect']):
            if velocity_x > 0:
                entity_rect.right = platform['rect'].left
                entity.velocity_x = 0
            elif velocity_x < 0:
                entity_rect.left = platform['rect'].right
                entity.velocity_x = 0
    return entity_rect.x

def handle_y_collisions(entity, platforms, velocity_y, old_y):
    entity_rect = entity.rect
    entity.on_ground = False
    entity_rect.y += velocity_y
    for platform in platforms:
        if entity_rect.colliderect(platform['rect']):
            if velocity_y > 0 and old_y + entity_rect.height <= platform['rect'].top:
                entity_rect.bottom = platform['rect'].top
                entity.velocity_y = 0
                entity.on_ground = True
            elif velocity_y < 0 and old_y >= platform['rect'].bottom:
                entity_rect.top = platform['rect'].bottom
                entity.velocity_y = 0
    return entity_rect.y

def handle_collisions(entity, platforms, velocity_x, velocity_y, old_y):
    entity_rect = entity.rect
    entity_rect.x = handle_x_collisions(entity, platforms, velocity_x)
    entity_rect.y = handle_y_collisions(entity, platforms, velocity_y, old_y)
    return entity_rect.x, entity_rect.y