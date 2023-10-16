from prosuite.model import Model


class BaseDataset():
    """
    The base class for datasets representing tabular data. It is either a :class:`.Dataset` or, in the future, a :class:`.Transformer`
    """
    def __init__(self, name: str, filter_expression: str = ""):
        self.name: str = name
        self.filter_expression: str = filter_expression
        pass


class Dataset(BaseDataset):
    """
    A dataset represents data from a table or feature class in a workspace, optionally filtered by an SQL expression.

    :param name: table or featureclass name
    :type name: str
    :param model: The :class:`prosuite.model.Model` this dataset belongs to.
    :type model: class:`prosuite.model.Model`
    :param filter_expression: A where clause that filters the table. The syntax of the where clause is defined in
        the document SQLSyntax_en.pdf
    :type filter_expression: str, optional
    """

    def __init__(self, name: str, model: Model, filter_expression: str = ""):
        super().__init__(name, filter_expression)
        self.model: Model = model
