# mountcar
import numpy as np
import matplotlib.pyplot as plt

def step(xt,vt, a):
	vt_ = vt + 0.001 * a - 0.0025 * np.cos(3 * xt)
	xt_ = xt + vt_

	T = 0
	if xt_ <= -1.2:
		xt_ = -1.2
		vt_ = 0
	elif xt_ >= 0.5:
		T = 1

	if vt_ < -0.07:
		vt_ = -0.07
	elif vt_ > 0.07:
		vt_ = 0.07

	return xt_,vt_, T

num_episodes = 10
episode_count = 0
step_count_history = []
xt_history = []

while episode_count < num_episodes:
	print "---------- Episode " + str(episode_count) + "----------"
	xt_record = []
	terminal = 0
	step_count = 0
	xt = -0.2 * np.random.random() - 0.6
	vt = 0
	xt_record.append(xt)
	while terminal == 0:
		# print "step " + str(step_count)
		# random policy
		a = np.random.randint(-1,2)
		xt,vt,terminal = step(xt,vt,a)
		r = 0
		if terminal == 0:
			r = -1
		xt_record.append(xt)
		step_count += 1
	xt_history.append(xt_record)
	step_count_history.append(step_count)
	episode_count += 1

# plot results
f, (ax1,ax2) = plt.subplots(1,2)

ax1.plot(np.log10(step_count_history))
plt.sca(ax1) # set current axes instance
plt.xlabel('Episode')
plt.ylabel('Steps per episode log scale')
plt.title('Mountain Car')

ax2.plot(xt_history[0])
plt.sca(ax2)
plt.xlabel('Step')
plt.ylabel('x_t')
plt.title('Path')

fig = plt.gcf()
fig.set_size_inches(10,3)
plt.savefig('MountainCar_random.png', bbox_inches='tight', dpi=300)