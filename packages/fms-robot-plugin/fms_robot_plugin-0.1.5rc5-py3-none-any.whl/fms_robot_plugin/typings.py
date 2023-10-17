from pydantic import BaseModel


class Point(BaseModel):
    """
    Based on ROS geometry_msgs/Point
    """

    x: float
    y: float
    z: float


class Quarternion(BaseModel):
    """
    Based on ROS geometry_msgs/Quarternion
    """

    x: float
    y: float
    z: float
    w: float


class Twist(BaseModel):
    """
    Based on ROS geometry_msgs/Twist
    """

    linear: Point
    angular: Point


class LaserScan(BaseModel):
    """
    Based on ROS sensor_msgs/LaserScan
    """

    angle_min: float
    angle_max: float
    angle_increment: float
    time_increment: float
    scan_time: float
    range_min: float
    range_max: float
    ranges: list[float | None]
    intensities: list[float]


class Pose(BaseModel):
    """
    Based on ROS geometry_msgs/Pose
    """

    position: Point
    orientation: Quarternion


class MapMetadata(BaseModel):
    """
    Based on ROS nav_msgs/MapMetaData
    """

    resolution: float
    width: int
    height: int
    origin: Pose


class Map(BaseModel):
    """
    Contains the basic information of a navigational map
    """

    metadata: MapMetadata
    data: str
