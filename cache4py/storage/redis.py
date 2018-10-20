"""
Author: nitin
Date: 19/10/18
Description: Redis storage connector
"""
import pickle
import warnings

import redis

from cache4py.exceptions import RedisBackendException
from cache4py.storage.base import BaseBackend


class RedisBackend(BaseBackend):
    """
    Wrapper over redis client object provided by python redis library. Supports storing objects in redis.
    """

    def __init__(self, url, port=6379):
        """
        Initialize redis client as a cache backend.
        :param url: URL of redis service.
        :param port: Port number at which redis service is exposed. If not specified, uses port 6379 by default.
        """
        self.__server = url
        self.__port = port
        self.__client = redis.StrictRedis(host=url, port=port)
        try:
            self.__client.ping()
        except redis.ConnectionError as connection_error:
            warnings.warn('Failed to connect to redis server: {0} at port: {1}'.format(url, port))
            raise RedisBackendException(connection_error)

    def is_client_valid(self):
        """
        Checks if redis client points to an active Redis server.
        :return: True if client points to a functional Redis server else False.
        """
        if self.__client is None:
            return False
        try:
            self.__client.ping()
        except redis.ConnectionError:
            return False
        return True

    def get(self, key_name):
        """
        Return the value at key ``key_name``, or None if the key doesn't exist.
        :param key_name: A key.
        :return: Value at key ``key_name``, or None if the key doesn't exist.
        """
        if not self.is_client_valid():
            raise RedisBackendException('Failed to connect to redis backend {0}:{1}'.format(self.__server, self.__port))
        retrieved_value = self.__client.get(key_name)
        if retrieved_value is not None:
            retrieved_value = pickle.loads(retrieved_value)
        return retrieved_value

    def set(self, key_name, value):
        """
        Set the value at key ``key_name`` to ``value``
        :param key_name: A key object.
        :param value: A value object.
        :return: True if set successfully else False.
        """
        if not self.is_client_valid():
            raise RedisBackendException('Failed to connect to redis backend {0}:{1}'.format(self.__server, self.__port))
        set_response = self.__client.set(key_name, pickle.dumps(value))
        return set_response

    def delete(self, key_name):
        """
        Deletes key specified by ``key_name``.
        :param key_name: A key object.
        :return: True if key is successfully deleted else False. Failure can mean connection issue or no value at given key in db.
        """
        if not self.is_client_valid():
            raise RedisBackendException('Failed to connect to redis backend {0}:{1}'.format(self.__server, self.__port))
        if self.__client.delete(key_name) >= 0:
            return True

        return False