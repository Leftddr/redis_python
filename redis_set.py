import redis
import time
import random
import threading
import argparse

parser = argparse.ArgumentParser(description = 'redis_set_examine')

parser.add_argument('--n', required = True, help = 'SET COUNT', default = 100000)
parser.add_argument('--t', required = True, help = 'PER THREAD COUNT', default = 5)
parser.add_argument('--data_size_ranges', required = True, help = 'Data Size Range', default = 1000-8000)

args = parser.parse_args()

_lock = threading.Lock()

fp = open('./redis_set.txt', 'a')

try :
    conn = redis.StrictRedis(
        host = '127.0.0.1',
        port = 6379
    )
except Exception as ex:
    print('Error : ', ex)

time_result = []

def redis_for_set(n, size):

    limit_ = size.split('-')

    x = 'x'

    for i in range(0, 5000):
        x = x + 'x'

    result = x

    for count in range(0, n):
        key = random.randrange(1, 10000000)
        limit = random.randrange(int(limit_[0]), int(limit_[1]))
        x = result
        for i in (0, limit):
            x = x + 'x'

        _lock.acquire()
        start = time.time()
        conn.set(key, x)
        end = time.time() - start
        _lock.release()
        _lock.acquire()
        time_result.append(end)
        fp.write(str(end * 1000) + '\n')
        _lock.release()

if __name__ == "__main__":

    if args.data_size_ranges.find('-') == -1:
        println('Error : data_size_ranges format [1-n]')

    for i in range(int(args.t)):
        th = threading.Thread(target = redis_for_set, args=[int(args.n), args.data_size_ranges])
        th.start()
        th.join()

'''
for i in range(0, len(time_result)):
    fp.write(str(time_result[i] * 1000) + '\n')
'''

fp.close()

    