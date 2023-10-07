# coding: utf-8

"""
    FINBOURNE Luminesce Web API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.13.628
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from luminesce.configuration import Configuration


class IdSelectorDefinition(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'identifier': 'dict(str, str)',
        'actions': 'list[ActionId]',
        'name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'actions': 'actions',
        'name': 'name',
        'description': 'description'
    }

    required_map = {
        'identifier': 'required',
        'actions': 'required',
        'name': 'optional',
        'description': 'optional'
    }

    def __init__(self, identifier=None, actions=None, name=None, description=None, local_vars_configuration=None):  # noqa: E501
        """IdSelectorDefinition - a model defined in OpenAPI"
        
        :param identifier:  (required)
        :type identifier: dict(str, str)
        :param actions:  (required)
        :type actions: list[luminesce.ActionId]
        :param name: 
        :type name: str
        :param description: 
        :type description: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._identifier = None
        self._actions = None
        self._name = None
        self._description = None
        self.discriminator = None

        self.identifier = identifier
        self.actions = actions
        self.name = name
        self.description = description

    @property
    def identifier(self):
        """Gets the identifier of this IdSelectorDefinition.  # noqa: E501


        :return: The identifier of this IdSelectorDefinition.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this IdSelectorDefinition.


        :param identifier: The identifier of this IdSelectorDefinition.  # noqa: E501
        :type identifier: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and identifier is None:  # noqa: E501
            raise ValueError("Invalid value for `identifier`, must not be `None`")  # noqa: E501

        self._identifier = identifier

    @property
    def actions(self):
        """Gets the actions of this IdSelectorDefinition.  # noqa: E501


        :return: The actions of this IdSelectorDefinition.  # noqa: E501
        :rtype: list[luminesce.ActionId]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this IdSelectorDefinition.


        :param actions: The actions of this IdSelectorDefinition.  # noqa: E501
        :type actions: list[luminesce.ActionId]
        """
        if self.local_vars_configuration.client_side_validation and actions is None:  # noqa: E501
            raise ValueError("Invalid value for `actions`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                actions is not None and len(actions) < 1):
            raise ValueError("Invalid value for `actions`, number of items must be greater than or equal to `1`")  # noqa: E501

        self._actions = actions

    @property
    def name(self):
        """Gets the name of this IdSelectorDefinition.  # noqa: E501


        :return: The name of this IdSelectorDefinition.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this IdSelectorDefinition.


        :param name: The name of this IdSelectorDefinition.  # noqa: E501
        :type name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 100):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 0):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this IdSelectorDefinition.  # noqa: E501


        :return: The description of this IdSelectorDefinition.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this IdSelectorDefinition.


        :param description: The description of this IdSelectorDefinition.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, IdSelectorDefinition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IdSelectorDefinition):
            return True

        return self.to_dict() != other.to_dict()
