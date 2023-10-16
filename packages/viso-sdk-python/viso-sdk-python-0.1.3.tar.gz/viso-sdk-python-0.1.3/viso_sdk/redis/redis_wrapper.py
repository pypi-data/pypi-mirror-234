"""
Redis Wrapper from viso.ai
"""

import base64
import threading
from typing import Any, Optional, Union

import cv2  # type: ignore
import numpy as np
import redis


from viso_sdk.constants import PREFIX
from viso_sdk.logging.logger import get_logger


logger = get_logger("REDIS")


def gen_redis_key_local(node_id, port):
    return f"{PREFIX.REDIS.LOCAL}_{node_id}_{port}"


class RedisWrapper:
    """Represents a redis client specified for the containers.

    Args:
        thread(bool): Use threading or not
        host(str): Redis server host
        port(int): Redis server port
    """

    def __init__(
            self,
            thread: bool = True,
            host: str = "localhost",
            port: int = 6379,
    ):
        self._use_thread = thread
        self._redis_client = redis.StrictRedis(host, port)

        _img_arr = None

    @staticmethod
    def gen_redis_key_status(node_id, port):
        return f"{PREFIX.REDIS.STATUS}_{node_id}_{port}"

    @staticmethod
    def base64_to_img(b64_bytes: bytes) -> Union[None, np.ndarray]:
        """Convert base64 string to opencv frame"""
        try:
            str_frame = base64.b64decode(b64_bytes)
            _img_arr = np.frombuffer(str_frame, dtype=np.uint8)
            image = cv2.imdecode(  # pylint: disable=no-member
                _img_arr, -1
            )
            # self._img_arr = None
            return image
        except Exception as err:
            logger.warning(f"Failed to convert base64 to image - {err}")
        return None

    @staticmethod
    def img_to_base64str(image: np.ndarray, zoom_ratio: Optional[float] = 1.0) -> tuple:
        """Convert opencv frame to base64 encoded string"""
        if zoom_ratio != 1.0:
            image = cv2.resize(  # pylint: disable=no-member
                image, None, fx=zoom_ratio, fy=zoom_ratio
            )
        ret, jpg = cv2.imencode(".jpg", image)  # pylint: disable=no-member
        jpg_as_text = base64.b64encode(jpg)
        return ret, jpg_as_text

    def write_frame(
            self, frame: np.ndarray, redis_key: str, zoom: Optional[float] = 1.0
    ) -> bool:
        """Write video frame to the target redis key

        Args:
                frame(np.ndarray): numpy frame to be written.
                redis_key(str): Target redis key.
                zoom(float): Zoom ratio(optional).
        """
        if self._use_thread:
            threading.Thread(
                target=self._write_to_redis, args=(frame, redis_key, zoom)
            ).start()
            return True
        return self._write_to_redis(frame, redis_key, zoom)

    def _write_to_redis(
            self,
            frame: Union[np.ndarray, None],
            redis_key: str,
            zoom: Optional[float] = 1.0,
    ) -> bool:
        """Internal function that is executed in background thread"""
        if frame is not None:
            ret, jpg_as_text = self.img_to_base64str(frame, zoom)
            if ret:
                try:
                    return bool(self._redis_client.set(redis_key, jpg_as_text))
                except Exception as err:
                    logger.error(f"Failed to write frame to redis - {err}")
            logger.warning("Failed to convert stream to write to redis")
            return False
        return bool(self._redis_client.delete(redis_key))

    def delete_data(self, redis_key: str) -> bool:
        """Delete data from the target redis location

        Args:
            redis_key(str): Target redis key.
        """
        return bool(self._redis_client.delete(redis_key))

    def put_data(self, redis_key: str, data: str) -> bool:
        """Write data to the target redis location

        Args:
            redis_key(str): Target redis key.
            data(str): Data to be written.
        """
        return bool(self._redis_client.set(redis_key, data))

    def read_data(self, redis_key: str) -> Any:
        """Read data from the target redis location

        Args:
            redis_key(str): Target redis key.
        """
        return self._redis_client.get(redis_key)

    def get_frame(self, redis_key: str) -> Union[np.ndarray, None]:
        """Read video frame from a given redis key

        Args:
            redis_key(str): Target redis key.
        """
        try:
            b64_bytes = self._redis_client.get(redis_key)
            if b64_bytes and isinstance(b64_bytes, bytes):
                return self.base64_to_img(b64_bytes)
        except Exception as err:
            logger.warning(f"Failed to get redis frame from {redis_key} - {err}")
        return None
