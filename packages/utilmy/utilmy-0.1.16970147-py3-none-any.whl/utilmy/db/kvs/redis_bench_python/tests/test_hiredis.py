import redis
import random
import string

def hiredisPipeleineSetXTimes(client, keys, values):
    keylen = len(keys)
    pipe = client.pipeline(transaction=False)
    for i in range(keylen):
        pipe.set(keys[random.randint(0, keylen-1)], values[random.randint(0, keylen-1)])
    pipe.execute()

def hiredisPipeleineGetXTimes(client , keys):
    pipe = client.pipeline(transaction=False)
    for i in keys:
        pipe.get(i)
    pipe.execute()

def hiredisPipeleineHSetXTimes(client: redis.Redis, keys, values, batch_size=500):
    pipe = client.pipeline(transaction=False)

    keylen = len(keys)
    n_batch = keylen // batch_size

    for k in range(n_batch):
        for i in range(batch_size):
            pipe.hset(i, keys[random.randint(0, keylen-1)], values[random.randint(0, keylen-1)])

        pipe.execute()
        

def hiredisPipeleineHGetXTimes(client: redis.Redis ,keys, batch_size=500):
    pipe = client.pipeline(transaction=False)

    n_batch = len(keys) // batch_size

    for k in range(n_batch):
        for i in range(batch_size):
            pipe.hget(i, keys[i])

        pipe.execute()


def redis_get_batch(client: redis.Redis ,keys, batch_size=500):
    pipe = client.pipeline(transaction=False)
    n_batch = len(keys) // batch_size
    result = []

    for k in range(n_batch):
        for i in range(batch_size):
            pipe.hget(i, keys[i])

        result.append(pipe.execute())

    return result


def randomStringGenerator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

keys = []
values = []

for i in range(100000):
    keys.append(randomStringGenerator(15))
    values.append(randomStringGenerator(1000))

def test_hiredisSet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    hiredisPipeleineSetXTimes(client=client, keys=keys, values=values)

def test_hiredisGet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    hiredisPipeleineGetXTimes(client=client, keys=keys)

def test_hiredisHSet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    hiredisPipeleineHSetXTimes(client=client, keys=keys, values=values)

def test_hiredisHGet():
    client = redis.Redis(host='localhost', port=6379, db=0)
    hiredisPipeleineHGetXTimes(client=client, keys=keys)

