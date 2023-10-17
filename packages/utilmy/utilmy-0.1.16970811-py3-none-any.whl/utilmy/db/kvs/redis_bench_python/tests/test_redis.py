import redis
import random
import string

def redisSetXTimes(client, keys, values):
    keylen = len(keys)
    for i in range(keylen):
        client.set(keys[random.randint(0, keylen-1)], values[random.randint(0, keylen-1)])

def redisGetXTimes(client : redis.Redis, keys):
    for i in keys:
        client.get(i)

def redisHSetXTimes(client: redis.Redis, keys, values):
    keylen = len(keys)
    for i in range(keylen):
        client.hset(i, keys[random.randint(0, keylen-1)], values[random.randint(0, keylen-1)])

def redisHGetXTimes(client : redis.Redis, keys):
    for i in range(len(keys)):
        client.hget(i, keys[i])


def redisMGetXTimes(client , keys):
    client.mget(keys)

def randomStringGenerator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

keys = []
values = []

for i in range(100000):
    keys.append(randomStringGenerator(10))
    values.append(randomStringGenerator(500))

def test_redisSet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    redisSetXTimes(client=client, keys=keys, values=values)

def test_redisGet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    redisGetXTimes(client=client, keys=keys)

def test_redisHSet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    redisHSetXTimes(client=client, keys=keys, values=values)

def test_redisHGet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    redisHGetXTimes(client=client, keys=keys)

def test_redisMGet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    redisGetXTimes(client=client, keys=keys)
