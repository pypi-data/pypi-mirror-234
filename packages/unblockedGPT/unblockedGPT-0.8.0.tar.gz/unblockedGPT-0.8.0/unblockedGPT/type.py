import time
from unblockedGPT.typeresponse import Typeinator

def type():
    while True:
        print("Enter the text you want to type (end with a line saying 'END'):")
        text = ""
        end_flag = False
        while not end_flag:
            line = input("")
            if line == "END":
                end_flag = True
            else:
                text += line + "\n"
        print("Starting in 5 seconds...")
        time.sleep(5)
        typeinator = Typeinator()

        typeinator.type(text)



if __name__ == '__main__':
    type()    