def move_towards(current, target, max_delta):
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)


def colliderect(rect1, rect2):
    if rect1.x > rect2.x + rect2.width or rect1.x + rect1.width < rect2.x:
        return False
    if rect1.y > rect2.y + rect2.height or rect1.y + rect1.height < rect2.y:
        return False
    return True
