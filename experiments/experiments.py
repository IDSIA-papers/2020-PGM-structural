import config
import os
import socket
import subprocess
import pandas as pd
import io
from contextlib import redirect_stdout
import itertools
import warnings
from datetime import datetime
import time
import timeout_decorator
import numpy as np
import matplotlib.pyplot as plt




def print_project():
    print(config.prj_path)



def strdate(): return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')



@timeout_decorator.timeout(7*1*60)
def run_java(jarfile, javafile):
    cmd=f"java -cp {jarfile} {javafile}"
    if config.disable_java: cmd= "echo 0,0,0,0,0,0"
    print(cmd)
    result = subprocess.run(cmd, universal_newlines = True, shell=True,stdout = subprocess.PIPE)
    print(result.stdout)
    return result

# ChainNonMarkovian 6 5 1 -1 0 CCALP 1234
def run_chain(model, N, endovarsize, exovarsize, target, obsvar, dovar, method, seed):

    print(strdate())
    exovarsize = exovarsize or endovarsize*endovarsize + 1

    if obsvar is None: obsvar = -1;
    elif obsvar<0: obsvar = N + obsvar;

    if dovar is None: dovar = -1;
    elif dovar<0: dovar = N + dovar;

    if target is None: target = N//2;
    elif target<0: target = N + target;

    warmups = 0
    repetitions = 1
    eps = 0.0001
    #ChainNonMarkovian 4  -v 5 -V 9 -t 1 -o -1 -d 0 -m  CCALP --seed 12234 --warmpus 0 --repetitions 1
    javafile = f"{config.exp_folder}/RunExperiments.java {model} {N} -v {endovarsize} -V {exovarsize} -t {target} -o {obsvar} -d {dovar} -m {method} -e {eps} -s {seed} -w {warmups} -r {repetitions} "
    try:
        result = run_java(config.jarfile, javafile)
        output = [float(x) for x in result.stdout.splitlines()[-1].split(",")]
    except:
        output = [float("inf"),float("inf")]+[float("nan")]* (endovarsize*2)

    return output



def run_tree(N=4, endovarsize=2,exovarsize=None, target=None, obsvar=-1, dovar=0, method="CVE", seed=1234):
    return run_chain("ChainNonMarkovian", N, endovarsize, exovarsize, target, obsvar, dovar, method, seed)

def run_polytree(N=4, endovarsize=2,exovarsize=None, target=None, obsvar=-1, dovar=0, method="CVE", seed=1234):
    return run_chain("RHMM-NonMarkovian", N, endovarsize, exovarsize, target, obsvar, dovar, method, seed)

def run_multiplyconnected(N=4, endovarsize=2,exovarsize=None, target=None, obsvar=-1, dovar=0, method="CVE", seed=1234):
    return run_chain("Squares-NonMarkovian", N, endovarsize, exovarsize, target, obsvar, dovar, method, seed)



def run_experiments(f, args, outkeys, fargs=None, verbose=False, lenght_dep_vars = None, non_evaluable=[]):


    print("=========")
    print(args)
    print("=========")

    result = pd.DataFrame(columns=list(args.keys())+list(outkeys))
    log_file = f"{config.log_folder}{strdate()}_{f.__name__}.txt"

    data = pd.DataFrame(list(itertools.product(*list(args.values()))), columns = args.keys())

    fargs = fargs or {}
    for k,v in fargs.items():
        data[k]=data.apply(v, axis=1)


    non_evaluable = non_evaluable or []

    lenght_dep_vars = lenght_dep_vars or ["N"]

    def is_evaluable(args):
        current = {k:v for (k,v) in args.items() if k not in lenght_dep_vars}
        previous = [{k:v for (k,v) in a.items() if k not in lenght_dep_vars} for a in non_evaluable]

        print(f"current: {current}")
        print(f"previous: {previous}")


        return not current in previous

    def single_experiment(argsv):
        if is_evaluable(argsv):
            outvals = f(**argsv)
            if np.isnan(outvals).any():
                non_evaluable.append(argsv)
                print(f"setting as not evaluable: {argsv}")
        else:
            outvals=[float("nan")]*len(outkeys)
        return outvals


    for argsv in data.to_dict(orient="row"):

        strio = io.StringIO()
        print(strdate())
        with open(log_file, 'a+') as logger:
            if verbose == False:
                with redirect_stdout(strio):
                    print(strdate())
                    outvals = single_experiment(argsv)
            else:
                outvals = single_experiment(argsv)

            logger.write(strio.getvalue())


        result = result.append({**argsv, **dict(zip(list(outkeys), outvals))}, ignore_index=True)
        print(dict(result.iloc[-1]))
        print("\n\n")

    return result

def get_args(**kwargs): return kwargs