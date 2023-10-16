from typing import List
from prosuite.parameter import Parameter


class IssueFilter():
    def __init__(self, name, expression: str):
        self.parameters: List[Parameter] = []
        self.name = name
        self.expression = expression
