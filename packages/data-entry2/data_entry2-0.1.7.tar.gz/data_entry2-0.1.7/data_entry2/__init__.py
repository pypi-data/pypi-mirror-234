"""
     LICENSE:

     This program is free software: you can redistribute it and/or
     modify it under the terms of the GNU General Public License as
     published by the Free Software Foundation, either version 3 of
     the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

import numpy as np
import pandas as pd
import ipydatagrid as dg
import ipywidgets as widgets
import re
import pickle
from IPython import get_ipython
import time
import glob
import filecmp
import shutil
import os
temp_var = None

BACKUP_DIR= 'csv_backups/'
num_sheets = 0

# callback_count=0
class sheet:
    """ A spreadsheet-like interface in a Jupyter Notebook

    """



    # function called on every cell update:
    def my_callback(self, cell):
        # global callback_count

        row = cell["row"]
        column = cell["column"]
        column_index = cell["column_index"]
        value = cell["value"]

        #with self.out:
        #    print("Callback number:",callback_count, row,column_index,value)
        #    callback_count += 1
            
        if value == self.mar[row, column_index]:
            #with self.out:
            #    print("value unchanged quitting")
                #with self.out:
                #    print("unchanged, but reduing doing_undo")
            return

        self.out.clear_output()
        with self.out:
            print("Data vectors need to be updated")

        # for undo list:
        undo_event = (row, column_index, self.mar[row, column_index])
            
        # sanitize - remove any commas:
        self.mar[row, column_index] = str(value)
        if value == None:
            value = ""
            self.mar[row, column_index] = value
            # self.grid.on_cell_change(self.my_callback, remove=True)
            self.grid.set_cell_value_by_index(column_index, row, value)
            # self.grid.on_cell_change(self.my_callback)
            #with self.out:
            #    print('None replaced with ""')
        if ',' in value:
            value = value.replace(',', ';') 
            #self.callback_recur = 2
            self.mar[row, column_index] = value
            # self.grid.on_cell_change(self.my_callback, remove=True)
            self.grid.set_cell_value_by_index(column_index, row, value)
            # self.grid.on_cell_change(self.my_callback)
            with self.out:
                print("Comma in cell replaced with ;")
        #with self.out:
        #    print("cell val is:",value)

        # Deal with undo list:
        if self.doing_undo == False:
            if self.was_undoing:
                # move redo_list to undo_list:
                self.undo_list = self.undo_list + self.redo_list
                self.redo_list = []
                self.was_undoing = False
            
            # add this event to the undo list: undo/redo saves the list itself.
#            try: 
#                old_val = self.mar[row, column_index]
#            except: # if it didn't exist before:
#                old_val = ""
            self.undo_list = self.undo_list + [undo_event]
            self.save_undo_list(self.undo_list)
            #with self.out:
            #    print("added to undo list:",self.undo_list[-1])
        else:
            self.doing_undo = False
            #with self.out:
            #    print("was undoing?")
        # save the sheet:
        self.mar = self.grid.data.to_numpy()

#        with self.out:
#            print("mar is:")
#            print(self.mar)
        try:
            np.savetxt(self.fname, self.mar, fmt='%s', delimiter=',')
        except:
            with self.out:
                print("Failed to save csv file!")

        return
        ###


    def add_row(self, e):
        current_grid_df = self.grid.data
        myshape = current_grid_df.shape
        rows, cols = myshape
    
        additional_row = pd.DataFrame(
            columns = current_grid_df.columns, 
            #index = [current_grid_df.index[-1] + 1],
            index = [rows-2],
            data = "" * len(current_grid_df.columns)
        )
        self.grid.data = pd.concat([self.grid.data, additional_row], ignore_index=False)

        # adjust height of grid: 
        # height = (rows+2) * self.grid.base_row_size + 30
        height = (rows+1) * self.grid.base_row_size + 30 + self.grid.base_column_header_size
        self.grid.layout = {"height":str(height)+"px"}

        self.mar = self.grid.data.to_numpy()


        #def remove_row(e):
    #    current_grid_df = grid.get_visible_data()
    #    grid.data = current_grid_df.drop(current_grid_df.tail(1).index)

    def add_col(self, e):
        current_grid_df = self.grid.data
        myshape = current_grid_df.shape
        rows, cols = myshape
        name = cols
        # spaces in Index so that sort works...
        Index = ["  Variable:", " Units:"] + list(range(rows-2))
        additional_col = pd.DataFrame(
            [""] * rows, columns = [name], index=Index
        )

        self.grid.data = pd.concat([self.grid.data, additional_col], axis=1, ignore_index=False)
        #df = pd.concat([self.grid.data, additional_col], axis=1, ignore_index=False)
        #self.build_grid(df)
        self.mar = self.grid.data.to_numpy()

        #with self.out:
        #    print(self.grid.data)

        return
#    def remove_col(e):
#        current_grid_df = grid.get_visible_data()
#        cols = current_grid_df.columns
#        grid.data = current_grid_df.drop(columns=cols[-1])
#        return

    def undo(self, _):
        if len(self.undo_list) < 1:
            return
        self.was_undoing = True
        self.doing_undo = True
        
        r,c,v = self.undo_list.pop()

        #with self.out:
        #    print("undo:",r,c,v)
            
        current_grid_df = self.grid.data
        myshape = current_grid_df.shape
        rows, cols = myshape

        
        if r >= rows:
            with self.out:
                print("adding",r-rows+1,"rows")
            for i in range(r-rows+1):
                self.add_row(0)
        if c >= cols:
            for i in range(c-cols+1):
                self.add_col(0)
        try:
            old_val = self.mar[r,c]
        except:
            old_val = ''
        self.redo_list = self.redo_list + [(r,c,old_val)]

        # self.grid.on_cell_change(self.my_callback, remove=True)
        result = self.grid.set_cell_value_by_index(c, r, v)
        # self.grid.on_cell_change(self.my_callback)

        # for save:
        save_list = self.undo_list + self.redo_list
        self.save_undo_list(save_list)
        
    def redo(self, _):
        if len(self.redo_list) < 1:
            return
        self.was_undoing = True
        self.doing_undo = True
        r,c,v = self.redo_list.pop()
        self.undo_list = self.undo_list + [(r,c,self.mar[r,c])]
        # self.grid.on_cell_change(self.my_callback, remove=True)
        self.grid.set_cell_value_by_index(c, r, v)
        # self.grid.on_cell_change(self.my_callback)
       
        #self.doing_undo = False

        # for save:
        save_list = self.undo_list + self.redo_list
        self.save_undo_list(save_list)
        
    def generate(self, _, silent=False):
        global temp_var
        current_grid_df = self.grid.data
        myshape = current_grid_df.shape
        rows, cols = myshape
        self.out.clear_output()

        with self.out:
            # Look at column names, sanitize and find commented columns
            vnames = []
            for j in range(cols):
                vn = self.mar[0,j]
                # fix up so its a legal variable name: 
                # remove any [ or ]
                vn = vn.replace('[', '').replace(']', '')
                # append Vec then convert any illegal character to _ but remove trailing _
                vn2 = re.sub("[^0-9a-zA-Z]+", "_", vn).rstrip('_') + 'Vec'
                # print("col",j,", name is",vn2)
                # Check for duplicates
                if vn2 in vnames and vn2 != 'Vec':
                    if silent == False:
                        print("Duplicate column name:",vn2)
                        print("Aborting")
                    return
                if vn2 == 'Vec':
                    if silent == False:
                        print("Skipping column", j, "because it does not have a valid name")
                if vn2[0].isalpha() == False and vn2[0] != '_':
                    print("Variable names must begin with a letter.\nPlease change column name:",vn2,"so it begins with a letter")
                    print("Skipping this column")
                    vn2 = 'Vec'
                # names that start with $ are commented out columns:
                if len(vn) > 0:
                    if vn[0] == '$':
                        vn2 = 'Vec'
                        if silent == False:
                            print("Skipping column", j, vn, 'because it is commented')
                vnames = vnames + [vn2]
            # now go through rows and build array
            nar = np.zeros((rows-2, cols))
            mrow = 0
            row_indices = [] # for data frame
            for i in range(2, rows):
                # within the row, check that all are legal numeric values:
                try:
                    for j in range(cols):
                        if vnames[j] != 'Vec':
                            # look to see if first character is =, if so, evaluate.
                            if self.mar[i,j][0] == '=':
                                # print("Found an = sign, evaluating",self.mar[i,j][1:])
                                nar[mrow, j] = float(eval(self.mar[i,j][1:]))
                            else:
                                nar[mrow, j] = float(self.mar[i, j])
                    row_indices = row_indices + [i-2]
                    mrow += 1
                except:
                    if silent == False:
                        if '#' not in self.mar[i,j] and '$' not in self.mar[i,j]:
                            print("Converting Row: ", i-2, "Col: ",j , "with value",self.mar[i,j],"Failed")
                        print("Row #",i-2,"skipped")
            # make the arrays:
            if mrow > 0:
                if silent == False:
                    print("Found",mrow,"valid rows")
                # print(nar[:mrow])

                col_names = [] # for data frame
                col_arrays = []
                # ok, create the variables:
                for j in range(cols):
                    if vnames[j] != 'Vec':
                        # insert our array:
                        
                        # this inserts into our object, not a bad idea maybe?
                        # command = 'self.'+vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        # exec(command)
                        
                        # this is into the global module namespace. Not useful inside object.
                        # command = 'self.'+vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        # globals()[vnames[j]] = nar[:mrow, j]
                        
                        # this makes it global when in notebook: TESTING CM
                        temp_var= np.array(nar[:mrow,j])
                        # need to know what our object is?
                        command = vnames[j]+' = __data_entry2_object__.temp_var.copy()'
                        fcommand = vnames[j]+' = np.array('+str(list(nar[:mrow, j]))+')'
                        try:
                            get_ipython().ex(command)
                            
                            # prep to make dataframe.
                            col_names = col_names + [vnames[j][:-3]] # chop off the Vec in the name
                            col_arrays = col_arrays + [nar[:mrow, j]]
                            if silent == False:
                                # print("\nCreated array:",vnames[j], "with values:")
                                # print(str(list(nar[:mrow, j])))
                                print("\nCreated array:\n", fcommand)
                        except:
                            if silent == False:
                                print('Failed to create array. Ensure that column names are valid and that this module was imported without changing its name!.')
                            break
                # make a data frame - place inside our object.
                if len(col_names) > 0 and len(row_indices) > 0:
                    # print(col_arrays)
                    # print(col_names)
                    col_arrays = np.array(col_arrays).transpose()
                    self.df = pd.DataFrame(col_arrays, row_indices, col_names)
                    
            else: # no valid rows found
                if silent == False:
                    print("No valid data rows found. Giving up")
            # Also build a dataframe out of text that looks like our entire sheet:
            self.fdf = pd.DataFrame(self.mar[1:], ['Units']+list(range(rows-2)) , self.mar[0])
            # this doesn't quite work???
            # command = "display_sheet(%i)\n"%(self.sheet_num)
            # get_ipython().ex(command)
            ## display(self.fdf) # TODO was in old version.
            
            # now do file checkpointing. If current file is different from most recent checkpoint, save a checkpoint.

            # need to find all checkpoints
            dir_entries = glob.glob(BACKUP_DIR + self.fname + '*')
            # print(dir_entries)
            # go through them, look for numerical suffixes and look for latest:
            maxtime = 0
            maxindex = 0
            mintime = int(time.time())
            minindex = 0
            num_backups = 0
            for i in range(len(dir_entries)):
                fields = dir_entries[i].split('.')
                # print(fields)
                try:
                    stime = int(fields[-1])
                    num_backups += 1
                    # print(stime)
                    if stime > maxtime:
                        maxtime = stime
                        maxindex = i
                    if stime < mintime:
                        mintime = stime
                        minindex = i
                except:
                    pass
                
            if num_backups > 1:
                if filecmp.cmp(dir_entries[maxindex], self.fname) == True:
                    return
                
            utime = int(time.time())
            backup_name = BACKUP_DIR + self.fname + '.' + str(utime)
            # print("backup_name will be",backup_name)
            shutil.copyfile(self.fname, backup_name)

            # If there are more than 10 checkpoints, remove the oldest.
            if num_backups > 9:
                os.remove(dir_entries[minindex])

    def save_undo_list(self, list_to_save):
        try:
            undo_file = open(self.undo_name, "wb")
            pickle.dump(list_to_save, undo_file)
            undo_file.close()
        except:
            with self.out:
                print("Couldn't save undo history file. Permisions?")



    def __init__ (self, name):
        """ Create a spreadsheet-like interface in a Jupyter Notebook
        
        Argument: a file name for a csv file
        """
        global num_sheets, BACKUP_DIR

        # define a function that can generate a pointer to this module in the global namespace
        # we do this in here because a %reset -f removes it from the global namespace
        command = \
            "def __data_entry2_find_ourselves__():\n"+\
            "    global __data_entry2_object__\n"+\
            "    for name, val in globals().items():\n"+\
            "        try:\n"+\
            "            if val.__name__ == 'data_entry2':\n"+\
            "                return val\n"+\
            "        except:\n"+\
            "            pass\n"+\
            "    print('Could not find the data_entry2 module object. Vector creation will not work!')"
        get_ipython().ex(command)

        get_ipython().ex("__data_entry2_object__ = __data_entry2_find_ourselves__()")

        self.mar = None
        oar = None

        # again %reset -f removes this from global namespace?
        # set up global function for displaying all sheets
        command = \
            "def display_sheets():\n"+\
            "    for i in globals():\n"+\
            "        if type(globals()[i]) == __data_entry2_object__.sheet:\n" +\
            "            print('Sheet:', i, '  File:', globals()[i].fname)\n"+\
            "            display(globals()[i].fdf)\n"
        get_ipython().ex(command)
        
        self.undo_list = []
        self.redo_list = []

        self.doing_undo = False
        self.was_undoing = False
        
        self.out = widgets.Output()
        
        self.sheet_num = num_sheets
        num_sheets += 1
        
        # if there are any / in the file name, give up.
        if name.find('/') != -1:
            print("file name cannot refer to a different path. Remove any / characters from file name.")
            return None
        
        if not os.path.exists(BACKUP_DIR):
            print("Creating directory for backups: ",BACKUP_DIR)
            os.makedirs(BACKUP_DIR)

        
        self.fname = name + '.csv'
        self.undo_name = BACKUP_DIR + name + '.csv.undo'
        if (len(name) >= 4): # if the user's name ends in .csv, don't add it again.
            if name[-4:] == '.csv':
                self.fname = name
                self.undo_name = BACKUP_DIR + name + '.undo'


        # oar = old array, loaded in
        # mar is always the current array
        # nar is used when generating final output vectors, local to generate()
        # oar and mar are arrays of strings. nar is an array of floats.
    
        # Here see if fname (.csv) exists, and if so load it:
        file_read_ok = False
        try:
            oar = np.loadtxt(self.fname, dtype=str, delimiter=',', comments=None)
            if oar.ndim == 1:
                oar = oar.reshape((len(oar),1))
            rows, cols = oar.shape
            # look for empty columns:
            # can we remove empty columns:
            col = cols-1 # cols is the number of cols, col is the one we're looking at.
            all_empty = True
            while (col > 0):
                for i in range(rows):
                    if oar[i, col] != "":
                        all_empty = False
                        col = 0
                        break
                if all_empty == True:
                    # print("removing col:",col)
                    cols = cols -1
                    oar = oar[:,:-1]
                    col = col -1
            # can we remove empty rows:
            row = rows-1
            all_empty = True
            while (row > 0):
                for i in range(cols):
                    if oar[row, i] != "":
                        all_empty = False
                        row = 0
                        break
                if all_empty == True:
                    # print("removing row:",row)
                    rows = rows -1
                    oar = oar[:-1,:]
                    row = row -1
            if rows < 4:
                newa = np.empty((4-rows,cols),dtype=str)
                oar = np.vstack((oar,newa))
                rows = 4
            if cols < 2:
                newa = np.empty((rows,2-cols),dtype=str)
                oar = np.hstack((oar,newa))
                cols = 2
                
            file_read_ok = True
        except:
            rows = 10
            cols = 3
            oar = np.empty((rows,cols), dtype=str)
        if file_read_ok:
            try:
                # print("trying to open undo file")
                undo_file = open(self.undo_name, 'rb')
                self.undo_list = pickle.load(undo_file)
                undo_file.close()
                # print("undo_list",self.undo_list)
                # limit length of undo list?
                if len(self.undo_list) > 500:
                    self.undo_list = self.undo_list[len-500:]
            except:
                print("Creating undo file")
                pass

                    
        add_row_button = widgets.Button(description='Add Row')
        add_row_button.on_click(self.add_row)

        add_col_button = widgets.Button(description='Add Column')
        add_col_button.on_click(self.add_col)

        undo_button = widgets.Button(description='Undo')
        undo_button.on_click(self.undo) 

        redo_button = widgets.Button(description='Redo')
        redo_button.on_click(self.redo) 

        generate_button = widgets.Button(description='Generate Vectors')
        generate_button.on_click(self.generate)

        # build row headers:
        # spaces in Index so that sort works...
        rh = ['  Variable:', ' Units:'] + list(range(rows-2))

        # set up height, so we can adjust it later too.
        # based on: https://github.com/bloomberg/ipydatagrid/issues/216
        # gets updated in add_row. Should we do columns too?
        
        df = pd.DataFrame(oar, index = rh) 
        self.grid = dg.DataGrid(df, selection_mode = 'cell', editable=True, header_visibility='all')

        height = rows * self.grid.base_row_size + 30 + self.grid.base_column_header_size

        layout_string = {"height":str(height)+"px"}
        self.grid.layout = layout_string
        
        self.grid.on_cell_change(self.my_callback)
        self.mar = self.grid.data.to_numpy()
        if file_read_ok == False:
            try:
                np.savetxt(self.fname, self.mar, fmt='%s', delimiter=',')
            except:
                with self.out:
                    print("Failed to save csv file!")
       
        self.save_undo_list(self.undo_list)
                
        self.hb=widgets.HBox([undo_button, redo_button, add_row_button, add_col_button, generate_button])

        # Display it:
        print("Sheet name:", self.fname)
        self.sheet = widgets.VBox([self.hb, self.grid, self.out])
        self.generate(self, silent = True) 
        display(self.sheet)
        return None


def sheet_copy(old_sheet, new_sheet):
    # check to see if filename(s) ends in .csv, and if so, don't add it again.
    old_name = old_sheet + '.csv'
    if len(old_sheet) > 4:
        if old_sheet[-4:] == '.csv':
            old_name = old_sheet
            
    if '/' in new_sheet or '\\' in new_sheet:
        print("New file must be in current working directory")
        return
    new_name = new_sheet + '.csv'
    if len(new_sheet) > 4:
        if new_sheet[-4:] == '.csv':
            new_name = new_sheet

    if os.path.isfile(new_name) == False: # check to see if you already have an existing filename
        if os.path.isfile(old_name) == False:
            print("Could not access source file:", old_name)
            print("Check file and path and try again.")
            return
        shutil.copyfile(old_name, new_name)
        print("Copied", old_name,"to", new_name)
    return sheet(new_name)

