import entities

def fade_in(enemy, screen, params):
    speed = int(params[0])
    factor = int(params[1])

    if enemy.y_speed is None:
        enemy.x_speed = 0
        x_speed = enemy.x_speed
        enemy.y_speed = speed
        y_speed = enemy.y_speed
    if abs(enemy.x_speed) < 1:
        x_speed = 0
    else:
        x_speed = enemy.x_speed
    if abs(enemy.y_speed) < 1:
        y_speed = 0
    else:
        y_speed = enemy.y_speed

    return x_speed * factor, y_speed * factor

def sweep(enemy, screen, params):
    screen_size = screen.get_size()
    speed = int(params[0])
    delay = int(params[1])

    if enemy.x_speed is None:
        x_speed = speed
        enemy.delay = 0
        enemy.next_direction = 1

    if enemy.delay > 0:
        enemy.delay -= 1
        return 0, 0

    if enemy.x < 0:
        enemy.x = 0
        x_speed = 0
        enemy.delay = delay
        enemy.next_direction = 1
    elif enemy.x + enemy.width > screen_size[0]:
        enemy.x = screen_size[0] - enemy.width
        x_speed = 0
        enemy.delay = delay
        enemy.next_direction = -1
    else:
        x_speed = speed*enemy.next_direction

    return x_speed, 0

def border(enemy, screen, params):
    screen_size = screen.get_size()
    border_speed = int(params[0])

    if enemy.x < 0:
        enemy.x = 0
    if enemy.x + enemy.width > screen_size[0]:
        enemy.x = screen_size[0] - enemy.width
    if enemy.y < 0:
        enemy.y = 0
    if enemy.y + enemy.height > screen_size[1]:
        enemy.y = screen_size[1] - enemy.height

    if enemy.x == 0: # down
        if enemy.y + enemy.height < screen_size[1]:
            return 0, border_speed
        else:
            return border_speed, 0
    if enemy.y + enemy.height == screen_size[1]: # right
        if enemy.x + enemy.width < screen_size[0]:
            return border_speed, 0
        else:
            return 0, -border_speed
    if enemy.x + enemy.width == screen_size[0]: # up
        if enemy.y > 0:
            return 0, -border_speed
        else:
            return -border_speed, 0
    if enemy.y == 0: # left
        if enemy.x > 0:
            return -border_speed, 0
        else:
            return 0, border_speed

    # not on an edge
    x_distance = min(enemy.x, screen_size[0] - enemy.x) # closest x-border
    y_distance = min(enemy.y, screen_size[1] - enemy.y) # closest y-border

    if x_distance <= y_distance:
        if enemy.x + enemy.width < screen_size[0] - enemy.x:
            return -abs(border_speed), 0
        else:
            return abs(border_speed), 0
    if y_distance < x_distance:
        if enemy.y + enemy.height < screen_size[1] - enemy.y:
            return 0, -abs(border_speed)
        else:
            return 0, abs(border_speed)

entities.pattern_types["Border"] = border
entities.pattern_types["Sweep"] = sweep
entities.pattern_types["FadeIn"] = fade_in