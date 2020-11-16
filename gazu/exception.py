class HostException(Exception):
***REMOVED***
    Error raised when host is not valid.
***REMOVED***

    pass


class AuthFailedException(Exception):
***REMOVED***
    Error raised when user credentials are wrong.
***REMOVED***

    pass


class NotAuthenticatedException(Exception):
***REMOVED***
    Error raised when a 401 error (not authenticated) is sent by the API.
***REMOVED***

    pass


class NotAllowedException(Exception):
***REMOVED***
    Error raised when a 403 error (not authorized) is sent by the API.
***REMOVED***

    pass


class MethodNotAllowedException(Exception):
***REMOVED***
    Error raised when a 405 error (method not handled) is sent by the API.
***REMOVED***

    pass


class RouteNotFoundException(Exception):
***REMOVED***
    Error raised when a 404 error (not found) is sent by the API.
***REMOVED***

    pass


class ServerErrorException(Exception):
***REMOVED***
    Error raised when a 500 error (server error) is sent by the API.
***REMOVED***

    pass


class ParameterException(Exception):
***REMOVED***
    Error raised when a 400 error (argument error) is sent by the API.
***REMOVED***

    pass


class UploadFailedException(Exception):
***REMOVED***
    Error raised when an error while uploading a file, mainly to handle cases
    where processing that occurs on the remote server fails.
***REMOVED***

    pass


class TooBigFileException(Exception):
***REMOVED***
    Error raised when a 413 error (payload too big error) is sent by the API.
***REMOVED***

    pass
