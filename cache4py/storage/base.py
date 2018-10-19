"""
Author: nitin
Date: 19/10/18
Description: Base class for all storage interfaces
"""
import abc


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