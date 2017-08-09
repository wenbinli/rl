# puck world example
# no GUI atm
import numpy as np

def step(x, y, v_x, v_y, w, h):
	x_ = x + v_x * 1.
	y_ = y + v_y * 1.
	
	return x_, y_

# world size
w = 3
h = 3

start_x = np.random.random() * w
start_y = np.random.random() * h

# dynamic model
v_x = 0
v_y = 0

# move every second
# constraint: boundary
# every 30 seconds reset
T = 1000
while t < T:

	t += 1