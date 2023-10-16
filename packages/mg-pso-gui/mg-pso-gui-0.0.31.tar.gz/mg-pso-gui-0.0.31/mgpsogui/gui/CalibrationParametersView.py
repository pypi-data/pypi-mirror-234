from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkEntry
import tkinter as tk

global option_manager

class CalibrationParametersView(CTkScrollableFrame):
    def __init__(self, *args,
                 option_manager: None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        
        self.option_manager = option_manager
        self.key_values = option_manager.get_arguments()['calibration_parameters']
        self.edit_mode = False
        
        self.render()

    def clear(self):
        self.containerFrame.destroy()
        
    def toggle_edit_mode(self):
        self.clear()
        self.edit_mode = not self.edit_mode
        self.render()
        
    def render(self):
        row = 0
        index = 0
        
        self.containerFrame = CTkFrame(self)
        self.containerFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.containerFrame.grid_columnconfigure((0, 1), weight=1)
        
        CTkLabel(self.containerFrame, text="Name:").grid(row=row, column=0, columnspan=1, padx=5, pady=5, sticky="")
        CTkLabel(self.containerFrame, text="Value:").grid(row=row, column=1, columnspan=1, padx=5, pady=5, sticky="")
        row += 1
        
        for key_value_pair in self.key_values:
            CTkEntry(self.containerFrame, textvariable=self.key_values[index]["name"]).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
            if self.edit_mode:
                return_func = lambda index=index: (self.clear(), self.option_manager.remove_calibration_parameter(index), self.render())
                CTkButton(self.containerFrame, text="Remove", command=return_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
            else:
                bb = CTkEntry(self.containerFrame)
                bb.grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")
                bb.configure(textvariable=self.key_values[index]["value"])
            row += 1
            index += 1
            
        if self.edit_mode:
            CTkButton(self.containerFrame, text="Exit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
        else:
            CTkButton(self.containerFrame, text="Edit", command=self.toggle_edit_mode).grid(row=row, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
            
        add_key_func = lambda: (self.clear(), self.option_manager.add_calibration_param("name", "value"), self.render())
        CTkButton(self.containerFrame, text="Add Parameter", command=add_key_func).grid(row=row, column=1, padx=(5, 5), pady=(5, 5), sticky="ew")