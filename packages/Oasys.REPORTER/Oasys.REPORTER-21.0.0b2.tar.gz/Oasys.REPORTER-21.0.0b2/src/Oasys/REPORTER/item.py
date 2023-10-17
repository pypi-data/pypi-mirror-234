import Oasys.gRPC


# Metaclass for static properties and constants
class ItemType(type):
    _consts = {'ARROW', 'AUTO_TABLE', 'D3PLOT', 'ELLIPSE', 'IMAGE', 'IMAGE_FILE', 'LIBRARY_IMAGE', 'LIBRARY_PROGRAM', 'LINE', 'NOTE', 'PLACEHOLDER', 'PRIMER', 'PROGRAM', 'RECTANGLE', 'SCRIPT', 'SCRIPT_FILE', 'TABLE', 'TEXT', 'TEXTBOX', 'TEXT_FILE', 'THIS'}

    def __getattr__(cls, name):
        if name in ItemType._consts:
            return Oasys.REPORTER._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Item(Oasys.gRPC.OasysItem, metaclass=ItemType):
    _props = {'active', 'autotableType', 'bottomCrop', 'bottomMargin', 'columns', 'conditions', 'embed', 'file', 'fillColour', 'fontName', 'fontSize', 'fontStyle', 'generatedRowHeight', 'headerHeight', 'height', 'job', 'justify', 'leftCrop', 'leftMargin', 'lineColour', 'lineStyle', 'lineWidth', 'name', 'resolution', 'rightCrop', 'rightMargin', 'rows', 'saveCSV', 'saveCSVFilename', 'saveXlsx', 'saveXlsxFilename', 'script', 'text', 'textColour', 'topCrop', 'topMargin', 'width', 'x', 'x2', 'y', 'y2'}
    _rprops = {'filetype', 'type'}


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the properties we define then get it
        if name in Item._props:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

# If one of the read only properties we define then get it
        if name in Item._rprops:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the properties we define then set it
        if name in Item._props:
            Oasys.REPORTER._connection.instanceSetter(self.__class__.__name__, self._handle, name, value)
            return

# If one of the read only properties we define then error
        if name in Item._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Constructor
    def __init__(self, page, type, name=Oasys.gRPC.defaultArg, x=Oasys.gRPC.defaultArg, x2=Oasys.gRPC.defaultArg, y=Oasys.gRPC.defaultArg, y2=Oasys.gRPC.defaultArg):
        handle = Oasys.REPORTER._connection.constructor(self.__class__.__name__, page, type, name, x, x2, y, y2)
        Oasys.gRPC.OasysItem.__init__(self, self.__class__.__name__, handle)


# Static methods
    def GetAll(page):
        """
        Get all of the items on a page

        Parameters
        ----------
        page : Page
            Page to get items from

        Returns
        -------
        list
            List of Item objects
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetAll", page)

    def GetFromName(page, name):
        """
        Get an Item from its name

        Parameters
        ----------
        page : Page
            Page to get item from
        name : string
            Item name

        Returns
        -------
        Item
            Item object (or None if item cannot be found)
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "GetFromName", page, name)



