def heapsort(heap):
    import heapq
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


# [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
lst = range(10, -1, -1)

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print heapsort(lst)
