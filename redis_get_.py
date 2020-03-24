import redis
import time
import random
import threading
import argparse

parser = argparse.ArgumentParser(description = 'redis_get_examine')

parser.add_argument('--n', required = True, help = 'GET COUNT', default = 100000)
parser.add_argument('--t', required = True, help = 'PER THREAD COUNT', default = 5)

args = parser.parse_args()

_lock = threading.Lock()

fp = open('./redis_get.txt', 'a')

try :
    conn = redis.StrictRedis(
        host = '127.0.0.1',
        port = 6379
    )
except Exception as ex:
    print('Error : ', ex)

time_result = []

def redis_for_get(until_):

    for count in range(0, until_):
        key = random.randrange(1, 10000000)
        _lock.acquire()
        start = time.time()
        conn.get(key)
        end = time.time() - start
        _lock.release()
        _lock.acquire()
        fp.write(str(end * 1000) + '\n')
        time_result.append(end)
        _lock.release()

if __name__ == "__main__":
    for i in range(int(args.t)):
        th = threading.Thread(target = redis_for_get, args=[int(args.n)])
        th.start()
        th.join()

'''
for i in range(0, len(time_result)):
    fp.write(str(time_result[i] * 1000) + '\n')
'''

fp.close()