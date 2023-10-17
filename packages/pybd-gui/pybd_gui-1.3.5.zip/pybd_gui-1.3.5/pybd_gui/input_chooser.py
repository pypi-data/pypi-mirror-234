import tkinter
import tkinter as tk
from tkinter import ttk

from tkinter import ttk
from tkinter.messagebox import showinfo

from pybd_gui.tkinter_utils import my_toplevel_window

import py_block_diagram as pybd

import copy

from krauss_misc import string_cleaner



# Updated approach:
# 
# - the current main gui tries to show or hide the set input 1 and set input 2
#   buttons as appropriate or whatever, but it is clunky and doesn't work well
#   and takes up too much space
# - I want a new approach that has a set input(s) option from the menu
# - the updated input chooser dialog will let me choose the block whose
#   input(s) I am setting at the top
# - based on the block selected, the input 2 options and possible other options 
#   will be shown or hidden
# - cases like an if_block with a third (or zeroth) input will be handled in 
#   a way that is scalable and generalizable


class input_chooser(my_toplevel_window):
    def __init__(self, block, parent, title="Input Chooser Dialog", \
                 geometry='350x600', selected_index=0):
        super().__init__(parent, title=title, geometry=geometry)
        self.bd = self.parent.bd
        self.selected_index = selected_index

        self.columnconfigure(0, weight=4)
        self.block = block
        self.block_name = self.block.variable_name
        self.N = self.block.num_inputs
        self.setfunc = self.block.set_input_block1
        self.main_label_text = "Choose the input for block: %s" % self.block_name 
        self.make_widgets()


    def make_widgets(self):
        ## These are the new parameters for inputs:
        ##           num_inputs = 1, \
        ##         gui_input_labels=['Input 1'], \
        ##        set_input_func_names=['set_input_block1'], \
        
        mycol = 0
        if self.N == 1:
            base = "Setting the input for %s"
        elif self.N > 1:
            base = "Setting the inputs for %s"
        top_label_text = base % self.block_name
        self.top_label = self.make_label(top_label_text, root=self)
        self.grid_widget(self.top_label, row=0, col=mycol, padx=10, pady=5, sticky='nw')
        ## - I need to put this in some kind of loop
        #self.make_label_and_grid_sw(self.main_label_text, 0, mycol)
        #self.make_combo_and_var_grid_nw("input_chooser", 1, mycol)
        self.all_block_names = self.bd.find_single_output_blocks_and_sensors()
        print("all_block_names:")
        pybd.print_list(self.all_block_names)

        self.other_block_names = copy.copy(self.all_block_names)
        #remove the block from possible inputs if it is in the list
        if self.block_name in self.all_block_names:
            myind = self.all_block_names.index(self.block_name)
            self.other_block_names.pop(myind)
        
        # make a combox box and string var for each input
        self.input_vars = []
        currow = 1
        for i in range(self.N):
            # make widget
            curlabel = self.block.gui_input_labels[i]
            self.make_label_and_grid_sw(curlabel, currow, mycol)
            currow += 1
            basename = string_cleaner.label_to_attr_name(curlabel)
            var_name = basename + '_var'
            cur_combo = self.make_combo_and_var_grid_nw(basename, currow, mycol)
            cur_var = getattr(self, var_name)
            self.input_vars.append(cur_var)
            currow += 1
            cur_combo['values'] =  self.other_block_names
            get_name_attr = self.block.get_input_func_names[i]
            get_name_func = getattr(self.block, get_name_attr)
            in_name = get_name_func()
            if in_name:
                if in_name in self.other_block_names:
                    myindex = self.other_block_names.index(in_name)
                    cur_combo.current(myindex)
        #self.input_chooser_combobox.bind('<<ComboboxSelected>>', self.input_combo_selected)
        
        # go button
        self.go_button = self.make_button_and_grid("Set Input", 10, mycol, \
                                                   command=self.on_go_button)


    def on_go_button(self, *args, **kwargs):
        print("on_go_button pressed")
        # - get the chosen block name for each input
        # - set the inputs
        for i in range(self.N):
            cur_var = self.input_vars[i]
            input_name = cur_var.get()
            print("input_name: %s" % input_name)
            if input_name in self.bd.block_dict:
                input_block = self.bd.get_block_by_name(input_name)
            elif input_name in self.bd.sensors_dict:
                input_block = self.bd.get_sensor_by_name(input_name)
            func_name = self.block.set_input_func_names[i]
            myfunc = getattr(self.block, func_name)
            myfunc(input_block)
        # what does the line below do?
        #self.parent.blocklistbox.select_set(self.selected_index)
        self.destroy()
        # - get name from combobox
        # - get the selected block by name
        # - call the set input method of self.block
        # - handle second input if applicable



class input2_chooser(input_chooser):
    def __init__(self, block, parent, title="Input 2 Chooser Dialog", \
                 geometry='300x200', selected_index=0):   
        my_toplevel_window.__init__(self, parent, title=title, geometry=geometry)
        self.bd = self.parent.bd
        self.selected_index = selected_index
        self.columnconfigure(0, weight=4)
        self.block = block
        self.block_name = self.block.variable_name
        self.setfunc = self.block.set_input_block2
        self.main_label_text = "Choose input 2 for block: %s" % self.block_name 
        self.make_widgets()
