Copy / Move
===========

Copying an object
-----------------

To copy a content object send a POST request to the ``/@copy`` endpoint at the
destinations url with the source object specified in the request body. The source
object can be specified either by url, path, UID or intid.

.. example-code::

  .. code-block:: http-request

    POST /Plone/@copy HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json

    {
        "source": "http://localhost:8080/Plone/front-page"
    }

  .. code-block:: curl

    curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"source": "http://localhost:8080/Plone/front-page"}' --user admin:admin -X POST http://localhost:8080/Plone/@copy

If the copy operation succeeds, the server will respond with status 200 (OK) and return
the new and old url of the copied object.

.. literalinclude:: _json/copy.json
   :language: js


Moving an object
----------------

To move a content object send a POST request to the ``/@move`` endpoint at the
destinations url with the source object specified in the request body. The source
object can be specified either by url, path, UID or intid.

.. example-code::

  .. code-block:: http-request

    POST /Plone/folder/@move HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json

    {
        "source": "http://localhost:8080/Plone/front-page"
    }

  .. code-block:: curl

    curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"source": "http://localhost:8080/Plone/front-page"}' --user admin:admin -X POST http://localhost:8080/Plone/folder/@move

If the move operation succeeds, the server will respond with status 200 (OK) and return
the new and old url of the moved object.

.. literalinclude:: _json/copy.json
   :language: js


Copying/moving multiple objects
-------------------------------

Multiple objects can be moved/copied by giving a list of sources.

.. example-code::

  .. code-block:: http-request

    POST /Plone/@copy HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json

    {
        "source": [
            "http://localhost:8080/Plone/front-page",
            "http://localhost:8080/Plone/news"
        ]
    }

  .. code-block:: curl

    curl -i -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"source": ["http://localhost:8080/plone/front-page", "http://localhost:8080/Plone/news"]}' --user admin:admin -X POST http://localhost:8080/Plone/@copy
