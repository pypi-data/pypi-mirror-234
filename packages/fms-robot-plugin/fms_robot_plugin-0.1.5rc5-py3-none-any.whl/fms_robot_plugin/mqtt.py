from typing import Any, Callable

import json
import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, host: str, port: int):
        self.client = mqtt.Client()
        self.client.connect(host, port)

    def publish(self, topic: str, data: Any, serialize: bool = True):
        if serialize:
            data = json.dumps(data)

        self.client.publish(topic, data)


class MqttConsumer:
    def __init__(self, topic: str, host: str, port: int):
        self.topic = topic
        self.url_params: list[tuple[int, str]] = []
        self.host = host
        self.port = port

    def consume(self, cb: Callable[[dict, dict], None], serialize: bool = True):
        self.cb = cb

        for index, section in enumerate(self.topic.split("/")):
            if section.startswith(":"):
                self.topic = self.topic.replace(section, "+")
                self.url_params.append((index, section[1:]))

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message_callback(serialize)

        client.connect(self.host, self.port)
        client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message_callback(self, serialize: bool = True):
        def on_message(client, userdata, msg):
            msg.topic.split("/")

            payload = msg.payload
            if serialize:
                payload = json.loads(payload.decode("utf-8"))

            url_params = {}

            for index, param in self.url_params:
                url_params[param] = msg.topic.split("/")[index]

            if len(url_params.keys()) > 0:
                self.cb(payload, url_params)
            else:
                self.cb(payload)

        return on_message
