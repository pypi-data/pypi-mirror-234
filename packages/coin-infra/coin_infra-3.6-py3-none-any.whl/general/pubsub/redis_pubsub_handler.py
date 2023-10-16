import redis


class RedisPubSubHandler:
    def __init__(self, host, port, db, logger):
        self.logger = logger
        self.redis_conn = redis.StrictRedis(host=host, port=port, db=db)
        self.pubsub = self.redis_conn.pubsub()

    def publish(self, channel, message):
        self.redis_conn.publish(channel, message)

    def subscribe(self, channels):
        if isinstance(channels, str):
            channels = [channels]
        for channel in channels:
            self.pubsub.subscribe(channel)

    def listen(self, callback=None):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel']
                data = message['data']
                self.logger.debug(f"Received message '{data}' on channel '{channel}'")
                if callback:
                    callback(data)
