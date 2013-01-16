"""Quick and dirty conversion of SAGE worksheets to IPython notebooks.

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
"""


preamble_string = """{
 "metadata": {
  "name": "pyclaw_tutorial"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
"""

post_string = """
   ]
  }
 ]
}
"""

cell_strings = {'code' : 'input', 'markdown' : 'source'}

def open_cell(stream,state):
    """Write IPython notebook string to open a cell."""

    if not state['first_cell']:
        stream.write(',')
    stream.write('\n')
    
    stream.write("""
    {
     "cell_type": "%s",
     "metadata": {},
     "%s": [\n""" % (state['cell_type'],cell_strings[state['cell_type']]))

    state['first_cell'] = False
    state['cell_open']  = True
    state['first_line'] = True
    return state

def close_cell(stream, state):
    """Write IPython notebook string to close a cell."""
    if state['cell_type'] is 'code':
        stream.write("""
        ],
         "language": "python",
         "metadata": {},
         "outputs": []
        }""")
    else:
        stream.write("""
        ]
        }""")
    state['cell_open']  = False
    state['cell_type']  = None
    state['is_output']  = False
    return state

def escape_characters(line):
    """Escape special characters and remove some HTML."""
    line = line.replace("\\","\\\\")
    line = line.replace('"','\\"')
    line = line.replace('<p>','')
    line = line.replace('</p>','  ')
    line = line.replace('&nbsp;','')
    line = line.replace('&amp;','&')
    line = line.replace('&lt;','<')
    return line


def sage2ipy(path,outname):
    """Converts the .html version of a SAGE worksheet to an IPython notebook.
       All we need to know: Code cells begin and end with {{{...}}}.
       Everything not in a code cell will be put in a markdown cell.

       Any output is simply deleted.
    """
    infile = open(path+'worksheet.html','rU')
    outfile = open(outname+'.ipynb','w')
    outfile.write(preamble_string)

    i=-1
    state = {}
    state['cell_type']  = None
    state['cell_open']  = False
    state['first_line'] = True
    state['first_cell'] = True
    state['is_output']  = False

    lines=infile.readlines()
    while i<len(lines)-1:
        i=i+1
        line=lines[i]
    
        if line.startswith('}}}'):
            state = close_cell(outfile,state)
        elif state['is_output']:
            continue
        elif line.startswith('{{{'):
            if state['cell_type'] is not 'code':
                if state['cell_open']:
                    close_cell(outfile,state)
                state['cell_type'] = 'code'
                open_cell(outfile,state)
            else:
                raise Exception('Code cell starting inside a code cell')
        elif line.startswith('///'):
            state['is_output'] = True
            continue
        elif line.isspace():
            continue
        else:
            if state['cell_type'] is 'code':
                if state['first_line']:
                    state['first_line'] = False
                else:
                    outfile.write(',\n')
                line = line.replace('\\','\\\\')
                line = line.replace('"','\\"')
                outfile.write(' '*13 + '"'+line[:-1]+r'\n'+'"')
            elif state['cell_type'] is 'markdown':
                outfile.write(',\n')
                line = escape_characters(line)
                outfile.write(' '*13 + '"'+line[:-1]+'"')
            elif state['cell_type'] is None:
                state['cell_type'] = 'markdown'
                open_cell(outfile,state)
                line = escape_characters(line)
                outfile.write(' '*13 + '"'+line[:-1]+'"')

    outfile.write(post_string)
    outfile.close()

def convert_all_sage_worksheets(user):
    """Convert all worksheets belonging to 'user'.
    Uses default path to SAGE worksheets on Mac OS X.
    Note that worksheet titles won't be preserved,
    because they're not stored in the worksheet file
    (SAGE must keep an index somewhere else).
    """
    import os
    import pickle

    path = '/Users/'+user+'/.sage/sage_notebook.sagenb/home/admin'
    worksheets = [x for x in os.listdir(path) if x.isdigit()]
    for worksheet in worksheets:
        ws_path = path+'/'+worksheet+'/'
        f = open(ws_path+'worksheet_conf.pickle')
        ws_data = pickle.load(f)
        ws_name = ws_data['name']
        sage2ipy(ws_path,ws_name)
