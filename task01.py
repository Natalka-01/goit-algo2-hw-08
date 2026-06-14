import random
import time
from collections import OrderedDict

# LRU Cache Implementation
class LRUCache:
    def __init__(self, capacity: int = 1000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: tuple) -> int:
        
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: tuple, value: int) -> None:

        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_index(self, index: int) -> None:

        keys_to_remove = [k for k in self.cache.keys() if k[0] <= index <= k[1]]
        for k in keys_to_remove:
            del self.cache[k]


# Functions WITHOUT Cache
def range_sum_no_cache(array, left, right):

    return sum(array[left : right + 1])

def update_no_cache(array, index, value):
    # Direct element update
    array[index] = value


# Functions WITH Cache 

cache = LRUCache(capacity=1000)

def range_sum_with_cache(array, left, right):
    key = (left, right)
    cached_result = cache.get(key)
    
    
    if cached_result != -1:
        return cached_result
    
    
    result = sum(array[left : right + 1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value):
# Update array and invalidate affected cache entries
    array[index] = value
    cache.invalidate_index(index)


#Query Generator
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 
            if random.random() < p_hot:       
                left, right = random.choice(hot)
            else:                             
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries



if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    
    # Initialize arrays with strictly positive integers
    array_no_cache = [random.randint(1, 100) for _ in range(N)]
    array_with_cache = array_no_cache.copy() 
    
    
    queries = make_queries(N, Q)

    
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array_no_cache, query[1], query[2])
        elif query[0] == "Update":
            update_no_cache(array_no_cache, query[1], query[2])
    time_no_cache = time.time() - start_time

    # 2. Benchmark WITH Cache
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array_with_cache, query[1], query[2])
        elif query[0] == "Update":
            update_with_cache(array_with_cache, query[1], query[2])
    time_with_cache = time.time() - start_time

    # Output Results
    speedup = time_no_cache / time_with_cache
    print(f"Without cache : {time_no_cache:.2f} c")
    print(f"LRU-cache  : {time_with_cache:.2f} c  (speedup ×{speedup:.1f})")