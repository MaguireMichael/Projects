import redis

r = redis.Redis(
    host='192.168.1.141',
    port=6379, 
    password='')

#print("This is the value of r " + str(r))

#r.set('foo', 'bar')
#r.set('hot', 'cheryl')
#r.set('On my mind', 'Cheryl is fucking hot')
k = r.keys("*")
print(k)
#r.delete('foo')
#r.delete('On my mind')
#print(r.keys())
#value = r.get('hot')
#value2 = r.get('hot')
#print(value)
#print(value2)
#answer = r.get("On my mind")
#print(" What is on my mind? " + answer)

#value3 = r.randomkey()
#print("This is value3: " + str(value3))
#print(r.client_list())

h = r.hgetall("*" " *")
print(h)
t = r.ttl('hot')
print(t)