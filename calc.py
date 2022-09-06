def move_towards(current, target, max_delta):
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)
