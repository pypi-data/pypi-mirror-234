import pprint
import re  # noqa: F401

import six

class WorkflowRun(object):
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
        'correlation_id': 'str',
        'create_time': 'int',
        'created_by': 'str',
        'input': 'dict(str, object)',
        'output': 'dict(str, object)',
        'priority': 'int',
        'request_id': 'str',
        'status': 'str',
        'tasks': 'list[Task]',
        'update_time': 'int',
        'variables': 'dict(str, object)',
        'workflow_id': 'str'
    }

    attribute_map = {
        'correlation_id': 'correlationId',
        'create_time': 'createTime',
        'created_by': 'createdBy',
        'input': 'input',
        'output': 'output',
        'priority': 'priority',
        'request_id': 'requestId',
        'status': 'status',
        'tasks': 'tasks',
        'update_time': 'updateTime',
        'variables': 'variables',
        'workflow_id': 'workflowId'
    }

    def __init__(self, correlation_id=None, create_time=None, created_by=None, input=None, output=None, priority=None, request_id=None, status=None, tasks=None, update_time=None, variables=None, workflow_id=None):  # noqa: E501
        """WorkflowRun - a model defined in Swagger"""  # noqa: E501
        self._correlation_id = None
        self._create_time = None
        self._created_by = None
        self._input = None
        self._output = None
        self._priority = None
        self._request_id = None
        self._status = None
        self._tasks = None
        self._update_time = None
        self._variables = None
        self._workflow_id = None
        self.discriminator = None
        if correlation_id is not None:
            self.correlation_id = correlation_id
        if create_time is not None:
            self.create_time = create_time
        if created_by is not None:
            self.created_by = created_by
        if input is not None:
            self.input = input
        if output is not None:
            self.output = output
        if priority is not None:
            self.priority = priority
        if request_id is not None:
            self.request_id = request_id
        if status is not None:
            self.status = status
        if tasks is not None:
            self.tasks = tasks
        if update_time is not None:
            self.update_time = update_time
        if variables is not None:
            self.variables = variables
        if workflow_id is not None:
            self.workflow_id = workflow_id

    @property
    def correlation_id(self):
        """Gets the correlation_id of this WorkflowRun.  # noqa: E501


        :return: The correlation_id of this WorkflowRun.  # noqa: E501
        :rtype: str
        """
        return self._correlation_id

    @correlation_id.setter
    def correlation_id(self, correlation_id):
        """Sets the correlation_id of this WorkflowRun.


        :param correlation_id: The correlation_id of this WorkflowRun.  # noqa: E501
        :type: str
        """

        self._correlation_id = correlation_id

    @property
    def create_time(self):
        """Gets the create_time of this WorkflowRun.  # noqa: E501


        :return: The create_time of this WorkflowRun.  # noqa: E501
        :rtype: int
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this WorkflowRun.


        :param create_time: The create_time of this WorkflowRun.  # noqa: E501
        :type: int
        """

        self._create_time = create_time

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowRun.  # noqa: E501


        :return: The created_by of this WorkflowRun.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowRun.


        :param created_by: The created_by of this WorkflowRun.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def input(self):
        """Gets the input of this WorkflowRun.  # noqa: E501


        :return: The input of this WorkflowRun.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._input

    @input.setter
    def input(self, input):
        """Sets the input of this WorkflowRun.


        :param input: The input of this WorkflowRun.  # noqa: E501
        :type: dict(str, object)
        """

        self._input = input

    @property
    def output(self):
        """Gets the output of this WorkflowRun.  # noqa: E501


        :return: The output of this WorkflowRun.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this WorkflowRun.


        :param output: The output of this WorkflowRun.  # noqa: E501
        :type: dict(str, object)
        """

        self._output = output

    @property
    def priority(self):
        """Gets the priority of this WorkflowRun.  # noqa: E501


        :return: The priority of this WorkflowRun.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this WorkflowRun.


        :param priority: The priority of this WorkflowRun.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def request_id(self):
        """Gets the request_id of this WorkflowRun.  # noqa: E501


        :return: The request_id of this WorkflowRun.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this WorkflowRun.


        :param request_id: The request_id of this WorkflowRun.  # noqa: E501
        :type: str
        """

        self._request_id = request_id

    @property
    def status(self):
        """Gets the status of this WorkflowRun.  # noqa: E501


        :return: The status of this WorkflowRun.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this WorkflowRun.


        :param status: The status of this WorkflowRun.  # noqa: E501
        :type: str
        """
        allowed_values = ["RUNNING", "COMPLETED", "FAILED", "TIMED_OUT", "TERMINATED", "PAUSED"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def tasks(self):
        """Gets the tasks of this WorkflowRun.  # noqa: E501


        :return: The tasks of this WorkflowRun.  # noqa: E501
        :rtype: list[Task]
        """
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        """Sets the tasks of this WorkflowRun.


        :param tasks: The tasks of this WorkflowRun.  # noqa: E501
        :type: list[Task]
        """

        self._tasks = tasks

    @property
    def update_time(self):
        """Gets the update_time of this WorkflowRun.  # noqa: E501


        :return: The update_time of this WorkflowRun.  # noqa: E501
        :rtype: int
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this WorkflowRun.


        :param update_time: The update_time of this WorkflowRun.  # noqa: E501
        :type: int
        """

        self._update_time = update_time

    @property
    def variables(self):
        """Gets the variables of this WorkflowRun.  # noqa: E501


        :return: The variables of this WorkflowRun.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """Sets the variables of this WorkflowRun.


        :param variables: The variables of this WorkflowRun.  # noqa: E501
        :type: dict(str, object)
        """

        self._variables = variables

    @property
    def workflow_id(self):
        """Gets the workflow_id of this WorkflowRun.  # noqa: E501


        :return: The workflow_id of this WorkflowRun.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this WorkflowRun.


        :param workflow_id: The workflow_id of this WorkflowRun.  # noqa: E501
        :type: str
        """

        self._workflow_id = workflow_id

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
        if issubclass(WorkflowRun, dict):
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
        if not isinstance(other, WorkflowRun):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