# Instance methods
    def DeleteColumn(self, column):
        """
        Delete a column from a table. Valid for item type Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        column : integer
            The index of the column to delete. Note that indices start from 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteColumn", column)

    def DeleteRow(self, row):
        """
        Delete a row from a table. Valid for item type Item.TABLE

        Parameters
        ----------
        row : integer
            The index of the row to delete. Note that indices start from 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "DeleteRow", row)

    def Generate(self):
        """
        Generate an item

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "Generate")

    def GetCellProperties(self, row, column):
        """
        Get the properties of the specified cell. Valid for item type Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        row : integer
            The row index of the cell of interest. Note that indices start from 0
        column : integer
            The column index of the cell of interest. Note that indices start from 0

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCellProperties", row, column)

    def GetColumnProperties(self, column, header):
        """
        Get an autotable column properties. Valid for item type Item.AUTO_TABLE

        Parameters
        ----------
        column : integer
            The index of the column of interest. Note that indices start from 0
        header : constant
            An argument to signify to get the properties of the header or the generated rows. Can be Reporter.AUTO_TABLE_HEADER or 
            Reporter.AUTO_TABLE_ROWS

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetColumnProperties", column, header)

    def GetColumnWidth(self, row):
        """
        Get the width of a table column. Valid for item types Item.TABLE or Item.AUTO_TABLE

        Parameters
        ----------
        row : integer
            The index of the column of interest. Note that indices start from 0

        Returns
        -------
        int
            Integer. The width of the specified column
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetColumnWidth", row)

    def GetCondition(self, index):
        """
        Get the conditional formatting data for an item. Valid for item types Item.TEXT_FILE,
        Item.PROGRAM,
        Item.TEXT or
        Item.TEXTBOX (for 
        Item.AUTO_TABLE and 
        Item.TABLE, see GetCondition functions with additional arguments below)

        Parameters
        ----------
        index : integer
            The index of the condition to get. Note that indices start from 0. See conditions for the total number
            of comditions

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCondition", index)

    def GetAutotableCondition(self, index, column):
        """
        Get the conditional formatting data for an Item.AUTO_TABLE item

        Parameters
        ----------
        index : integer
            The index of the condition to get. Note that indices start from 0
        column : integer
            The column to get the condition from. Note that indices start from 0

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCondition", index, column)

    def GetTableCondition(self, index, row, column):
        """
        Get the conditional formatting data for an Item.TABLE item

        Parameters
        ----------
        index : integer
            The index of the condition to get. Note that indices start from 0
        row : integer
            The cell row to get the condition from. Note that indices start from 0
        column : integer
            The cell column to get the condition from. Note that indices start from 0

        Returns
        -------
        dict
            Dict with properties
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetCondition", index, row, column)

    def GetGeneratedData(self, row_index, column_index):
        """
        Get the text that appears in an autotable cell once generated. Valid for item type Item.AUTO_TABLE

        Parameters
        ----------
        row_index : integer
            The index of the row of interest. Note that indices start from 0
        column_index : integer
            The index of the column of interest. Note that indicies start from 0

        Returns
        -------
        ?
            String: the text displayed in the specified row and column
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetGeneratedData", row_index, column_index)

    def GetRowHeight(self, row):
        """
        Get the height of a table row. Valid for item type Item.TABLE

        Parameters
        ----------
        row : integer
            The index of the row of interest. Note that indices start from 0

        Returns
        -------
        int
            integer
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "GetRowHeight", row)

    def InsertColumn(self, column):
        """
        Insert a column into a table. Valid for item types Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        column : integer
            The index of the position where the inserted column will end up. Note that indices start from 0. If no argument is given, a column will be added to the bottom of the table

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertColumn", column)

    def InsertRow(self, row):
        """
        Insert a row into a table. Valid for item type Item.TABLE

        Parameters
        ----------
        row : integer
            The index of the position where the inserted row will end up. Note that indices start from 0. If no argument is given, a row will be added to the bottom of the table

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "InsertRow", row)

    def MergeCells(self, topleftrow, topleftcolumn, rows, columns):
        """
        Merge specified cells in a table. Valid for item types Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        topleftrow : integer
            The row index of the top-left cell in the group of cells to be merged. Note that indices start from 0
        topleftcolumn : integer
            The column index of the top-left cell in the group of cells to be merged. Note that indices start from 0
        rows : integer
            The number of rows of cells to be merged (measured from the topLeftRow position)
        columns : integer
            The number of columns of cells to be merged (measured from the topLeftColumn position)

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "MergeCells", topleftrow, topleftcolumn, rows, columns)

    def SetCellProperties(self, properties, row, column):
        """
        Set the properties of the specified cell. Valid for item type Item.TABLE

        Parameters
        ----------
        properties : dict
            An object containing the cell properties
        row : integer
            The row index of the cell to be modified. Note that indices start from 0
        column : integer
            The column index of the cell to be modified. Note that indices start from 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCellProperties", properties, row, column)

    def SetColumnProperties(self, properties, column, header):
        """
        Set the properties of an autotable column. Valid for item type Item.AUTO_TABLE

        Parameters
        ----------
        properties : dict
            Set the properties of an autotable column. Valid for item type Item.AUTO_TABLE
        column : integer
            The index of the column of interest. Note that indices start from 0
        header : constant
            An argument to signify to set the properties of the header or the generated rows. Can be Reporter.AUTO_TABLE_HEADER or 
            Reporter.AUTO_TABLE_ROWS

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetColumnProperties", properties, column, header)

    def SetColumnWidth(self, column, width):
        """
        Set the width of a table column. Valid for item type Item.TABLE

        Parameters
        ----------
        column : integer
            The index of the column of interest. Note that indices start from 0
        width : float
            The column width

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetColumnWidth", column, width)

    def SetCondition(self, condition, properties):
        """
        Set the specified condition for an item. Valid for item types Item.TEXT_FILE,
        Item.PROGRAM,
        Item.TEXT or
        Item.TEXTBOX (for 
        Item.AUTO_TABLE and 
        Item.TABLE, see SetCondition functions with additional arguments below)

        Parameters
        ----------
        condition : integer
            The index of the condition you wish to set. Note that indices start at 0. If a condition already exists at the specified index, it will be replaced.
            To add a new condition, specify an index equal to the number of existing conditions
        properties : dict
            The index of the condition you wish to set. Note that indices start at 0. If a condition already exists at the specified index, it will be replaced.
            To add a new condition, specify an index equal to the number of existing conditions

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCondition", condition, properties)

    def SetAutotableCondition(self, condition, column, properties):
        """
        Set the specified condition for an Item.AUTO_TABLE item

        Parameters
        ----------
        condition : integer
            The index of the condition you wish to set. Note that indices start at 0. If a condition already exists at the specified index, it will be replaced.
            To add a new condition, specify an index equal to the number of existing conditions
        column : integer
            The column to set the condition for. Note that indices start from 0
        properties : dict
            The column to set the condition for. Note that indices start from 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCondition", condition, column, properties)

    def SetTableCondition(self, condition, row, column, properties):
        """
        Set the specified condition for an Item.TABLE item

        Parameters
        ----------
        condition : integer
            The index of the condition you wish to set. Note that indices start at 0. If a condition already exists at the specified index, it will be replaced.
            To add a new condition, specify an index equal to the number of existing conditions
        row : integer
            The row to set the condition for. Note that indices start from 0
        column : integer
            The column to set the condition for. Note that indices start from 0
        properties : dict
            The column to set the condition for. Note that indices start from 0

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetCondition", condition, row, column, properties)

    def SetRowHeight(self, row, height):
        """
        Set the height of a table row. Valid for item type Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        row : integer
            The index of the row of interest. Note that indices start from 0
        height : float
            The row height

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "SetRowHeight", row, height)

    def UnmergeCells(self, row, column):
        """
        Unmerge the specified cell in a table. All cells merged to the specified cell will be unmerged. Valid for item types Item.TABLE and Item.AUTO_TABLE

        Parameters
        ----------
        row : integer
            The row index of the cell to be unmerged. Note that indices start from 0
        column : integer
            The column index of the cell to be unmerged. Note that indices start from 0.

        Returns
        -------
        None
            No return value
        """
        return Oasys.REPORTER._connection.instanceMethod(self.__class__.__name__, self._handle, "UnmergeCells", row, column)

