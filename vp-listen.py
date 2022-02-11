import redis
import time
import codecs 
import pickle

channel = "ansible"

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port='6379', db='0')
    p = r.pubsub()
    p.subscribe(channel)
    while True:
        t = p.get_message()
        if t["type"] == "message":
            print(pickle.loads(codecs.decode(t['data'], 'base64')))

        time.sleep(15)
