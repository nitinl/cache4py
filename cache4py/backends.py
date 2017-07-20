"""
Author: nitin
Date: 18/7/17
Description: 
"""
import abc
import redis
import warnings
import pickle

from pymemcache.client import Client

from exceptions import RedisBackendException, MemcachedBackendException


class BaseBackend(metaclass=abc.ABCMeta):
    """
    Abstract class defining Cache client interface. All implementations of cache clients
    must extend this class.
    """

    @abc.abstractmethod
    def get(self, key_name):
        """
        Return the value at key ``key_name``, or None if the key doesn't exist.
        :param key_name: A key.
        :return: Value at key ``key_name``, or None if the key doesn't exist.
        """
        raise NotImplementedError('Cache client must define a get method.')

    @abc.abstractmethod
    def set(self, key_name, value):
        """
        Set the value at key ``key_name`` to ``value``
        :param key_name: A key object.
        :param value: A value object.
        :return: True if set successfully else False.
        """
        raise NotImplementedError('Cache client must define a set method.')

    @abc.abstractmethod
    def delete(self, key_name):
        """
        Deletes key specified by ``key_name``.
        :param key_name: A key object.
        :return: True if key is successfully deleted else False. Failure can mean connection issue or no value at given key in db.
        """
        raise NotImplementedError('Cache client must define a delete method.')


class RedisBackend(BaseBackend):
    """
    Wrapper over redis client object provided by python redis library. Supports storing objects in redis.
    """

    def __init__(self, server, port=6379):
        self.__server = server
        self.__port = port
        self.__client = redis.StrictRedis(host=server, port=port)
        try:
            self.__client.ping()
        except redis.ConnectionError as connection_error:
            warnings.warn('Failed to connect to redis server: {0} at port: {1}'.format(server, port))
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
        return pickle.dumps(value), 2

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
        self.__server = server
        self.__port = port
        self.__client = Client(server=(server, port),
                               connect_timeout=1,
                               timeout=0.5,
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
        except:
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
        except Cca:
            raise MemcachedBackendException(
                'Error in connecting to memcached server: {0} at port: {1}. More details:\n{2}'.format(self.__server,
                                                                                                       self.__port, e))
