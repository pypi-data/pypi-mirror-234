class LikeInterfaceError(Exception):
    ...


class DecodeError(LikeInterfaceError):
    ...


class LikeAPIError(LikeInterfaceError):
    ...


class LikeNetworkError(LikeAPIError):
    ...
