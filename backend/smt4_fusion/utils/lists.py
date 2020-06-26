
def right_pad(arr, size):
    assert len(arr) <= size, f"length of arr must be less than {size=}"
    padding = [None] * (size - len(arr))
    return arr + padding
