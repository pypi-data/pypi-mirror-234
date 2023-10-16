import pyautogui
import random
import sys

class Typeinator():
    def __init__(self):
        self.delay = 0.02
        self.buletPointFlag = False
        #check if windows
        self.comandKey = ''
        if sys.platform == 'win32':
            self.comandKey = 'ctrl'
        #check if mac
        elif sys.platform == 'darwin':
            self.comandKey = 'command'
        else:
            self.comandKey = 'ctrl'
    
    def type(self, text: str) -> None:
        """
            function to type text
            input: text to be typed
            output: None
        """
        #random 0.1 - 0.5 second delay between each letter
        #self.delay = random.uniform(0.01, 0.2)
        if '...' in text:
            text = text.replace('...', './DOTS/')
        sentances = text.split('.')
        for sentance in sentances:
            #add back punctuation
            if sentance != sentances[-1]:
                sentance += '.'
            if '/I/' in sentance:
                pyautogui.hotkey(self.comandKey, 'i')
                sentance = sentance.replace('/I/', '')
            if '/B/' in sentance:
                pyautogui.hotkey(self.comandKey, 'b')
                sentance = sentance.replace('/B/', '')
            if '/U/' in sentance:
                pyautogui.hotkey(self.comandKey, 'u')
                sentance = sentance.replace('/U/', '')
            if '/DOTS/' in sentance:
                sentance = sentance.replace('/DOTS/', '..')
            
            if '/+/' in sentance:
                split = sentance.split('/+/')
                pyautogui.typewrite(split[0] + '\n' , self.delay)
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                pyautogui.typewrite(split[1] + '', self.delay)
            elif '/-/' in sentance:
                split = sentance.split('/-/')
                pyautogui.typewrite(split[0], self.delay)
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                pyautogui.typewrite(split[1] + '', self.delay)
                
            else:
            #random chance to add a typo
                if random.randint(3,5) == 4:
                    #split into words and pick a random word
                    words = sentance.split(' ')
                    mispelled = random.randint(0, len(words) - 1)
                    original = words[mispelled]
                    if len(original) > 3:
                        #split the word into letters and pick a random letter
                        letter = random.randint(1, len(words[mispelled]) - 1)
                        #remove the letter from word in list
                        words[mispelled] = words[mispelled].replace(words[mispelled][letter], '')
                        #output list until mispelled word
                        for i in range(mispelled):
                            pyautogui.typewrite(words[i] + ' ', self.delay)
                        #type the mispelled word
                        pyautogui.typewrite(words[mispelled], self.delay)
                        
                        #use backspace to remove the mispelled word
                        for i in range(len(words[mispelled])):
                            pyautogui.press('backspace')
                        #type the word again
                        pyautogui.typewrite(original + ' ', self.delay)
                        #output the rest of the list
                        for i in range(mispelled + 1, len(words)):
                            pyautogui.typewrite(words[i] + ' ', self.delay)

                    else:
                        pyautogui.typewrite(sentance , self.delay)
                else:
                    #type the sentance
                    pyautogui.typewrite(sentance , self.delay)


if __name__ == '__main__':
    import time
    exampleParagraph = """This is an example paragraph using all the funtions above. /I/This is an italic sentance./I/ /B/This is a bold sentance./B/ /U/This is an underlined sentance./U/ and here are some more...
Testing for the mispelling function. bigwords, forthcoming bigsentences.
more conent... and more content...
beofre bullets/+/ first bullet
This is a bullet point.
another
another
/-/
after the bullets.
    """
    time.sleep(5)
    Typeinator().type(exampleParagraph)
