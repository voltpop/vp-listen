import redis
import time
import codecs
import pickle
import yaml

channel = "ansible"
redishost = "announce.voltpop.com"
redisport = 10001
if __name__ == "__main__":
    config = yaml.load(open('listen.yml', "r").read(), Loader=yaml.SafeLoader)["listener"]
    print("Connecting to %s:%s"%(config['redis_host'], config['redis_port']))
    r = redis.Redis(host=config['redis_host'], port=config["redis_port"], db='0')
    p = r.pubsub()
    
    for channel in config["channels"]:
        print("Subscribing to channel: %s" % (channel))
        p.subscribe(channel)

    while True:
        print("Checking Messages...")
        t = p.get_message()
        if t:
            if t["type"] == "message":
                print(pickle.loads(codecs.decode(t['data'], 'base64')))
            time.sleep(15)
        else:
            time.sleep(1)
