from collections import OrderedDict

class LRUCache:
    capacity = 0

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.mapper = OrderedDict()

    def get(self, key: int) -> int:
        if key in self.mapper:
            self.mapper.move_to_end(key)
            return self.mapper[key]
        return -1
        
        

    def put(self, key: int, value: int) -> None:
        if key in self.mapper:
            self.mapper[key] = value
            self.mapper.move_to_end(key)
        else:
            self.mapper[key] = value
            self.mapper.move_to_end(key)
            keys = self.mapper.keys()
            if len(keys) > self.capacity:
                self.mapper.popitem(last=False)
            
            


# [[2],[2,1],[1,1],[2,3],[4,1],[1],[2]]

lrucache = LRUCache(2)

print(lrucache.get(2))
lrucache.put(2,1)
lrucache.put(1,1)
lrucache.put(2,3)
lrucache.put(4,1)
print(lrucache.get(1))
print(lrucache.get(2))
# print(lrucache.get(1))
# print(lrucache.get(3))
# print(lrucache.get(4))

# print(lrucache.get(3))
# print(lrucache.get(2))
# print(lrucache.get(4))
print(lrucache.mapper)


