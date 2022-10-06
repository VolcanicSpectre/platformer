def move_towards(current, target, max_delta):
    """Returns the value closest to the target value with a maximimm change of max_delta"""
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)
