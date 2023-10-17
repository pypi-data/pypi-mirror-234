#!/usr/local/bin/python3.9

import os 
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(dir_path)


import tkinter as tk
import tkinter.messagebox
import customtkinter
import json
import os
from PIL import Image
import traceback
from multiprocessing import Process
from multiprocessing import Queue
import re
import requests
import pandas as pd
import numpy as np
import ast

from ..util import PSORunner
from ..util import GraphGenerator

import subprocess
import plotly.express as px
import plotly.graph_objs as go

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from . import StepView as sv
from . import StaticParameterView as spv
from . import CalibrationParametersView as cpv
from . import OptionManager as om
from ..util.CTkToolTip import CTkToolTip as ctt

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.option_manager = om.OptionManager()
        
        self.running_config = None
        self.selected_graph_name = None

        self.process = None
        self.data_x = [0]
        self.data_y = [0]

        # configure window
        self.title("CSIP PSO")
        self.geometry(f"{1920}x{1080}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.grid_rowconfigure((0), weight=4)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CSIP PSO", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self.save_project)
        self.save_button.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", command=self.load_project)
        self.load_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        self.new_window = customtkinter.CTkButton(self.sidebar_frame, text="New Window", command=self.new_window)
        self.new_window.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scale:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["50%", "75%", "100%", "150%", "200%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")
        
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=2, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        tab1 = "Platform"
        tab2 = "Setup"
        tab3 = "Run"
        tab4 = "Visualize"
        
        self.tabview.add(tab1)
        self.tabview.add(tab2)
        self.tabview.add(tab3)
        self.tabview.add(tab4)
        
        self.tabview.configure(state="disabled")
        
        self.tabview.tab(tab1).grid_columnconfigure(0, weight=1)
        self.tabview.tab(tab1).grid_columnconfigure(1, weight=1)
        self.tabview.tab(tab1).grid_rowconfigure(1, weight=1)
        
        self.top_bar_container = customtkinter.CTkFrame(self.tabview.tab(tab1))
        self.top_bar_container.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.top_bar_container.grid_columnconfigure(1, weight=1)
        
        cl = customtkinter.CTkLabel(self.top_bar_container, text="Service URL:", anchor="w")
        cl.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="ew")
        
        self.service_url = customtkinter.CTkEntry(self.top_bar_container, textvariable=self.option_manager.get_arguments()['url'])
        self.service_url.grid(row=0, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.load_parameters = customtkinter.CTkButton(self.top_bar_container, text="Connect", command=self.load)
        self.load_parameters.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
                
        self.service_editor = customtkinter.CTkScrollableFrame(self.tabview.tab(tab1), label_text="Service Editor")
        self.service_editor.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.service_editor.grid_columnconfigure(0, weight=1)
        self.service_editor.grid_rowconfigure(0, weight=1)
        
        cl = customtkinter.CTkLabel(self.service_editor, text="Service Status:", anchor="w")
        cl.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.service_status = customtkinter.CTkTextbox(self.service_editor, height=32)
        self.service_status.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        cl = customtkinter.CTkLabel(self.service_editor, text="Service Name:", anchor="w")
        cl.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.service_name = customtkinter.CTkTextbox(self.service_editor, height=32)
        self.service_name.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        cl = customtkinter.CTkLabel(self.service_editor, text="Service Description:", anchor="w")
        cl.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.service_description = customtkinter.CTkTextbox(self.service_editor, height=32)
        self.service_description.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        cl = customtkinter.CTkLabel(self.service_editor, text="Service Details:", anchor="w")
        cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.service_details = customtkinter.CTkTextbox(self.service_editor, height=480)
        self.service_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.environment_editor = customtkinter.CTkScrollableFrame(self.tabview.tab(tab1), label_text="Environment Editor")
        self.environment_editor.grid(row=1, column=1, padx=(20, 20), pady=(5, 5), sticky="nsew")
        self.environment_editor.grid_columnconfigure(0, weight=1)
        self.environment_editor.grid_rowconfigure(0, weight=1)
        
        cl = customtkinter.CTkLabel(self.environment_editor, text="Cluster Preset:", anchor="w")
        cl.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.preset_selector = customtkinter.CTkOptionMenu(self.environment_editor, values=["Local", "AWS", "Azure", "Google Cloud"])
        self.preset_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        cl = customtkinter.CTkLabel(self.environment_editor, text="Controls:", anchor="w")
        cl.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.start_cluster_button = customtkinter.CTkButton(self.environment_editor, text="Start Cluster", command=self.start_cluster)
        self.start_cluster_button.grid(row=3, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
        
        self.create_environment_button = customtkinter.CTkButton(self.environment_editor, text="Deploy Environment")
        self.create_environment_button.grid(row=4, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
        
        self.get_status = customtkinter.CTkButton(self.environment_editor, text="Cluster Status:", command=self.cluster_status)
        self.get_status.grid(row=5, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
        
        self.destroy_environment_button = customtkinter.CTkButton(self.environment_editor, text="Stop Cluster", command=self.stop_cluster)
        self.destroy_environment_button.grid(row=6, column=0, padx=(20, 20), pady=(5,10), sticky="ew")
        
        cl = customtkinter.CTkLabel(self.environment_editor, text="Cluster Status", anchor="w")
        cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.custer_details = customtkinter.CTkTextbox(self.environment_editor, height=480)
        self.custer_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
        
        self.tabview.tab(tab2).grid_columnconfigure(0, weight=8)
        self.tabview.tab(tab2).grid_columnconfigure(1, weight=1)
        self.tabview.tab(tab2).grid_rowconfigure(0, weight=1)
        self.tabview.tab(tab2).grid_rowconfigure(1, weight=1)
        
        self.steps_frame = sv.StepView(self.tabview.tab(tab2), label_text="Group Editor", option_manager=self.option_manager)
        self.steps_frame.grid(row=0, rowspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.steps_frame.grid_columnconfigure(0, weight=1)
        self.steps_frame.grid_rowconfigure(0, weight=1)
        
        self.static_param_frame = spv.StaticParameterView(self.tabview.tab(tab2), label_text="Static Parameters", option_manager=self.option_manager)
        self.static_param_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.static_param_frame.grid_columnconfigure(0, weight=1)
        self.static_param_frame.grid_rowconfigure(0, weight=1)
        
        self.calib_param_frame = cpv.CalibrationParametersView(self.tabview.tab(tab2), label_text="Calibration Parameters", option_manager=self.option_manager)
        self.calib_param_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.calib_param_frame.grid_columnconfigure(0, weight=1)
        self.calib_param_frame.grid_rowconfigure(0, weight=1)
        
        # URL
        
        self.tabview.tab(tab3).grid_columnconfigure(0, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(0, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(1, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(2, weight=200)
        self.url = customtkinter.CTkEntry(self.tabview.tab(tab3), textvariable=self.option_manager.get_arguments()['url'])
        self.url.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.run_button = customtkinter.CTkButton(self.tabview.tab(tab3), text="Run", command=self.run)
        self.run_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        ctt(self.run_button, delay=0.5, message="Start calibration...")
        
        
        self.stop_button = customtkinter.CTkButton(self.tabview.tab(tab3), text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        ctt(self.stop_button, delay=0.5, message="Stop calibration...")
        
        self.progress_container = customtkinter.CTkFrame(self.tabview.tab(tab3))
        self.progress_container.grid_columnconfigure(0, weight=1)
        self.progress_container.grid_columnconfigure(1, weight=1)
        self.progress_container.grid_columnconfigure(2, weight=1)
        self.progress_container.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        #fig = px.scatter(x=self.data_x, y=self.data_y)
        #fig.write_image("./best_cost_stacked.png")
        #fig.write_image("./best_cost_by_round.png")
        #fig.write_image("./table.png")
        #fig.write_image("./calibrated_params_by_round.png")
        
        # Add progress bar to progress container
        self.progress_message_left = customtkinter.CTkLabel(self.progress_container, text="")
        self.progress_message_left.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
        
        self.progress_message_middle = customtkinter.CTkLabel(self.progress_container, text="Calibration not running...")
        self.progress_message_middle.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        
        self.progress_message_right = customtkinter.CTkLabel(self.progress_container, text="")
        self.progress_message_right.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="e")
        
        self.progress_bar = customtkinter.CTkProgressBar(self.progress_container)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.progress_bar.set(0)
        ctt(self.progress_bar, delay=0.5, message="Current calibration progress")
        
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab(tab3))
        self.textbox.grid(row=2, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "Welcome to the CSIP PSO Calibration Tool!\n\nUse the Calibration tab to define steps and calibration parameters. Use this tab to run and observe calibration progress. Once finished, use the Visualization tab to generate figures and graphs.")
        
        self.tabview.tab(tab4).grid_columnconfigure(1, weight=10)
        self.tabview.tab(tab4).grid_columnconfigure(0, weight=1)
        self.tabview.tab(tab4).grid_columnconfigure(2, weight=1)
        self.tabview.tab(tab4).grid_rowconfigure(1, weight=1)
        
        self.graph_selector_value = tk.StringVar()
        self.graph_selector_value.set("Best Cost Stacked")
        self.graph_selector = customtkinter.CTkOptionMenu(self.tabview.tab(tab4), values=["Best Cost Stacked", "Best Cost by Round", "Calibrated Parameters", "Table"], variable=self.graph_selector_value, command=self.update_graph)
        self.graph_selector.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Add a button to call open_graph_in_browser
        self.graph_button = customtkinter.CTkButton(self.tabview.tab(tab4), text="Open Graph in Browser", command=self.open_graph_in_browser)
        self.graph_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #CTkToolTip(self.graph_button, delay=0.5, message="Open graph in browser...")
        
        
        self.graph_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "up.png")), size=(700, 500))
        self.graph_label = customtkinter.CTkLabel(self.tabview.tab(tab4), text=None, image=self.graph_image)
        self.graph_label.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def callback_test(self, *args):
        print("callback_test called")

    def start_cluster(self):
        process = subprocess.Popen(["minikube", "start"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('unicode-escape') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('unicode-escape') + "\n\n")
            
    def cluster_status(self):
        process = subprocess.Popen(["minikube", "status"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('unicode-escape') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('unicode-escape') + "\n\n")
            
    def stop_cluster(self):
        process = subprocess.Popen(["minikube", "stop"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"An error occurred: {error}")
            self.custer_details.insert("0.0", error.decode('latin_1') + "\n\n")
        else:
            print(f"Output: {output}")
            self.custer_details.insert("0.0", output.decode('latin_1') + "\n\n")

    def run(self):
        metrics = self.option_manager.get_metrics()
        self.running_config = metrics
        
        self.progress_bar.configure(mode="indeterminnate")
        self.progress_bar.start()
        
        self.data_x = [0]
        self.data_y = [0]
        
        self.progress_message_middle.configure(text="Calibration starting...")
        
        self.textbox.insert("0.0", "Starting calibration...\n\n")
        self.textbox.insert("0.0", "Calibration Parameters:\n")
        self.textbox.insert("0.0", json.dumps(metrics, indent=4) + "\n\n")
        try:
            info = self.option_manager.get_project_data()
            folder = info['path'] + '/' + info['name']
            
            
            self.process = Process(target=PSORunner.run_process, args=(metrics, folder))
            self.process.daemon = True
            self.process.start()
            self.after(1000, self.watch_loop)
            self.string_cache = ""
            self.data_cache = ""
            
        except Exception as e:
            self.textbox.insert("0.0", "An exception occurred!\n Exception: " + str(e) + "\n\n")
            self.textbox.insert("0.0", "Stack trace:\n")
            self.textbox.insert("0.0", traceback.format_exc())
            self.textbox.insert("0.0", "\n\n")
            self.textbox.insert("0.0", "Calibration failed!")
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration failed! See error log below.")
            self.progress_message_right.configure(text="")
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(0)
            
    def update_graph(self, value):
        selected_graph = self.graph_selector_value.get()
        info = self.option_manager.get_project_data()
        folder = info['path'] + '/' + info['name']
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (selected_graph == "Best Cost Stacked"):
            self.selected_graph_name = "best_cost_stacked"
            image_path = folder + self.selected_graph_name + ".png"
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image = customtkinter.CTkImage(Image.open(image_path), size=(1280, 720))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Best Cost by Round"):
            self.selected_graph_name = "best_cost_by_round"
            image_path = folder + self.selected_graph_name + ".png"
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image = customtkinter.CTkImage(Image.open(image_path), size=(1280, 720))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Table"):
            self.selected_graph_name = "table"
            image_path = folder + self.selected_graph_name + ".png"
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image = customtkinter.CTkImage(Image.open(image_path), size=(1280, 720))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Calibrated Parameters"):
            self.selected_graph_name = "calibrated_params_by_round"
            image_path = folder + self.selected_graph_name + ".png"
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image = customtkinter.CTkImage(Image.open(image_path), size=(1280, 720))
            self.graph_label.configure(image=self.graph_image)
            
    def save_project(self):
        metrics = self.option_manager.get_metrics()
        filename = asksaveasfilename(filetypes=[("JSON", "*.json")], initialfile="config", defaultextension="json", title="Save Project")
        
        try:
        
            # Convert metrics to json and save to file with proper spacing
            with open(filename, "w") as f:
                f.write(json.dumps(metrics, indent=4))
                
            self.save_button.configure(text="Saved!")
            self.after(3000, lambda: self.save_button.configure(text="Save"))
        except Exception as e:
            self.save_button.configure(text="Error!")
            print(e)
            self.after(3000, lambda: self.save_button.configure(text="Save"))
    
    def new_window(self):
        # Shell out and run ./main.py
        subprocess.Popen(["python3", "../mgpsogui.py"])
    
    def load_project(self):
        
        filename = askopenfilename(filetypes=[("JSON", "*.json")], title="Open Project", multiple=False)
        print(filename)
        
        try:
        
            # Load config.json and convert to metrics
            with open(filename, "r") as f:
                metrics = json.loads(f.read())
            
            self.option_manager.set_path(filename)
            
            if "arguments" in metrics:
                metrics["arguments"]["calibration_parameters"] = metrics["calibration_parameters"]
            
            if "service_parameters" in metrics:
                self.option_manager.set_service_parameters(metrics["service_parameters"])
                self.tabview.configure(state="enabled")
            
            print(metrics)
            
            self.option_manager.clear()
            self.option_manager.add_arguments(metrics["arguments"])
            self.option_manager.add_steps(metrics["steps"])
            
            self.steps_frame.clear()
            self.steps_frame.render()

            self.static_param_frame.clear()
            self.static_param_frame.render()
            
            self.calib_param_frame.clear()
            self.calib_param_frame.render()
            
            self.load_button.configure(text="Loaded!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))
            
        except Exception as e:
            print(e)
            self.load_button.configure(text="Error!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))
        
        
    def load(self):
        # Make HTTP request to service_url and save the result to bounds.json
        self.load_parameters.configure(text="Loading...")
        self.after(10, self.make_request)
        self.after(3000, lambda: self.load_parameters.configure(text="Connect"))
            
    import json

    def make_request(self):
        service_url = self.service_url.get()
        response = requests.get(service_url)
            
        response_json = json.loads(response.text)
        status = response.status_code
        
        self.option_manager.set_service_parameters(response_json)
        self.tabview.configure(state="enabled")
        
        self.service_status.delete('0.0', tk.END)
        self.service_status.insert(text=str(status), index='0.0')
        self.service_name.delete('0.0', tk.END)
        self.service_name.insert(text=str(response_json["metainfo"]["name"]), index='0.0')
        self.service_description.delete('0.0', tk.END)
        self.service_description.insert(text=str(response_json["metainfo"]["description"]), index='0.0')
        self.service_details.delete('0.0', tk.END)
        self.service_details.insert(text=json.dumps(response_json, indent=4), index='0.0')
        
        
        self.load_parameters.configure(text="Loaded!")
            
    def watch_loop(self):
        # Check if file exists:
        
        info = self.option_manager.get_project_data()
        folder = info['path'] + '/' + info['name']
            
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (os.path.exists(folder + '/output.txt')):
            with open(folder + '/output.txt', 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                
                new_characters = lines_string.replace(self.string_cache, "")
                # Update the textbox with characters not in self.string_cache
                self.textbox.insert('0.0', new_characters)
                self.string_cache = lines_string
                print(new_characters, end="")
                
            try:
                with open(folder + "/output.txt", "r") as f:
                    text = f.read()

                calibrated_params_pattern = r"calibrated params: ({.*?})"
                best_particle_values_pattern = r"best particle values: (\[.*?\])"
                progress_pattern = r"Progress -  best_round_cost:(.*?), rel_round_tol:(.*?), rtol:(.*?)\n"

                calibrated_params = re.findall(calibrated_params_pattern, text)
                best_particle_values = re.findall(best_particle_values_pattern, text)
                progress_values = re.findall(progress_pattern, text)

                for index, pp in enumerate(best_particle_values):
                    pp = pp.strip()
                    pp = pp.replace('[ ', '[')
                    pp = pp.replace('  ', ',')
                    pp = pp.replace(' ', ',')
                    best_particle_values[index] = pp

                calibrated_params = [ast.literal_eval(i) for i in calibrated_params]
                best_particle_values = [ast.literal_eval(i) for i in best_particle_values]
                progress_values = [tuple(map(float, i)) for i in progress_values]
                
                print(calibrated_params)
                
                GraphGenerator.calibrated_params_by_round(self.running_config['steps'], calibrated_params, self.option_manager)
                self.update_graph("")
            except Exception as e:
                # Print stack trace
                traceback.print_exc()
                
                print(e)
                
        if (os.path.exists(folder + '/error.txt')):
            with open(folder + '/error.txt', 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                self.data_cache = lines_string
                
                pattern = r'(\d+)%\|.*\|(\d+)/(\d+)(?:,\sbest_cost=(\d+\.\d+))?' # The magic of AI
                matches = re.findall(pattern, self.data_cache)
                filtered_matches = [match for match in matches if match[3] != '']
                matches = filtered_matches

                if len(matches) > 0:
                    df = pd.DataFrame(matches, columns=['percent', 'completed_rounds', 'total_rounds', 'best_cost'], dtype=float)
                    df = df[df['best_cost'] != '']
                    df = df.dropna()
                    df = df.drop_duplicates()
                    df['round_step'] = (df['completed_rounds'].diff() < 0).cumsum()
                    df = df.drop_duplicates(subset=['completed_rounds', 'round_step'])

                    GraphGenerator.best_cost_stacked(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.best_cost_by_round(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.table(self.running_config['steps'], df, self.option_manager)
                    self.update_graph("")

                    match = matches[-1]
                    percent = int(match[0])
                    completed_rounds = int(match[1])
                    total_rounds = int(match[2])
                    best_cost = float(match[3]) if match[3] else None
                    
                    if (percent > 0):
                        self.progress_bar.stop()
                        self.progress_bar.configure(mode="determinate")
                        self.progress_bar.set(percent/100)
                        self.progress_message_left.configure(text="Percent Complete: " + str(percent) + "%")
                        self.progress_message_middle.configure(text=str(completed_rounds) + "/" + str(total_rounds))
                        self.progress_message_right.configure(text="Best Cost: " + str(best_cost))
                    else:
                        self.progress_bar.configure(mode="indeterminate")
                        self.progress_bar.start()
                        self.progress_message_left.configure(text="")
                        self.progress_message_middle.configure(text="Starting new round...")
                        self.progress_message_right.configure(text="")
                
                
                
        if self.process.is_alive():
            self.after(1000, self.watch_loop)
        else:
            self.textbox.insert("0.0", "\nCalibration finished!\n")
        
    def open_graph_in_browser(self):
        # Shell out to the terminal and run "open ./example.html"
        subprocess.run(["open", "./" + self.selected_graph_name + ".html"])
        
    def stop(self):
        
        info = self.option_manager.get_project_data()
        folder = info['path'] + '/' + info['name']
            
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Stop the process
        if (os.path.exists(folder + '/output.txt')):
            os.remove(folder + '/output.txt')
        
        if (os.path.exists(folder + '/error.txt')):
            os.remove(folder + '/error.txt')
            
        self.textbox.insert("0.0", "\nCalibration terminated!\n")
        self.process.terminate()
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.progress_message_left.configure(text="")
        self.progress_message_middle.configure(text="Calibration stopped!")
        self.progress_message_right.configure(text="")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

def start():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()