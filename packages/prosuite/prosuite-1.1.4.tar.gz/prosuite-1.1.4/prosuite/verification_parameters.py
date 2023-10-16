import typing


class VerificationParameters():
    """
    Contains all parameters that can be passed to a verification. 

    :param tile_size: size (in meter) for testing quality conditions
    :type tile_size: int
    :param username: the executing user
    :type username: str
    """

    def __init__(self, tile_size: int = 5000, user_name: str = None) -> None:
        #:
        self.tile_size: int = tile_size
        #:
        self.user_name: str = user_name
