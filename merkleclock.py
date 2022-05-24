from hashlib import sha256
from collections import OrderedDict
from ordered_set import OrderedSet
import random
database = {}
def generate_hash(value):
  if type(value) == str:
    return value
  if type(value) == dict:
    hash = ""
    for key, value in value.items():
      hash += key
      hash += generate_hash(value)
    return hash


class MerkleClock:
  @classmethod
  def new_root(cls, database):
    
    hash = str(random.getrandbits(128)).encode("utf8")
    root_cid = sha256(hash).hexdigest()
    new_root = MerkleClock(root_cid, database, "", "", OrderedSet(), None, None)
    database[root_cid] = new_root
    return new_root

  

  def __init__(self, cid, database, key, value, children, previous, cache):
    self.cid = cid
    self.database = database
    self.value = value
    self.key = key
    self.children = children
    self.previous = previous
    if cache == None:
      self.cache = {}
    else:
      self.cache = cache

  def __eq__(self, item):
    if isinstance(item, MerkleClock) and item.cid == self.cid:
      return True
    else:
      return False

  def __hash__(self):
    return hash(self.cid)
  
  def __repr__(self):
    data = ""
    for value in self.children:
      data += "{} = {}\n".format(self.key, str(value.value))
    return data
    
  def set(self, key, value):
    
    if type(value) == dict:
      last = MerkleClock.new_root(database)
      hash = ""

      

      for lkey, subvalue in value.items():
        last = last.set(lkey, subvalue)
        

      new_children = OrderedSet(self.children)
      
      new_cid = sha256((key + generate_hash(value)).encode("utf8")).hexdigest()
      new_keyvalue = last
      last.key = key
      last.value = value
      
            
      new_children.add(new_keyvalue)


      root_cid = sha256("".join([clock.cid for clock in new_children]).encode("utf8")).hexdigest()
      new_root = MerkleClock(root_cid, self.database, "", "", new_children, None, self.cache)
      self.database[root_cid] = new_root
      self.database[new_cid] = new_keyvalue
      if key in new_root.cache:
       new_children.remove(self.cache[key])
      new_root.cache[key] = new_keyvalue
      return new_root
    if type(value) == str:
      new_children = OrderedSet(self.children)
      new_cid = sha256((key + value).encode("utf8")).hexdigest()
      
      new_keyvalue = MerkleClock(new_cid, self.database, key, value, OrderedSet(), self, None)
      
      new_children.add(new_keyvalue)


      root_cid = sha256("".join([clock.cid for clock in new_children]).encode("utf8")).hexdigest()
      new_root = MerkleClock(root_cid, self.database, "", "", new_children, None, self.cache)
      self.database[root_cid] = new_root
      self.database[new_cid] = new_keyvalue
      if key in new_root.cache:
       new_children.remove(self.cache[key])
      new_root.cache[key] = new_keyvalue
      return new_root
  def lookup(self, key):
    return self.cache[key]
  
  def merge(self, clock, path=""):
    new_children = OrderedSet()
    for child in self.children:
      for merge_child in clock.children:
        if path + child.key == path + merge_child.key:
          new_children.add(child.merge(merge_child, path + child.key))
          
        else:
          new_children.add(merge_child)
          new_children.add(child)     
    root_cid = sha256("".join([clock.cid for clock in new_children]).encode("utf8")).hexdigest()
    new_cache = dict(self.cache)
    new_cache.update(clock.cache)
    new_root = MerkleClock(root_cid, self.database, "", "", new_children, None, new_cache)
    
    self.database[root_cid] = new_root
    
    return new_root
    
  def lookup(self, key):
    return self.cache[key]

      
m1 = MerkleClock.new_root(database)
m2 = m1.set("hello", "world")
m3 = m2.set("hello", "world2")
m4 = m3.set("hello", {
  "hi": {"world": "6"}
})

print(database)
print(m4.lookup("hello"))

a1 = MerkleClock.new_root(database)
a2 = a1.set("world", "hi")
merged = m4.merge(a2)
for child in merged.children:
  print("key")
  print(child.key)
