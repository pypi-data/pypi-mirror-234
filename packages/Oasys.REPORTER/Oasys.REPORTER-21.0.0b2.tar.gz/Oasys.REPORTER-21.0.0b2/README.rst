The Oasys.REPORTER package allows Python scripts to control the Oasys LS-DYNA Environment
software `REPORTER <https://www.oasys-software.com/dyna/software/reporter/>`_.

Basic Information
-----------------

The module uses gRPC to communicate with the REPORTER executable using the `Oasys.gRPC <https://pypi.org/project/Oasys.gRPC/>`_ module.

**The Python API is currently in Beta testing for version 21.0. If you would like to be involved in testing it then please contact dyna.support@arup.com**.

Getting started
---------------

As python is running outside REPORTER, the first thing a script needs to do is to either start an instance of REPORTER, or to connect to an already running
instance of REPORTER. At the end of the script you should then either disconnect again or terminate the REPORTER instance.

A skeleton python script to start REPORTER (Installed at C:\\Oasys 21\\reporter21_x64.exe) and then terminate it is::

    import Oasys.REPORTER

    connection = Oasys.REPORTER.start(abspath="C:\\Oasys 21\\reporter21_x64.exe")

    ...

    Oasys.REPORTER.terminate(connection)

By default REPORTER will use port 50053 to communicate with Python and will allocate 25Mb of memory for running scripts. These can be changed by adding port and memory arguments to the start function. e.g::

    connection = Oasys.REPORTER.start(abspath="C:\\Oasys 21\\reporter21_x64.exe", port=1234, memory=100)

To connect to an instance of REPORTER that is already running, **REPORTER must currently have been started in a special mode telling it to listen on a port for gRPC messages**. 
This is done by using the ``-grpc`` command line argument when starting REPORTER. e.g::

    'C:\\Oasys 21\\reporter21_x64.exe' -grpc=50053

A skeleton script to connect to REPORTER and disconnect again would then be::

    import Oasys.REPORTER

    connection = Oasys.REPORTER.connect(port=50053)

    ...

    Oasys.REPORTER.disconnect(connection)

or if you want to terminate the instance of REPORTER use ``terminate`` instead of ``disconnect``.

Python API
----------

The JS API has been available for several years, is stable and works well, so we have designed the Python API to have the same classes, methods and properties as the JS API.
The Python API is currently in beta release and does not yet have any documentation, so for information on the available classes etc please see the `Oasys JS API documentation <https://www.oasys-software.com/dyna/downloads/oasys-suite/>`_.

However, the following classes are not available:

*   Ssh (use python modules instead)
*   XlsxWorkbook (use python modules instead)
*   XlsxWorksheet (use python modules instead)
*   XMLParser (use python modules instead)
*   Zip (use python modules instead)

If an argument in the JS API is an object then the equivalent in Python will be a dict, and if an array in JS, the equivalent in Python will be a list.

Simple Example
--------------

It's probably easier to give a simple example of how to do something in REPORTER using Python compared to JavaScript, so here is simple example that creates a new Template and adds a text item on the first page using the JS API::

    var t = new Template();
    var p = t.GetPage(0);

    var i = new Item(p, Item.TEXT, "example", 100, 100, 150, 150);
    i.text = "Example";
    i.fontSize = 48;
    i.textColour = Colour.Red()

and here is the equivalent example in Python::

    import Oasys.REPORTER

    connection = Oasys.REPORTER.start(abspath="C:\\oasys 21\\reporter21_x64.exe")

    t = Oasys.REPORTER.Template()
    p = t.GetPage(0)

    i = Oasys.REPORTER.Item(p, Oasys.REPORTER.Item.TEXT, "example", 100, 100, 150, 150)
    i.text = "Example"
    i.fontSize = 48
    i.textColour = Oasys.REPORTER.Colour.Red()
    

    Oasys.REPORTER.disconnect(connection)

More Information
----------------

For more details on the Oasys LS-DYNA environment software please see

* Website: `https://www.oasys-software.com/dyna/software/ <https://www.oasys-software.com/dyna/software/>`_
* Linkedin: `https://www.linkedin.com/company/oasys-ltd-software/ <https://www.linkedin.com/company/oasys-ltd-software/>`_
* YouTube: `https://www.youtube.com/c/OasysLtd <https://www.youtube.com/c/OasysLtd>`_
* Email: `dyna.support@arup.com <mailto:dyna.support@arup.com>`_

