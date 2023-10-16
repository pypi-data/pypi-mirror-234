class DataMasterApiError(Exception):
    """
    Исключения, которые выдаются API датамастера
    """


class WrongDataMasterApiVersion(DataMasterApiError):
    """
    Попытка использовать API датамастера, которое несовместимо с API AW
    """


class AwModelForbidden(DataMasterApiError):
    """
    Доступ к модели запрещен
    """


class AwClientMisconfigured(Exception):
    """ """
