The Oasys.PRIMER package allows Python scripts to control the Oasys LS-DYNA Environment
software `PRIMER <https://www.oasys-software.com/dyna/software/primer/>`_.

Basic Information
-----------------

The module uses gRPC to communicate with the PRIMER executable using the `Oasys.gRPC <https://pypi.org/project/Oasys.gRPC/>`_ module.

**The Python API is currently in Beta testing for version 21.0. If you would like to be involved in testing it then please contact dyna.support@arup.com**.

Getting started
---------------

As python is running outside PRIMER, the first thing a script needs to do is to either start an instance of PRIMER, or to connect to an already running
instance of PRIMER. At the end of the script you should then either disconnect again or terminate the PRIMER instance.

A skeleton python script to start PRIMER (Installed at C:\\Oasys 21\\primer21_x64.exe) and then terminate it is::

    import Oasys.PRIMER

    connection = Oasys.PRIMER.start(abspath="C:\\Oasys 21\\primer21_x64.exe")

    ...

    Oasys.PRIMER.terminate(connection)

By default PRIMER will use port 50051 to communicate with Python and will allocate 25Mb of memory for running scripts. These can be changed by adding port and memory arguments to the start function. e.g::

    connection = Oasys.PRIMER.start(abspath="C:\\Oasys 21\\primer21_x64.exe", port=1234, memory=100)

To connect to an instance of PRIMER that is already running, **PRIMER must currently have been started in a special mode telling it to listen on a port for gRPC messages**. 
This is done by using the ``-grpc`` command line argument when starting PRIMER. e.g::

    'C:\\Oasys 21\\primer21_x64.exe' -grpc=50051

A skeleton script to connect to PRIMER and disconnect again would then be::

    import Oasys.PRIMER

    connection = Oasys.PRIMER.connect(port=50051)

    ...

    Oasys.PRIMER.disconnect(connection)

or if you want to terminate the instance of PRIMER use ``terminate`` instead of ``disconnect``.

Python API
----------

The JS API has been available for several years, is stable and works well, so we have designed the Python API to have the same classes, methods and properties as the JS API.
The Python API is currently in beta release and does not yet have any documentation, so for information on the available classes etc please see the `Oasys JS API documentation <https://www.oasys-software.com/dyna/downloads/oasys-suite/>`_.

However, the following classes are not available:

*   PopupWindow (GUIs not available from Python)
*   Window (GUIs not available from Python)
*   Widget (GUIs not available from Python)
*   WidgetItem (GUIs not available from Python)
*   Check (Custom checks not available from Python)
*   File (use Python i/o instead)
*   Graphics (Graphics drawing not available from Python)
*   Ssh (use python modules instead)
*   XlsxWorkbook (use python modules instead)
*   XlsxWorksheet (use python modules instead)
*   XMLParser (use python modules instead)
*   Zip (use python modules instead)

and the following methods are not available:

*   ForEach
*   Error
*   Warning

If an argument in the JS API is an object then the equivalent in Python will be a dict, and if an array in JS, the equivalent in Python will be a list.

Simple Example
--------------

It's probably easier to give a simple example of how to do something in PRIMER using Python compared to JavaScript, so here is simple example that makes a new model containing some nodes and shells using the JS API::

    var m = new Model();

    Message("Making nodes");

    for (y=0; y<11; y++)
    {
        for (x=0; x<11; x++)
            var n = new Node(m, 1+x+(y*11), x*10, y*10, 0);
    }

    Message("Making shells");

    for (i=1; i<=10; i++)
    {
        for (j=1; j<=10; j++)
            var s = new Shell(m, i+(j*10), i, ((i-1)*11)+j+0, ((i-1)*11)+j+1, ((i-0)*11)+j+1, ((i-0)*11)+j+0);
    }

    m.UpdateGraphics();
    View.Show(View.XY);
    View.Ac();

and here is the equivalent example in Python::

    import Oasys.PRIMER

    connection = Oasys.PRIMER.start(abspath="C:\\oasys 21\\primer21_x64.exe")

    m = Oasys.PRIMER.Model()

    Oasys.PRIMER.Message("Making nodes")

    for y in range(0, 11):
        for x in range(0, 11):
            Oasys.PRIMER.Node(m, 1+x+(y*11), x*10, y*10, 0)

    Oasys.PRIMER.Message("Making shells")

    for i in range(1, 11):
        for j in range(1, 11):
            Oasys.PRIMER.Shell(m, i+(j*10), i, ((i-1)*11)+j+0, ((i-1)*11)+j+1, ((i-0)*11)+j+1, ((i-0)*11)+j+0)

    m.UpdateGraphics()
    Oasys.PRIMER.View.Show(Oasys.PRIMER.View.XY)
    Oasys.PRIMER.View.Ac()

    Oasys.PRIMER.disconnect(connection)

More Information
----------------

For more details on the Oasys LS-DYNA environment software please see

* Website: `https://www.oasys-software.com/dyna/software/ <https://www.oasys-software.com/dyna/software/>`_
* Linkedin: `https://www.linkedin.com/company/oasys-ltd-software/ <https://www.linkedin.com/company/oasys-ltd-software/>`_
* YouTube: `https://www.youtube.com/c/OasysLtd <https://www.youtube.com/c/OasysLtd>`_
* Email: `dyna.support@arup.com <mailto:dyna.support@arup.com>`_
