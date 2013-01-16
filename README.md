# SAGE to IPython

Quick and dirty conversion of SAGE worksheets to IPython notebooks.

See www.sagemath.org and ipython.org.
This has been tested with SAGE version 4.2.1 and IPython version 0.13.1.

Usage:

    >>> import sage2ipython
    >>> sage2ipython.sage2ipy('/path/to/sage/worksheet/html/file','output_file_name.ipynb')

Note that this does NOT operate on the (binary) .sws files.
It uses the html version of the worksheet, which can usually be found in
~/.sage/sage_notebook.sagenb/home/username/number/.
To convert all your SAGE worksheets, do:

    >>> import sage2ipython
    >>> sage2ipython.convert_all_sage_worksheets('username')

where 'username' is your account name.  You may also need to edit the 
SAGE notebook account name that occurs in the path in convert_all_sage_worksheets.

General notes/limitations:
    - All code blocks are assumed to be Python code blocks.
    - Output is simply deleted.
    - Everything else is put in Markdown cells.
    - Double backslashes are handled properly only if you have the development version of IPython.
      Otherwise, you should convert them to quadruple backslashes.

