__author__ = "The ProSuite Authors"
__copyright__ = "Copyright 2021-2023, The ProSuite Authors"
__license__ = "MIT"
__version__ = "1.0.1.0"
__maintainer__ = "Dira GeoSystems"
__email__ = "programmers@dirageosystems.ch"
__date__  = "16.01.2023"
__status__ = "Production"


from datetime import datetime
from typing import List
from prosuite.issue_filter import IssueFilter
from prosuite.parameter import Parameter
from prosuite.dataset import BaseDataset
from prosuite.factories.enums import *

class IssueFilters:
    @classmethod
    def not_yet_implemented(cls, feature_class: BaseDataset, tolerance: float) -> IssueFilter:
        """
        Stay tuned
        """
        
        result = IssueFilter("dummy(0)")
        return result