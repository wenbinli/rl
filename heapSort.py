# heap sort experiment
# Version 1
# def maxHeapify(data,idx):
#     if idx < len(data):
#         root = data[idx]
#     else:
#         return data

#     # only compare if there are children nodes for the current index
#     if 2 * idx + 1 < len(data):
#         l_child = data[2*idx + 1]
#     else:
#         l_child = -10 # surrogate for -inf

#     if 2 * idx + 2 < len(data):    
#         r_child = data[2*idx + 2]
#     else:
#         r_child = -10

#     # root exchanges with bigger child
#     if l_child > root and l_child > r_child:
#         data[idx] = l_child
#         data[2 * idx + 1] = root
#     if r_child > root and r_child > l_child:
#         data[idx] = r_child
#         data[2 * idx + 2] = root

#     # check if max-heap properties maintains at sub-tree
#     maxHeapify(data,2*idx + 1)
#     maxHeapify(data,2*idx + 2)

#     return data

# Version 2
def maxHeapify(data,n,idx):
    largest = idx
    l = 2 * idx + 1
    r = 2 * idx + 2

    if l < n and data[largest] < data[l]:
        largest = l

    if r < n and data[largest] < data[r]:
        largest = r

    if largest != idx:
        data[idx], data[largest] = data[largest], data[idx]

        maxHeapify(data,n,largest)

def buildHeap(data):
    n = len(data)
    for i in range(n/2-1,-1,-1):
        maxHeapify(data,n,i)

def heapSort(data):
    buildHeap(data)
    n = len(data)

    for i in range(n-1,0,-1):
        # print i
        data[i], data[0] = data[0], data[i]
        maxHeapify(data,i,0)
        # print data
    
data = [12, 11, 13, 5, 6, 7]
heapSort(data)
print data