import csip
import cosu
import sys
import multiprocessing
import threading
import time
import os

from cosu.pso import global_best

def run_process(data, queue):
    steps = data['steps']
    args = data['arguments']
    calib = data['calibration_parameters']
    
    calibration_map = {}
    for param in calib:
        param_name = param['name']
        param_value = param['value']
        calibration_map[param_name] = param_value

    if (os.path.exists('output.txt')):
        os.remove('output.txt')
        
    if (os.path.exists('error.txt')):
        os.remove('error.txt')

    sys.stdout = open('output.txt', 'w')
    sys.stderr = open('error.txt', 'w')
    
    options = {}
    oh_strategy = {}
    
    for key in calibration_map.keys():
        if "options_" in key:
            options[key.replace("options_", "")] = float(calibration_map[key])
        if "strategy_" in key:
            oh_strategy[key.replace("strategy_", "")] = calibration_map[key]

    print("\n")
    print(calibration_map)
    print("\n")
    print(options)
    print("\n")
    print(oh_strategy)
    print("\n")

    optimizer, trace  = global_best(steps,                 # step definition
            rounds=(int(calibration_map['min_rounds']), int(calibration_map['max_rounds'])),                              # min/max number of rounds
            args=args,                                  # static arguments    
            n_particles=int(calibration_map['n_particles']),                             # number of particle candidates for each param
            iters=int(calibration_map['iters']),                                   # max # of iterations
            n_threads=int(calibration_map['n_threads']),                               # number of threads to use
            # ftol=0.00000001,                          # min cost function delta for convergence
            options=options,       # hyperparameter
            oh_strategy=oh_strategy,   # adaptive hyperparameter adjustments based on current and max # of iterations 
            conf={
                'service_timeout': int(calibration_map['service_timeout']),
                'http_retry': int(calibration_map['http_retry']),
                'http_allow_redirects': True if calibration_map['allow_redirects'] == "True" else False,
                'async_call': True if calibration_map['async_call'] == "True" else False,
                'http_conn_timeout': int(calibration_map['conn_timeout']),
                'http_read_timeout': int(calibration_map['read_timeout']),
                'particles_fail': int(calibration_map['particles_fail'])
                },
            result_queue=queue
        )  
    