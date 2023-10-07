 # data_entry2.py

- A spreadsheet interface for data entry in Python/Jupyter 


Requires: ipydatagrid

To use:

      import data_entry2

      de = data_entry2.sheet("name")

This creates or loads name.csv and presents as a "live"
spreadsheet-like interface. This is for data entry only, no
 calculations are possible in the spreadsheet.

Put a # in front of a row to comment it out
Put a $ in front of a column name to comment out the column (useful for
non-numeric columns)

Simple expressions can be evaluated, eg: =1+3/np.sqrt(3)

Generate Vectors generates a series of arrays for each non-commented
column.

Two pandas data frames are also created:

- one is self.df that contains just the data in the vectors.
- the other, self.fdf is strings that has everything in the whole table.

To take a snapshot of a current sheet and generate a new one:
    de2 = data_entry2.sheet_copy("old", "new")

if new.csv exists, it gets loaded, if not, old.csv is copied to new.csv.

Add Row and Add Column do what they claim. To *remove* unwanted
empty rows and columns, just re-run the cell that sets up the
sheet. empty rows and columns will be deleted.

Copy & Paste only work for single cells.

To edit a cell - click and start typing. If you want to edit a current
value: try double clicking - doesn't always take, might need a few tries.
Or click and press F2.

After editing a cell, enter moves to next cell down, probably want Tab to
move to next cell to right. (shift tab goes left).

There is a top row of cell headers shown that allows: column
widths to be adjusted, and filters and sorting. Probably the
sorting and filters should not be available. Display of these
headers can be disabled by setting: header_visibility='row' in the
call to DataGrid, but then the widths can't be adjusted...
Can always restore the correct order by sorting key by ascending.
To make that work there are some extra spaces included in front of
the Variable and Units row headers

In order to help avoid disasterous data loss: every time Generate
Vectors is pressed, a snapshot of the current sheet is saved in
csv_backups (as long as it is different from the most recent
backup).  You can poke around in there and make copies of the
backups, rename them and move up to where the notebook can use it.

BUGS: the sheet will only render when the notebook is exported if
Settings->Auto Save Widget State is toggled on.

To output all sheets: call
   display_sheets()
As long as each sheet was created with a different variable name,
they will all be displayed.
