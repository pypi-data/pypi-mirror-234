# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.579
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

from lusid.configuration import Configuration


class ComplianceSummaryRuleResultRequest(object):
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
        'rule_id': 'ResourceId',
        'template_id': 'ResourceId',
        'variation': 'str',
        'rule_status': 'str',
        'affected_portfolios': 'list[ResourceId]',
        'affected_orders': 'list[ResourceId]',
        'rule_breakdown': 'dict(str, ComplianceRuleBreakdownRequest)'
    }

    attribute_map = {
        'rule_id': 'ruleId',
        'template_id': 'templateId',
        'variation': 'variation',
        'rule_status': 'ruleStatus',
        'affected_portfolios': 'affectedPortfolios',
        'affected_orders': 'affectedOrders',
        'rule_breakdown': 'ruleBreakdown'
    }

    required_map = {
        'rule_id': 'required',
        'template_id': 'required',
        'variation': 'required',
        'rule_status': 'required',
        'affected_portfolios': 'required',
        'affected_orders': 'required',
        'rule_breakdown': 'required'
    }

    def __init__(self, rule_id=None, template_id=None, variation=None, rule_status=None, affected_portfolios=None, affected_orders=None, rule_breakdown=None, local_vars_configuration=None):  # noqa: E501
        """ComplianceSummaryRuleResultRequest - a model defined in OpenAPI"
        
        :param rule_id:  (required)
        :type rule_id: lusid.ResourceId
        :param template_id:  (required)
        :type template_id: lusid.ResourceId
        :param variation:  (required)
        :type variation: str
        :param rule_status:  (required)
        :type rule_status: str
        :param affected_portfolios:  (required)
        :type affected_portfolios: list[lusid.ResourceId]
        :param affected_orders:  (required)
        :type affected_orders: list[lusid.ResourceId]
        :param rule_breakdown:  (required)
        :type rule_breakdown: dict[str, lusid.ComplianceRuleBreakdownRequest]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._rule_id = None
        self._template_id = None
        self._variation = None
        self._rule_status = None
        self._affected_portfolios = None
        self._affected_orders = None
        self._rule_breakdown = None
        self.discriminator = None

        self.rule_id = rule_id
        self.template_id = template_id
        self.variation = variation
        self.rule_status = rule_status
        self.affected_portfolios = affected_portfolios
        self.affected_orders = affected_orders
        self.rule_breakdown = rule_breakdown

    @property
    def rule_id(self):
        """Gets the rule_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The rule_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """Sets the rule_id of this ComplianceSummaryRuleResultRequest.


        :param rule_id: The rule_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type rule_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and rule_id is None:  # noqa: E501
            raise ValueError("Invalid value for `rule_id`, must not be `None`")  # noqa: E501

        self._rule_id = rule_id

    @property
    def template_id(self):
        """Gets the template_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The template_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._template_id

    @template_id.setter
    def template_id(self, template_id):
        """Sets the template_id of this ComplianceSummaryRuleResultRequest.


        :param template_id: The template_id of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type template_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and template_id is None:  # noqa: E501
            raise ValueError("Invalid value for `template_id`, must not be `None`")  # noqa: E501

        self._template_id = template_id

    @property
    def variation(self):
        """Gets the variation of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The variation of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: str
        """
        return self._variation

    @variation.setter
    def variation(self, variation):
        """Sets the variation of this ComplianceSummaryRuleResultRequest.


        :param variation: The variation of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type variation: str
        """
        if self.local_vars_configuration.client_side_validation and variation is None:  # noqa: E501
            raise ValueError("Invalid value for `variation`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                variation is not None and len(variation) > 6000):
            raise ValueError("Invalid value for `variation`, length must be less than or equal to `6000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                variation is not None and len(variation) < 0):
            raise ValueError("Invalid value for `variation`, length must be greater than or equal to `0`")  # noqa: E501

        self._variation = variation

    @property
    def rule_status(self):
        """Gets the rule_status of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The rule_status of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: str
        """
        return self._rule_status

    @rule_status.setter
    def rule_status(self, rule_status):
        """Sets the rule_status of this ComplianceSummaryRuleResultRequest.


        :param rule_status: The rule_status of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type rule_status: str
        """
        if self.local_vars_configuration.client_side_validation and rule_status is None:  # noqa: E501
            raise ValueError("Invalid value for `rule_status`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                rule_status is not None and len(rule_status) > 6000):
            raise ValueError("Invalid value for `rule_status`, length must be less than or equal to `6000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                rule_status is not None and len(rule_status) < 0):
            raise ValueError("Invalid value for `rule_status`, length must be greater than or equal to `0`")  # noqa: E501

        self._rule_status = rule_status

    @property
    def affected_portfolios(self):
        """Gets the affected_portfolios of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The affected_portfolios of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._affected_portfolios

    @affected_portfolios.setter
    def affected_portfolios(self, affected_portfolios):
        """Sets the affected_portfolios of this ComplianceSummaryRuleResultRequest.


        :param affected_portfolios: The affected_portfolios of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type affected_portfolios: list[lusid.ResourceId]
        """
        if self.local_vars_configuration.client_side_validation and affected_portfolios is None:  # noqa: E501
            raise ValueError("Invalid value for `affected_portfolios`, must not be `None`")  # noqa: E501

        self._affected_portfolios = affected_portfolios

    @property
    def affected_orders(self):
        """Gets the affected_orders of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The affected_orders of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._affected_orders

    @affected_orders.setter
    def affected_orders(self, affected_orders):
        """Sets the affected_orders of this ComplianceSummaryRuleResultRequest.


        :param affected_orders: The affected_orders of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type affected_orders: list[lusid.ResourceId]
        """
        if self.local_vars_configuration.client_side_validation and affected_orders is None:  # noqa: E501
            raise ValueError("Invalid value for `affected_orders`, must not be `None`")  # noqa: E501

        self._affected_orders = affected_orders

    @property
    def rule_breakdown(self):
        """Gets the rule_breakdown of this ComplianceSummaryRuleResultRequest.  # noqa: E501


        :return: The rule_breakdown of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :rtype: dict[str, lusid.ComplianceRuleBreakdownRequest]
        """
        return self._rule_breakdown

    @rule_breakdown.setter
    def rule_breakdown(self, rule_breakdown):
        """Sets the rule_breakdown of this ComplianceSummaryRuleResultRequest.


        :param rule_breakdown: The rule_breakdown of this ComplianceSummaryRuleResultRequest.  # noqa: E501
        :type rule_breakdown: dict[str, lusid.ComplianceRuleBreakdownRequest]
        """
        if self.local_vars_configuration.client_side_validation and rule_breakdown is None:  # noqa: E501
            raise ValueError("Invalid value for `rule_breakdown`, must not be `None`")  # noqa: E501

        self._rule_breakdown = rule_breakdown

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
        if not isinstance(other, ComplianceSummaryRuleResultRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComplianceSummaryRuleResultRequest):
            return True

        return self.to_dict() != other.to_dict()
