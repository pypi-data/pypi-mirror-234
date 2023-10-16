__all__ = ['Condition']
from prosuite.issue_filter import IssueFilter
from prosuite.parameter import Parameter
from typing import List


class Condition:
    """
    Defines a quality condition, i.e. the configuration of a test algorithm with for one or more 
    datasets. Conditions must be created with the factory methods from :py:mod:`prosuite.factories.quality_conditions` 
    """

    def __init__(self, test_descriptor: str, name: str = ""):

        #:
        self.name = name
        """
        The unique name of the quality condition.
        """
        #:
        self.test_descriptor = test_descriptor
        """
        The test descriptor, i.e. the algorithm used to verify this condition.
        """
        
        #: TODO: Rename to IssueType or add enum IssueType {Warning|Error} or Serverity 
        # New doc: The type/severity of the quality issues identified by this quality condition. Quality conditions with 
        # “Issue Type = Warning” are considered “soft” conditions, for which exceptions (“Allowed Issues”) may be defined.
        self.allow_errors: bool = False
        """
        For internal use only.
        """
        #:
        self.category: str = ""
        """
        The name of the category, if this issue is assigned to a category.
        """
        #:
        self.stop_on_error: bool = False
        """
        Indicates if the occurrence of an error for an object should stop any further testing of the same object. 
        This can be used to prevent further tests on a feature after a serious geometry error (e.g. incorrectly 
        oriented rings) was detected for the feature.
        The used Test Descriptor provides a standard value for this property. It can optionally be overridden here.
        """
        #:
        self.description: str = ""
        """
        Freely definable description of the Quality Condition. This description can be displayed when viewing 
        issues in the issue navigator, and may contain explanations to the Quality Condition and instructions for 
        correcting the issues.
        """
        #:
        self.url: str = ""
        """
        Optional URL to a website providing additional information for this Quality Condition.
        Certain Quality Conditions require more detailed information about the test logic and/or the correction 
        guidelines than the field “Description” can provide. This information can for example be assembled in a 
        wiki, and the URL may be provided here. When viewing issues in the issue navigator, the corresponding web 
        page can be opened. In the HTML verification reports these URLs are used to render the names of the 
        Quality Conditions as links.
        """
        #:
        self.parameters: List[Parameter] = []
        """
        The list of parameters. Typically the parameters are specified in the factory method used to create the
        quality condition (see :py:mod:`prosuite.factories.quality_conditions`) and do not need to be changed
        through this list.
        """
        #:
        self.issue_filters: List[IssueFilter] = []
        """
        Reserved for future use.
        """
        #:
        self.issue_filter_expression: str
        """
        Reserved for future use.
        """

    def generate_name(self):
        """
        Generates a technical name using the dataset name(s) and the test descriptor. This is the default name of 
        a condition if it was created by the standard factory method from :py:mod:`prosuite.factories.quality_conditions`.
        """
        first_dataset_parameter = next(
            (p for p in self.parameters if p.is_dataset_parameter), None)
        if first_dataset_parameter:
            ds_param: Parameter = first_dataset_parameter
            if ds_param.contains_list_of_datasets:
                dataset_list: List[str] = [ds.name for ds in ds_param.dataset]
                dataset_names = "_".join(dataset_list)
                self.name = f"{self.test_descriptor} {dataset_names}"
            else:
                self.name = f"{self.test_descriptor} {ds_param.dataset.name}"
