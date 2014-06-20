********
Examples
********


Management
==========

The following code block will display each :term:`technology` available on
your system:

.. code-block:: python

	import pyconnman

  	mgr = pyconnman.ConnManager()
  	technologies = mgr.list_technologies()
  	print technologies

**Example output:**

.. code-block:: python

	<add output here>
