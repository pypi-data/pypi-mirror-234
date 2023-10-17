
import os,json

import pandas as pd
import pathlib,shutil

def rm_cache():
    for i in pathlib.Path(".").rglob("__pycache__"):
        print(i)
        shutil.rmtree(i)

if __name__ == "__main__" :
    rm_cache()