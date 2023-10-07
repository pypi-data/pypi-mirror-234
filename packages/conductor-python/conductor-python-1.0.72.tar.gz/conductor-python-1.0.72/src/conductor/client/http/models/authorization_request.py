import pprint
import re  # noqa: F401

import six

class AuthorizationRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'subject': 'SubjectRef',
        'target': 'TargetRef',
        'access': 'list[str]'
    }

    attribute_map = {
        'subject': 'subject',
        'target': 'target',
        'access': 'access'
    }

    def __init__(self, subject=None, target=None, access=None):  # noqa: E501
        """AuthorizationRequest - a model defined in Swagger"""  # noqa: E501
        self._subject = None
        self._target = None
        self._access = None
        self.discriminator = None
        self.subject = subject
        self.target = target
        self.access = access

    @property
    def subject(self):
        """Gets the subject of this AuthorizationRequest.  # noqa: E501


        :return: The subject of this AuthorizationRequest.  # noqa: E501
        :rtype: SubjectRef
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """Sets the subject of this AuthorizationRequest.


        :param subject: The subject of this AuthorizationRequest.  # noqa: E501
        :type: SubjectRef
        """
        self._subject = subject

    @property
    def target(self):
        """Gets the target of this AuthorizationRequest.  # noqa: E501


        :return: The target of this AuthorizationRequest.  # noqa: E501
        :rtype: TargetRef
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this AuthorizationRequest.


        :param target: The target of this AuthorizationRequest.  # noqa: E501
        :type: TargetRef
        """
        self._target = target

    @property
    def access(self):
        """Gets the access of this AuthorizationRequest.  # noqa: E501

        The set of access which is granted or removed  # noqa: E501

        :return: The access of this AuthorizationRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._access

    @access.setter
    def access(self, access):
        """Sets the access of this AuthorizationRequest.

        The set of access which is granted or removed  # noqa: E501

        :param access: The access of this AuthorizationRequest.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["CREATE", "READ", "UPDATE", "DELETE", "EXECUTE"]  # noqa: E501
        if not set(access).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `access` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(access) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._access = access

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AuthorizationRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AuthorizationRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
