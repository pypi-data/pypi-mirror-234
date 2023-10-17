import tkinter
import tkinter as tk
from tkinter import ttk

from tkinter import ttk
from tkinter.messagebox import showinfo

from pybd_gui.tkinter_utils import my_toplevel_window

import py_block_diagram as pybd

import copy

class multi_block_selector(my_toplevel_window):
    def __init__(self, parent, title="Input Chooser Dialog", \
                 geometry='500x400', selected_index=0, main_label_text="hello"):        
        super().__init__(parent, title=title, geometry=geometry)
        self.bd = self.parent.bd
        self.columnconfigure(0, weight=4)
        self.main_label_text = main_label_text
        self.set_all_blocks()
        self.make_widgets()


    def set_all_blocks(self):
        """All might not necessarily mean all...."""
        self.all_block_names = self.bd.block_name_list
        

    def make_widgets(self):
        mycol = 0
        self.make_label_and_grid_sw(self.main_label_text, 0, mycol)
        self.make_label_and_grid_sw("Blocks", 1, mycol)
        self.make_listbox_and_var("blocklist", 2, mycol, selectmode="multiple")
        self.blocklist_var.set(self.all_block_names)

        # go button
        self.go_button = self.make_button_and_grid("Done", 10, mycol, \
                                                   command=self.on_go_button)


    def on_go_button(self, *args, **kwargs):
        raise NotImplementedError



class print_block_selector(multi_block_selector):
    """Plants with two outputs do not work as print blocks, but
    sensors can also be print blocks."""
    def set_all_blocks(self):
        all_block_names = self.bd.block_name_list

        printable_blocks = []
        for block_name in all_block_names:
            block = self.bd.get_block_by_name(block_name)
            if not isinstance(block, pybd.plant_with_double_actuator_two_sensors):
                printable_blocks.append(block_name)

        # append all sensor names (might need to revisit later)
        printable_blocks += self.bd.sensor_name_list
        self.all_block_names = printable_blocks


    def on_go_button(self, *args, **kwargs):
        print("on_go_button pressed")
        selected_indices = self.blocklist_listbox.curselection()
        #print("selected_indices:")
        block_name_list = []
        for item in selected_indices:
            curname = self.blocklist_listbox.get(item)
            block_name_list.append(curname)
        print("block_name_list:" + str(block_name_list))
        self.bd.set_print_blocks_from_names(block_name_list)
        self.destroy()
        # - get name from combobox
        # - get the selected block by name
        # - call the set input method of self.block
        # - handle second input if applicable



