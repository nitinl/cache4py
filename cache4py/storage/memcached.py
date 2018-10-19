"""
Author: nitin
Date: 19/10/18
Description: Memcached storage connector
"""
import pickle
import warnings

from pymemcache.client import Client

from cache4py.exceptions import MemcachedBackendException
from cache4py.storage.base import BaseBackend


class MemcachedBackend(BaseBackend):
    """
    Wrapper over memcached client object provided by pymemcached library. Supports storing objects in memcached.
    """

    @staticmethod
    def memcached_serializer(key, value):
        """
        Pickle objects for storing in memcached.
        :param key: A key (length not exceeding 250)
        :param value: A value object.
        :return: Tuple (Serialized object, type_code)
        """
        if type(value) == str:
            return value, 1
        return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL), 2

    @staticmethod
    def memcached_deserializer(key, value, flags):
        """
        Unpickles objects for recovering them from memcached store.
        :param key: A key (length not exceeding 250)
        :param value: Pickled object corresponding to above key.
        :param flags: Value type code.
        :return: Unpickled python object.
        """
        if flags == 1:
            return value
        if flags == 2:
            return pickle.loads(value)
        raise Exception("Unknown serialization format")

    def __init__(self, server, port=11211):
        """
        Initialize memcached client as a cache backend.
        :param server: URL of memcached service.
        :param port: Port number at which memcached service is exposed. If not specified, uses port 11211 by default.
        """
        self.__server = server
        self.__port = port
        self.__client = Client(server=(server, port),
                               default_noreply=True,
                               serializer=MemcachedBackend.memcached_serializer,
                               deserializer=MemcachedBackend.memcached_deserializer)

        try:
            self.__client.stats()
        except Exception as exception:
            warnings.warn(
                'Error in connecting to memcached server: {0} at port: {1}. More details:\n{2}'.format(server, port,
                                                                                                       exception))

    def get(self, key_name):
        """
        Return the value at key ``key_name``, or None if the key doesn't exist.
        :param key_name: A key.
        :return: Value at key ``key_name``, or None if the key doesn't exist.
        """
        try:
            retrieved_value = self.__client.get(key_name)
            return retrieved_value
        except Exception as e:
            raise MemcachedBackendException(
                'Error in connecting to memcached server: {0} at port: {1}. More details:\n{2}'.format(self.__server,
                                                                                                       self.__port, e))

    def set(self, key_name, value):
        """
        Set the value at key ``key_name`` to ``value``
        :param key_name: A key object.
        :param value: A value object.
        :return: True if set successfully else False.
        """
        try:
            set_response = self.__client.set(key_name, value)
            return set_response
        except Exception as e:
            raise MemcachedBackendException(
                'Error in connecting to memcached server: {0} at port: {1}. More details:\n{2}'.format(self.__server,
                                                                                                       self.__port, e))

    def delete(self, key_name):
        """
        Deletes key specified by ``key_name``.
        :param key_name: A key object.
        :return: True if key is successfully deleted else False. Failure can mean connection issue or no value at given key in db.
        """
        try:
            if self.__client.delete(key_name) >= 0:
                return True
            return False  # given key does not exist in memcached
        except Exception as e:
            raise MemcachedBackendException(
                'Error in connecting to memcached server: {0} at port: {1}. More details:\n{2}'.format(self.__server,
                                                                                                       self.__port, e))