from unblockedGPT.typeresponse import Typeinator
import time
breaks = True

while breaks:
    text = input("Enter text: ")
    timeInput = int(input("Enter time(minutes): "))
    typer = Typeinator()
    print("Typing in 5 seconds...")
    time.sleep(5)
    typer.timeToType(text, timeInput)
    breaksInput = input("Type again? (y/n): ").lower()
    if breaksInput == 'n':
        breaks = False
    