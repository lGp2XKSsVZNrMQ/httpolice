Python API
==========

HTTPolice can be used as a Python library:
for example, to analyze requests or responses as part of a test suite.


Example
-------
.. literalinclude:: api_example.py


API reference
-------------
.. autoclass:: httpolice.Request

   .. attribute:: notices

      A list of :class:`Notice` objects reported on this request.
      Filled by :func:`~httpolice.check_exchange`.

.. autoclass:: httpolice.Response

   .. attribute:: notices

      A list of :class:`Notice` objects reported on this response.
      Filled by :func:`~httpolice.check_exchange`.

.. autoclass:: httpolice.Exchange

   .. attribute:: request

      The :class:`~httpolice.Request` object passed to the constructor.

   .. attribute:: responses

      The list of :class:`~httpolice.Response` objects
      passed to the constructor.

.. autofunction:: httpolice.check_exchange

.. class:: Notice

   .. attribute:: id
   
     The notice’s ID (an integer).
   
   .. attribute:: severity
   
     The notice’s severity.
     This is an opaque value that should only be compared to the constants
     :data:`httpolice.ERROR`, :data:`httpolice.COMMENT`,
     and :data:`httpolice.DEBUG`.

.. autofunction:: httpolice.text_report

.. autofunction:: httpolice.html_report