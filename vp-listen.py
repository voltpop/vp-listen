import redis
import time
import codecs
import pickle
import yaml
import pprint
import subprocess
import logging
import jinja2

logging.basicConfig(level=logging.INFO)
pp = pprint.PrettyPrinter()

if __name__ == "__main__":
    logging.info("Starting VoltPop Listener Service")
    config = yaml.load(open('listen.yml', "r").read(), Loader=yaml.SafeLoader)["listener"]
    logging.info("Connecting to %s:%s"%(config['redis_host'], config['redis_port']))
    r = redis.Redis(host=config['redis_host'], port=config["redis_port"], db='0')
    p = r.pubsub()
    
    for channel in config["channels"]:
        logging.info("Subscribing to channel: %s" % (channel["name"]))
        p.subscribe(channel['name'])

    while True:
        t = p.get_message()
        if t and t["type"] == "message":
            channel_name = t["channel"].decode('utf8')
            logging.debug("Received message for %s" % channel_name)
            data = pickle.loads(codecs.decode(t["data"], 'base64'))
            channel_config = next((channel for channel in config["channels"] if channel["name"] == t["channel"].decode('utf8')), None)
            logging.info("%s: %s" % (channel_name, str(data)))
        else:
            time.sleep(1)