class print_block_selector_v2(print_block_selector):
    def __init__(self, parent, title="Print Blocks Dialog 2.0", \
                 geometry='600x300', selected_index=0, main_label_text="Print Blocks Dialog"):        
        super().__init__(parent, title=title, geometry=geometry)
        self.bd = self.parent.bd
        self.columnconfigure(0, weight=4)
        self.main_label_text = main_label_text
        self.set_all_blocks()
        self.make_widgets()


    def make_widgets(self):
        mycol = 0
        self.make_label_and_grid_sw(self.main_label_text, 0, mycol)
        self.make_label_and_grid_sw("Remaining Blocks", 1, mycol)
        self.make_listbox_and_var("remaining_blocklist", 2, mycol, selectmode="multiple")
        self.remaining_blocklist_var.set(value=self.all_block_names)
        self.select_all_button = self.make_button_and_grid("Select All", 3, mycol, \
                                                           command=self.on_select_all_button)
        self.remaining_blocks_list = copy.copy(self.all_block_names)


        mycol = 1
        self.add_button = self.make_button_and_grid("Add -->", 2, mycol, \
                                                    command=self.on_add_button)


        mycol = 2
        self.make_label_and_grid_sw("Print Blocks", 1, mycol)
        self.make_listbox_and_var("print_blocklist", 2, mycol)
        #self.blocklist_var.set(self.all_block_names)
        self.print_blocks_list = []

        # go button
        self.go_button = self.make_button_and_grid("Done", 10, mycol, \
                                                   command=self.on_go_button)


        mycol = 3   
        self.button_frame_R = ttk.Frame(self)
        currow = 0
        sub_col = 0
        mykwargs = {'root':self.button_frame_R, \
                    'pady':5}
        self.move_up_button = self.make_button_and_grid("Move Up", currow, sub_col, \
                                                        command=self.on_move_up_button,\
                                                        **mykwargs)
        currow += 1
        self.move_down_button = self.make_button_and_grid("Move Down", currow, sub_col, \
                                                        command=self.on_move_down_button,\
                                                        **mykwargs)
        currow += 1
        self.remove_button = self.make_button_and_grid("Remove", currow, sub_col, \
                                                        command=self.on_remove_button,\
                                                        **mykwargs)
 
        self.button_frame_R.grid(row=2, column=3)


    def on_select_all_button(self, *args, **kwargs):
        print("in on_select_all_button")
        self.remaining_blocklist_listbox.select_set(0, 'end')


    def _update_listboxes(self):
        self.remaining_blocklist_var.set(self.remaining_blocks_list)
        self.print_blocklist_var.set(self.print_blocks_list)

    

    def on_add_button(self, *args, **kwargs):
        print("in on_add_button")
        selected_indices = self.remaining_blocklist_listbox.curselection()
        print("selected indices: " + str(selected_indices))

        selected_names = []

        for ind in selected_indices:
            cur_item = self.remaining_blocks_list[ind]
            selected_names.append(cur_item)
            self.print_blocks_list.append(cur_item)

        print("selected_names: " + str(selected_names))

        for item in selected_names:
            self.remaining_blocks_list.remove(item)
        
        self._update_listboxes()
        


    def on_move_up_button(self, *args, **kwargs):
        """Take the current selection and move it up one spot in the list.
           - the selected index should decrement

           Practical python:
               - get current index
               - pop item at the index
               - insert item at index-1
        """
        print("in on_move_up_button")
        selected_index = self.print_blocklist_listbox.curselection()[0]
        print("selected_index: " + str(selected_index))
        if selected_index > 0:
            item = self.print_blocks_list.pop(selected_index)
            print("item: " + str(item))
            dest_index = selected_index-1
            self.print_blocks_list.insert(dest_index, item)
            self._update_listboxes()
            self.print_blocklist_listbox.selection_clear(0, 'end')
            self.print_blocklist_listbox.select_set(dest_index)


    def on_move_down_button(self, *args, **kwargs):
        print("in on_move_down_button")
        selected_index = self.print_blocklist_listbox.curselection()[0]
        print("selected_index: " + str(selected_index))
        N = len(self.print_blocks_list)
        if selected_index < N-1:
            item = self.print_blocks_list.pop(selected_index)
            print("item: " + str(item))
            dest_index = selected_index+1
            self.print_blocks_list.insert(dest_index, item)
            self._update_listboxes()
            self.print_blocklist_listbox.selection_clear(0, 'end')
            self.print_blocklist_listbox.select_set(dest_index)


    def on_remove_button(self, *args, **kwargs):
        print("in on_remove_button")
        selected_index = self.print_blocklist_listbox.curselection()[0]
        print("selected_index: " + str(selected_index))
        item = self.print_blocks_list.pop(selected_index)
        self.remaining_blocks_list.append(item)
        self._update_listboxes()
        self.print_blocklist_listbox.selection_clear(0, 'end')



    def on_go_button(self, *args, **kwargs):
        print("on_go_button pressed")
        print("block_name_list:" + str(self.print_blocks_list))
        self.bd.set_print_blocks_from_names(self.print_blocks_list)
        self.destroy()
        # - get name from combobox
        # - get the selected block by name
        # - call the set input method of self.block
        # - handle second input if applicable


