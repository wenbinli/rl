# heap sort experiment
def maxHeapify(data,idx):
    if idx < len(data):
        root = data[idx]
    else:
        return data

    # only compare if there are children nodes for the current index
    if 2 * idx + 1 < len(data):
        l_child = data[2*idx + 1]
    else:
        l_child = -10 # surrogate for -inf

    if 2 * idx + 2 < len(data):    
        r_child = data[2*idx + 2]
    else:
        r_child = -10

    # root exchanges with bigger child
    if l_child > root and l_child > r_child:
        data[idx] = l_child
        data[2 * idx + 1] = root
    if r_child > root and r_child > l_child:
        data[idx] = r_child
        data[2 * idx + 2] = root

    # check if max-heap properties maintains at sub-tree
    maxHeapify(data,2*idx + 1)
    maxHeapify(data,2*idx + 2)

    return data

data = [4,10,3,5,1]
data_sort = maxHeapify(data,0)
print data_sort