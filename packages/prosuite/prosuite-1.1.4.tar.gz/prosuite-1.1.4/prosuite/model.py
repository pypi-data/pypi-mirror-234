class Model:
    """
    The Model represents the data model in a workspace (file-gdb or enterprise-gdb)

    catalog_path examples:
        c:/data.gdb
        c:/enterprise_gdb.sde
    """

    def __init__(self, name, catalog_path):

        #:
        self.name: str = name
        """
        The unique name of the model.
        """
        #:
        self.catalog_path: str = catalog_path
        """
        The catalog path of the associated workspace.
        """
