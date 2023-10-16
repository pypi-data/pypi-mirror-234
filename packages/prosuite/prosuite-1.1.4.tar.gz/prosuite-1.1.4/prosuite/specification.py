from prosuite.condition import Condition
import typing


class Specification:
    def __init__(self, name: str = 'Custom Specification', description: str = ''):
        """
        CustomSpecification stores conditions.
        :param name: specification name
        :type name: str
        :param description: specification description
        :type description: str
        """
        self._conditions: typing.List[Condition] = []
        self.name = name
        self.description = description

    def add_condition(self, condition: Condition):
        """
        Adds conditions to the specification
        """
        self._conditions.append(condition)

    def get_conditions(self) -> typing.List[Condition]:
        """
        Returns the List of conditions
        """
        return self._conditions
