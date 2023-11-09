# Music related
MAXIMUM_QUEUE_SIZE  = 25
MAXIMU_QUEUE_SIZE_REACHED = "Sorry your queue is full."
MINIMUM_QUEUE_SIZE_REACHED = "Queue is empty."


def make_duraion(length):
    seconds = length / 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{int(minutes)}:{int(remaining_seconds)}"