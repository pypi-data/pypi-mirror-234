from credis import Connection
import random
import string

def redisSetXTimes(client, keys, values, batch_size=500):
    keylen = len(keys)
    n_batch = keylen // batch_size

    for k in range(n_batch):
        for i in range(batch_size):
            client.execute('set', keys[random.randint(0, keylen-1)], values[random.randint(0, keylen-1)])

def redisGetXTimes(client , keys):
    commands = [('get', i) for i in keys]
    client.execute_pipeline(*commands)

def redisMGetXTimes(client , keys):
    keys_str = ' '.join(keys)
    client.execute_pipeline('mget', keys_str)

def randomStringGenerator(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

keys = []
values = []

for i in range(100000):
    keys.append(randomStringGenerator(15))
    values.append(randomStringGenerator(1000))

def test_credisSet():
    client = Connection(host='localhost', port=6379, db=0)
    redisSetXTimes(client=client, keys=keys, values=values)

def test_credisGet():
    client = Connection(host='localhost', port=6379, db=0)
    redisGetXTimes(client=client, keys=keys)

def test_credisMGet():
    client = Connection(host='localhost', port=6379, db=0)
    redisGetXTimes(client=client, keys=keys)