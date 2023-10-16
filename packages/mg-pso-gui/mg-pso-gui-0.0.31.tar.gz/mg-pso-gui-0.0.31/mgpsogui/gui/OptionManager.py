from tkinter import StringVar as sv
from tkinter import IntVar as iv
from tkinter import BooleanVar as bv
from tkinter import DoubleVar as dv
import json

class OptionManager():
    
    def __init__(self):
        
        self.project_data = {"name": sv()}
        self.arguments = {"param": [],
                 "url": sv(),
                 "files": {},
                 "calibration_parameters": []}
        self.steps = []
        self.service_parameters = {}
            
    def clear(self):
        self.arguments['param'].clear()
        self.arguments['url'].set("")
        self.arguments['files'] = {}
        self.arguments['calibration_parameters'].clear()
        self.steps = []
        self.service_parameters = {}
    
    def add_arguments(self, arguments):
        
        if ("url" in arguments):
            self.arguments["url"].set(arguments["url"])
            
        if ("files" in arguments):
            for file in arguments["files"]:
                name = file["name"]
                value = file["value"]
                obj = {"name": sv(), "value": sv()}
                obj["name"].set(name)
                obj["value"].set(value)
                self.arguments["files"][name] = obj
        
        for param in arguments["param"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self.arguments["param"].append(obj)
            
        for param in arguments["calibration_parameters"]:
            name = param["name"]
            value = param["value"]
            obj = {"name": sv(), "value": sv()}
            obj["name"].set(name)
            obj["value"].set(value)
            self.arguments["calibration_parameters"].append(obj)
            
    def add_steps(self, steps):
        for step in steps:
            obj = {"param": [], "objfunc": [], "name": sv(), "message": sv(), "open": False}
            obj["name"].set("Step " + str(len(self.steps) + 1))
            obj["message"].set("Wow")
            
            for param in step["param"]:
                param_obj = {
                    "name": sv(), 
                    "bounds": (sv(), sv()), 
                    "default_value": sv(), 
                    "type": sv(),
                    "calibration_strategy": sv()
                }
                param_obj["name"].set(param["name"])
                if "bounds" in param:
                    param_obj["bounds"][0].set(param["bounds"][0])
                    param_obj["bounds"][1].set(param["bounds"][1]) 
                else: 
                    param_obj["bounds"][0].set(0)
                    param_obj["bounds"][1].set(1)
                if "type" in param:
                    param_obj["type"].set(param["type"])
                else:
                    param_obj["type"].set("float")
                if "default_value" in param:
                    param_obj["default_value"].set(param["default_value"])
                else:
                    param_obj["default_value"].set(1)
                if "calibration_strategy" in param:
                    param_obj["calibration_strategy"].set(param["calibration_strategy"])
                else:
                    param_obj["calibration_strategy"].set("none")
                obj["param"].append(param_obj)
            
            for objfunc in step["objfunc"]:
                objfunc_obj = {"name": sv(), "of": sv(), "weight": sv(), "data": (sv(), sv())}
                objfunc_obj["name"].set(objfunc["name"])
                objfunc_obj["of"].set(objfunc["of"])
                
                if ("weight" in objfunc): 
                    objfunc_obj["weight"].set(objfunc["weight"])
                else:
                    objfunc_obj["weight"].set(1)
                    
                objfunc_obj["data"][0].set(objfunc["data"][0])
                objfunc_obj["data"][1].set(objfunc["data"][1]) 
                obj["objfunc"].append(objfunc_obj)
            
            self.steps.append(obj)
    
    def add_function(self, step_index):
        obj = {"name": sv(), "of": sv(), "weight": sv(), "data": (sv(), sv())}
        obj["name"].set("ns")
        obj["of"].set("ns")
        obj["weight"].set(1)
        obj["data"][0].set("")
        obj["data"][1].set("")
        self.steps[step_index]["objfunc"].append(obj)
        
    def remove_function(self, step_index, index):
        self.steps[step_index]["objfunc"].pop(index)
    
    def add_bound(self, step_index, 
                  name="name", 
                  min=0, 
                  max=1,
                  type="float",
                  default_value=1,
                  calibration_strategy="none"):
        obj = {
            "name": sv(), 
            "bounds": (sv(), sv()), 
            "default_value": sv(), 
            "type": sv(),
            "calibration_strategy": sv()
        }
        obj["name"].set(name)
        obj["type"].set(type)
        obj["default_value"].set(default_value)
        obj["calibration_strategy"].set(calibration_strategy)
        obj["bounds"][0].set(min)
        obj["bounds"][1].set(max)
        self.steps[step_index]["param"].append(obj)
        
    def remove_bound(self, step_index, index):
        self.steps[step_index]["param"].pop(index)
        
    def add_argument(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["param"].append(obj)
        
    def add_calibration_param(self, key, value):
        obj = {"name": sv(), "value": sv()}
        obj["name"].set(key)
        obj["value"].set(value)
        self.arguments["calibration_parameters"].append(obj)
    
    def move_argument_up(self, index):
        if index > 0:
            self.arguments["param"][index], self.arguments["param"][index - 1] = self.arguments["param"][index - 1], self.arguments["param"][index]
            
    def move_argument_down(self, index):
        if index < len(self.arguments["param"]) - 1:
            self.arguments["param"][index], self.arguments["param"][index + 1] = self.arguments["param"][index + 1], self.arguments["param"][index]
            
    def move_step_up(self, index):
        if index > 0:
            self.steps[index], self.steps[index - 1] = self.steps[index - 1], self.steps[index]
            
    def move_step_down(self, index):
        if index < len(self.steps) - 1:
            self.steps[index], self.steps[index + 1] = self.steps[index + 1], self.steps[index]
            
    def toggle_step_open(self, index):
        self.steps[index]["open"] = not self.steps[index]["open"]
            
    def remove_argument(self, index):
        self.arguments["param"].pop(index)
        
    def remove_calibration_parameter(self, index):
        self.arguments["calibration_parameters"].pop(index)
        
    def remove_step(self, index):
        self.steps.pop(index)
            
    def get_arguments(self):
        return self.arguments
    
    def get_steps(self):
        return self.steps
            
            
    def get_all_as_json(self):
        obj = {"arguments": self.arguments, "steps": self.steps}
        return obj
    
    def set_service_parameters(self, service_parameters):
        self.service_parameters = service_parameters
    
    def get_service_parameters(self):
        return self.service_parameters

    def get_metrics(self):
        result = {}
        result['arguments'] = {}
        result['calibration_parameters'] = []
        result['service_parameters'] = {}
        for key, value in self.arguments.items():
            if key == 'url':
                result['arguments'][key] = value.get()
            elif key == 'files':
                result['arguments'][key] = {}
                #for name, obj in value.items():
                #    result['arguments'][key].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == 'param':
                result['arguments'][key] = []
                for obj in value:
                    result['arguments'][key].append({'name': obj['name'].get(), 'value': obj['value'].get()})
            elif key == "calibration_parameters":
                #result['calibration_parameters'][key] = []
                for obj in value:
                    result['calibration_parameters'].append({'name': obj['name'].get(), 'value': obj['value'].get()})
        result['steps'] = []
        for step in self.steps:
            step_result = {}
            #step_result['name'] = step['name'].get()
            #step_result['open'] = step['open']
            step_result['param'] = []
            for param in step['param']:
                # try converting the bounds to numbers
                #try:
                if param['type'].get() == 'float':
                    step_result['param'].append(
                        {
                            'name': param['name'].get(), 
                            'bounds': (float(param['bounds'][0].get()), 
                                       float(param['bounds'][1].get())),
                            'default_value': float(param['default_value'].get()),
                            'type': 'float',
                            'calibration_strategy': param['calibration_strategy'].get()
                        }
                    )
                elif param['type'].get() == 'list':
                    step_result['param'].append(
                        {
                            'name': param['name'].get(), 
                            'bounds': (float(param['bounds'][0].get()), 
                                       float(param['bounds'][1].get())),
                            'default_value': param['default_value'].get(),
                            'type': 'list',
                            'calibration_strategy': param['calibration_strategy'].get()
                        }
                    )
                #except ValueError:
                #    step_result['param'].append(
                #        {
                #            'name': param['name'].get(), 
                #            'bounds': (param['bounds'][0].get(), 
                #                       param['bounds'][1].get())
                #        }
                #    )
            step_result['objfunc'] = []
            for objfunc in step['objfunc']:
                step_result['objfunc'].append({'name': objfunc['name'].get(), 'of': objfunc['of'].get(), 'weight': float(objfunc['weight'].get()), 'data': (objfunc['data'][0].get(), objfunc['data'][1].get())})
            result['steps'].append(step_result)
        return result
