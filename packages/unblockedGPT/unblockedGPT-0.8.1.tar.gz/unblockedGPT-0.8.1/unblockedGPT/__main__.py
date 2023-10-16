import os
from unblockedGPT.typeresponse import Typeinator
from unblockedGPT.auth import Database
import openai
import time
import sys
def run():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app_path = os.path.join(dir_path, 'app.py')
    os.system(f'streamlit run {app_path}')
    
def textToType(args = sys.argv):
    if "-h" in args or "--help" in args:
        print("Usage: typetext -p [path to text file] (optional) -t [time in minutes] (optional) -s [speed][paues] (inprogress)")
        return
    if "-p" in args:
        path = args[args.index("-p") + 1]
        if os.path.exists(path):
            with open(path, 'r') as file:
                text = file.read()
        else:
            print("File not found")
            return
    else:
        print("No file path provided. Use -h for help")
        return
    if "-t" in args:
        timeInput = int(args[args.index("-t") + 1])
    else:
        timeInput = -1
    typer = Typeinator()
    print("Typing in 5 seconds...")
    time.sleep(5)
    if timeInput == -1:
        typer.type(text)
    else:
        typer.timeToType(text, timeInput)
    return
    
if __name__ == '__main__':
    type()