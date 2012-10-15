"""
Helper Functions
****************

The following functions allow opening an existing remote table (for
reading or writing) and creating new remote tables (write-only). All of
these methods return a remote table handler.

"""

from dxpy.bindings import *

def open_dxgtable(dxid, project=None, keep_open=None, mode=None):
    '''
    :param dxid: table ID
    :type dxid: string
    :param keep_open: Deprecated. Use the *mode* parameter instead.
    :type keep_open: boolean
    :param mode: One of "r", "w", or "a" for read, write, and append modes, respectively
    :type mode: string
    :rtype: :class:`~dxpy.bindings.dxgtable.DXGTable`

    Given the object ID of an existing table, returns a
    :class:`~dxpy.bindings.dxgtable.DXGTable` object for reading (with
    :meth:`~dxpy.bindings.dxgtable.DXGTable.get_rows`) or writing (with
    :meth:`~dxpy.bindings.dxgtable.DXGTable.add_row` or
    :meth:`~dxpy.bindings.dxgtable.DXGTable.add_rows`).

    Example::

      with open_dxgtable("table-xxxx") as dxgtable:
          for row in dxgtable.get_rows():
              print row[1] # Prints the value in the first column (after the row ID) for this row

    Note that this function is shorthand for the following::

        DXGTable(dxid)

    '''

    return DXGTable(dxid, project=project, keep_open=keep_open, mode=mode)

def new_dxgtable(columns=None, indices=None, init_from=None, keep_open=None, mode=None,
                 **kwargs):
    '''
    :param columns: An ordered list containing column descriptors.  See :meth:`~dxpy.bindings.dxgtable.DXGTable.make_column_desc` (required if *init_from* is not provided)
    :type columns: list of column descriptors
    :param indices: An ordered list containing index descriptors. See description in :func:`~dxpy.bindings.dxgtable.DXGTable._new`.
    :type indices: list of index descriptors
    :param init_from: GTable from which to initialize the metadata including column and index specs
    :type init_from: :class:`~dxpy.bindings.dxgtable.DXGTable`
    :param keep_open: Deprecated. Use the *mode* parameter instead.
    :type keep_open: boolean
    :param mode: One of "w" or "a" for write and append modes, respectively
    :type mode: string
    :returns: Remote table handler for the newly created table
    :rtype: :class:`~dxpy.bindings.dxgtable.DXGTable`

    Additional optional parameters not listed: all those under
    :func:`dxpy.bindings.DXDataObject.new`.

    Creates a new remote GTable with the given columns. If indices are
    given, the GTable will be indexed by the requested indices at the
    time that the table is closed.

    Example::

        col_descs = [dxpy.DXGTable.make_column_desc("a", "string"),
                     dxpy.DXGTable.make_column_desc("b", "int32")]
        with new_dxgtable(columns=col_descs, mode='w') as dxgtable:
            dxgtable.add_rows([["foo", 23], ["bar", 7]])

        gri_cols = [dxpy.DXGTable.make_column_desc("chr", "string"),
                    dxpy.DXGTable.make_column_desc("lo", "int32"),
                    dxpy.DXGTable.make_column_desc("hi", "int32")]
        gri_index = dxpy.DXGTable.genomic_range_index("chr", "lo", "hi")
        indexed_table = new_dxgtable(columns=gri_cols, indices=[gri_index])

    Note that this function is shorthand for the following::

        dxgtable = DXGTable()
        dxgtable.new(columns, **kwargs)

    '''

    dxgtable = DXGTable(keep_open=keep_open, mode=mode)
    dxgtable.new(columns=columns, indices=indices, init_from=init_from, **kwargs)
    return dxgtable

def extend_dxgtable(dxid, columns, indices=None, keep_open=None, mode=None, **kwargs):
    '''
    :param dxid: Object ID of table to extend
    :type dxid: string
    :param columns: An ordered list containing column descriptors.  See :meth:`~dxpy.bindings.dxgtable.DXGTable.make_column_desc`.
    :type columns: list of column descriptors
    :param indices: An ordered list containing index descriptors. See description in :func:`~dxpy.bindings.dxgtable.DXGTable.extend`.
    :type indices: list of index descriptors
    :param keep_open: Deprecated. Use the *mode* parameter instead.
    :type keep_open: boolean
    :param mode: One of "w" or "a" for write and append modes, respectively
    :type mode: string
    :rtype: :class:`~dxpy.bindings.dxgtable.DXGTable`

    Additional optional parameters not listed: all those under
    :func:`dxpy.bindings.DXDataObject.new`.

    Given the object ID of an existing table and a list of new columns with
    which to extend the table, creates a new remote table that is ready to be
    written to.

    Example::

        new_cols = [dxpy.DXGTable.make_column_desc("newcol", "double"),
                    dxpy.DXGTable.make_column_desc("anothercol", "int32")]
        with extend_dxgtable(old_dxgtable.get_id(), columns=new_cols, name="extended") as dxgtable:
            dxgtable.add_rows([[2.5498, 93]])

    Note that this function is shorthand for the following::

        DXGTable(dxid).extend(columns, **kwargs)

    '''

    return DXGTable(dxid).extend(columns, indices, keep_open=keep_open, mode=mode, **kwargs)
