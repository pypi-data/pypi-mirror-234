import tkinter
import tkinter as tk
from tkinter import ttk

#from matplotlib.backends.backend_tkagg import (
#    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import numpy as np
import copy
from tkinter import ttk
from tkinter.messagebox import showinfo

import py_block_diagram as pybd
pad_options = {'padx': 5, 'pady': 5}

from pybd_gui.tkinter_utils import my_toplevel_window, \
     window_with_param_widgets_that_appear_and_disappear, \
     value_from_str

class menu_params_dialog(my_toplevel_window, \
        window_with_param_widgets_that_appear_and_disappear):
    def __init__(self, parent, title="Edit Block Dialog"):
        super().__init__(parent, title=title, geometry="700x400")
        self.bd = self.parent.bd
        self.max_params = 6#not counting variable_name and label
        self.int_bool_list = []
        self.make_widgets()
        self.load_menu_params_from_bd()


    def make_widgets(self):
        self.global_params_list = ['','stop_t']
        currow = 0
        mycol = 0
        self.make_label_and_grid_sw("Global/System Parameters", \
                currow, mycol)
        currow += 1
        self.make_combo_and_var_grid_nw("global_params", currow, mycol)
        self.global_params_combobox['values'] =  self.global_params_list
        #currow += 1#<-- moving over, not down
        self.add_button = self.make_button_and_grid("Add Global Param", \
                                    currow, mycol+1, \
                                    command=self.on_add_global_button, \
                                    padx=5, pady=0)
        currow += 1
            
        #self.global_params_combobox.bind('<<ComboboxSelected>>', \
        #            self.on_block_selected)
 
        #def body(self):
        #print("frame: %s" % frame)
        # print(type(frame)) # tkinter.Frame
        self.block_names = self.bd.block_name_list
       
            
        #=================================
        #
        # column 0 
        #
        #=================================
        self.label1 = ttk.Label(self, text="Block")
        self.make_label_and_grid_sw("Block", currow, mycol)
        currow += 1
        self.make_combo_and_var_grid_nw("block_selector", currow, mycol)
        currow += 1
        mystart = currow
        self.block_selector_combobox['values'] =  self.block_names
        self.block_selector_combobox.bind('<<ComboboxSelected>>', \
                    self.on_block_selected)
        
        self.make_label_and_grid_sw("Block Parameters", currow, mycol)
        currow += 1
        self.make_listbox_and_var("block_params", currow, mycol)
        currow += 1


        bottom_row = 10


        self.cancel_btn = self.make_button_and_grid("Cancel", \
                                                bottom_row, mycol, \
                                                command=self.on_cancel_btn)
        currow += 1

        mycol = 1
        currow = mystart + 1
        self.add_button = self.make_button_and_grid("Add -->", currow, mycol, \
                                                    command=self.on_add_button)

        mycol = 2
        currow = mystart
        self.make_label_and_grid_sw("Menu Parameters", currow, mycol)
        currow+=1
        self.make_listbox_and_var("menu_params", currow, mycol)
        self.menu_params_list = []

        # go button
        self.go_button = self.make_button_and_grid("Done", bottom_row, mycol, \
                                                   command=self.on_go_button)


        mycol = 3   
        self.button_frame_R = ttk.Frame(self)
        currow = mystart + 1
        sub_col = 0
        mykwargs = {'root':self.button_frame_R, \
                    'pady':5}
        #self.move_up_button = self.make_button_and_grid("Move Up", currow, sub_col, \
        #                                                command=self.on_move_up_button,\
        #                                                **mykwargs)
        #currow += 1
        #self.move_down_button = self.make_button_and_grid("Move Down", currow, sub_col, \
        #                                                command=self.on_move_down_button,\
        #                                                **mykwargs)
        #currow += 1
        self.remove_button = self.make_button_and_grid("Remove", currow, sub_col, \
                                                        command=self.on_remove_button,\
                                                        **mykwargs)
 
        self.button_frame_R.grid(row=currow, column=3)


    def on_go_button(self, *args, **kwargs):
        #append_menu_param_from_block(self, block, param_name, int_only=0):
        # Steps:
        # - split strings
        # - get blocks by name
        # - call append_menu_param_from_block
        # 
        # Note that the two append methods below default to 
        # float rather than int on the Arduino level.
        # - if I load the menu params from a csv from seld.bd
        #   and save those to the combobox, I loose the int preference
        #   - I can't think of that many int menu params right now, 
        #     but throwing away the option seems risky in the long run

        # Future feature: read from self.int_bool_list
        #                 to determine if a menu_param is only
        #                 allowed to be an int

        ## Assuming we have loaded the params correctly from self.bd, 
        ## we need to clear the list in self.bd before re-appending 
        ## everything
        self.bd.menu_param_list = []#clear
        for menu_str in self.menu_params_list:
            if "." in menu_str:
                # block parameters
                block_name, param_name = menu_str.split('.',1)
                block = self.bd.get_block_by_name(block_name)
                self.bd.append_menu_param_from_block(block, param_name)
            else:
                # global parameters
                self.bd.append_menu_param_global_variable(menu_str, \
                                            int_only=0)
        self.destroy()

         


    def on_remove_button(self, *args, **kwargs):
        selected_indices = self.menu_params_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            item = self.menu_params_list.pop(selected_index)
            self.menu_params_var.set(self.menu_params_list)
            self.menu_params_listbox.selection_clear(0, 'end')


    def _get_selected_params(self):
        selected_params = []
        selected_indices = self.block_params_listbox.curselection()
        print("selected indices: " + str(selected_indices))
        
        for ind in selected_indices:
            param = self.params_list[ind]
            selected_params.append(param)

        return selected_params


    def append_to_int_bool(self):
        self.int_bool_list.append(0)#<-- no ints, only floats for menu_params
                                    #    for now.

   
    def on_add_button(self, *args, **kwargs):
        block_name = self.block_selector_var.get()
        selected_params = self._get_selected_params()
        param_strs = ["%s.%s" % (block_name, param) for param in \
                      selected_params]
        self.menu_params_list.extend(param_strs)
        self.menu_params_var.set(self.menu_params_list)


    def load_menu_params_from_bd(self, *args, **kwargs):
        param_strs = []
        int_bool_list = []
        if hasattr(self.bd, "menu_param_list"):
            for row in self.bd.menu_param_list:
                param_strs.append(row[0])
                int_bool_list.append(row[1])
        
        self.menu_params_list = param_strs
        self.int_bool_list = int_bool_list
        self.menu_params_var.set(self.menu_params_list)


   
    def on_add_global_button(self, *args, **kwargs):
        var_name = self.global_params_var.get()           
        if var_name.strip():
            print("var_name = %s" % var_name)
            self.menu_params_list.append(var_name)
            self.menu_params_var.set(self.menu_params_list)

       

    def on_block_selected(self, *args, **kwargs):
        block_name = self.block_selector_var.get()
        print("selected block name: %s" % block_name)
        block_instance = self.bd.get_block_by_name(block_name)
        self.selected_block = block_instance
        self.params_list = self.selected_block.param_list
        self.block_params_var.set(self.params_list)


    def on_save_changes_btn(self, *args, **kwargs):
        # approach:
        # - read the values from the widgets (done)
        # - see which values have changed (done)
        # - assign the changes to the block params
        # - deal with variable name changes if they have occured
        #     - how do we check for any blocks that have this block as an input?
        # - what happens if the user changed a sensor or actuator name?
        #     - do we want to make this impossible?
        #     - do we want to show comboxes for these
        other_kwargs = self.get_params_kwargs(self.N_params)
        kwargs = self.get_required_attrs_as_dict()
        kwargs.update(other_kwargs)
        self.new_kwargs = kwargs
        print("new_kwargs = %s" % self.new_kwargs)

        for key, value in self.original_kwargs.items():
            new_value = self.new_kwargs[key]
            if new_value != value:
                print("this changed: %s, %s --> %s" % (key, value, new_value))
                new_value = value_from_str(new_value)
                setattr(self.selected_block, key, new_value)
                if key == "variable_name":
                    self.bd.change_block_name(self.selected_block, new_value, value)
                    self.parent.block_list_var.set(self.bd.block_name_list)

        self.destroy()
                

    def on_cancel_btn(self, *args, **kwargs):
        print("in on_cancel_btn")
        self.destroy()
