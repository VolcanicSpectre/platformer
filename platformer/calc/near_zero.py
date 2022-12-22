from math import isclose
from functools import partial

threshold = 1e-5
is_close_to_zero = partial(isclose, b=0, abs_tol=threshold)

def near_zero(a):
	if is_close_to_zero(a):
		return 0
	return a