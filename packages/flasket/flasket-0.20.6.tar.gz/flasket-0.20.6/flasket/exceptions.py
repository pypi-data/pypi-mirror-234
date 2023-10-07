"""
Classes
-------

HTTPException
^^^^^^^^^^^^^

.. autoclass:: HTTPException
  :show-inheritance:
  :members:

.. HTTPExceptions
.. ^^^^^^^^^^^^^^
..
.. .. autoclass:: HTTPExceptions
..   :noindex:
..   :members:

NoContent
^^^^^^^^^

.. autoclass:: NoContent
  :show-inheritance:
  :members:

BadRequest
^^^^^^^^^^

.. autoclass:: BadRequest
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

Unauthorized
^^^^^^^^^^^^

.. autoclass:: Unauthorized
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

Forbidden
^^^^^^^^^

.. autoclass:: Forbidden
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

NotFound
^^^^^^^^

.. autoclass:: NotFound
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

FailedDependency
^^^^^^^^^^^^^^^^

.. autoclass:: FailedDependency
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

InternalServerError
^^^^^^^^^^^^^^^^^^^

.. autoclass:: InternalServerError
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*

NotImplemented
^^^^^^^^^^^^^^

.. autoclass:: NotImplemented
  :show-inheritance:
  :members:

  *(Content generated from Flask documentation)*
"""

from werkzeug import exceptions as exception

__all__ = [
    "BadRequest",
    "FailedDependency",
    "Forbidden",
    "HTTPException",
    "InternalServerError",
    "NoContent",
    "NotFound",
    "NotImplemented",
    "ServiceUnavailable",
    "Unauthorized",
]

# Notes on exceptions handling and errors:
# https://werkzeug.palletsprojects.com/en/master/exceptions/
# https://tools.ietf.org/html/rfc7807
HTTPException = exception.HTTPException


# 204 No Content
class NoContent(HTTPException):
    """
    *204 No Content*

    Indicates that the server has successfully fulfilled the request and that there is no content to send in the response payload body.
    """

    code = 204
    name = "No Content"


# 400 Bad Request
BadRequest = exception.BadRequest

# 401 Unauthorized
Unauthorized = exception.Unauthorized

# 403 Forbidden
Forbidden = exception.Forbidden

# 404 NotFound
NotFound = exception.NotFound

# 424 FailedDependency
FailedDependency = exception.FailedDependency

# 500 InternalServerError
InternalServerError = exception.InternalServerError

# 501 NotImplemented
# pylint: disable=redefined-builtin
NotImplemented = exception.NotImplemented

# 503 ServiceUnavailable
ServiceUnavailable = exception.ServiceUnavailable


class HTTPExceptions:
    """
    Minimal class for inheritance by :ref:`flasket.properties.FlasketProperties` class

    This class recieves all members of the ``flasket.exceptions`` module.
    """


# Copy all symbols above into HTTPExceptions
for x in __all__:
    setattr(HTTPExceptions, x, locals()[x])
