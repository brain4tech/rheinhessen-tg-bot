# functions to add working dir to sys.path and remove it afterwards

import os, sys

def enable():
    # print ("Adding workingdir to sys.path")
    dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(dir)
    os.chdir(parent_dir)
    sys.path.append(parent_dir)

def disable():
    # print ("Removing workingdir from sys.path")
    dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(dir)
    sys.path.remove(parent_dir)
