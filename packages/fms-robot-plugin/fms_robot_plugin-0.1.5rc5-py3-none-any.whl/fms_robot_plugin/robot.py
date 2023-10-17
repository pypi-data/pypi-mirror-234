from typing import Callable, Optional

import time
import datetime
import logging

from fms_robot_plugin.typings import LaserScan, Twist, Pose, Map
from fms_robot_plugin.mqtt import MqttClient, MqttConsumer


class Robot:
    robot_key: Optional[str]

    def __init__(
        self,
        robot_key: str,
        broker_host: str = "broker.movelrobotics.com",
        broker_port: int = 1883,
        heartbeat_interval_secs: int = 1,
        debug: bool = False,
    ):
        self.robot_key = robot_key

        self.broker_host = broker_host
        self.broker_port = broker_port
        self.mqtt = MqttClient(broker_host, broker_port)

        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def run(self):
        self.maintain_connection()

    """
    Command Callbacks

    These methods are called when a command is published from the FMS server.
    """

    def on_teleop(self, cb: Callable[[Twist], None]):
        topic = f"robots/{self.robot_key}/teleop"
        self.consumer(topic).consume(lambda data: cb(Twist(**data)))

    def on_start_mapping(self, cb: Callable[[str], None]):
        topic = f"robots/{self.robot_key}/mapping/start"
        self.consumer(topic).consume(lambda map_id: cb(map_id), serialize=False)

    def on_stop_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/stop"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_save_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/save"
        self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_localize(self, cb: Callable[[str, Pose], None]):
        topic = f"robots/{self.robot_key}/localize"
        self.consumer(topic).consume(lambda data: cb(data["map_id"], Pose(**data["initial_pose"])))

    def on_load_map_pgm(self, cb: Callable[[bytes, str], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/pgm"
        self.consumer(topic).consume(lambda pgm, url_params: cb(pgm, url_params["map_id"]), serialize=False)

    def on_load_map_yaml(self, cb: Callable[[bytes, str], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/yaml"
        self.consumer(topic).consume(lambda yaml, url_params: cb(yaml, url_params["map_id"]), serialize=False)

    """
    Publishers

    These methods are called to publish data to the FMS server.
    """

    def set_heartbeat(self):
        self.mqtt.publish(f"robots/{self.robot_key}/heartbeat", {"sent_at": datetime.datetime.utcnow().isoformat()})

    def set_camera_feed(self, data: str):
        self.mqtt.publish(f"robots/{self.robot_key}/camera", data, serialize=False)

    def set_lidar(self, data: LaserScan):
        self.mqtt.publish(f"robots/{self.robot_key}/lidar", data.dict())

    def set_pose(self, data: Pose):
        self.mqtt.publish(f"robots/{self.robot_key}/pose", data.dict())

    def set_map_data(self, data: Map):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/data", data.dict())

    def set_map_result(self, pgm: str, yaml: str):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/result/pgm", pgm, serialize=False)
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/result/yaml", yaml, serialize=False)

    def set_cpu_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/cpu", data, serialize=False)

    def set_memory_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/memory", data, serialize=False)

    def set_battery_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/battery", data, serialize=False)

    """
    Utilities
    """

    def consumer(self, topic: str):
        return MqttConsumer(topic, self.broker_host, self.broker_port)

    def maintain_connection(self):
        while True:
            self.set_heartbeat()
            time.sleep(1)
