import pyautogui
import random
import string
import sys
import time
class Typeinator():
    def __init__(self):
        self.delay = 0.02
        self.punctuationPause = .75
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
    def timeToType(self, text: str, timeIn:int) -> None:
        timeIn = timeIn * 60
        """
            function to type text given the minutes to type the str
            input: text to be typed, and minutes to type
            output: None
        """
        #deterine the amount of punctuation pauses
        punctuationPauses = 0
        for char in text:
            if char in ['.', '!', '?', ';']:
                if char == '.':
                    punctuationPauses += 1
                punctuationPauses += 1
        #determine the amount of characters to type
        characters = len(text)
        charTime = ((timeIn * 2) / 3)/characters
        #determine the amount of punctuation pauses
        punctuationPauseTime = (timeIn / 3) / punctuationPauses
        #set the values and call type, a he
        self.delay = charTime
        self.punctuationPause = punctuationPauseTime
        self.type(text)

    
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
            #will bold whole sentace
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
            if '/T/' in sentance:
                sentance = sentance.replace('/T/', '\t')
            
            if '/+/' in sentance:
                split = sentance.split('/+/')
                self.writer(split[0] + '\n' )
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                self.writer(split[1] + '')
            elif '/-/' in sentance:
                split = sentance.split('/-/')
                self.writer(split[0])
                pyautogui.hotkey(self.comandKey, 'shift', '8')
                self.writer(split[1] + '')
                
            else:
                
                if random.random() < 0.02:  # 2% chance of a typo
                    #chose a random word in the sentance
                    words = sentance.split(' ')
                    #randomly choose an index from words list
                    index = random.randint(0, len(words) - 1)
                    #type sentance up to the word
                    self.writer(' '.join(words[:index]))
                    #type the word with a typo
                    word = words[index]
                    typo_part = word + random.choice(string.ascii_lowercase)
                    self.writer(typo_part)

                    # 30% chance to recognize and fix the typo
                    if random.random() < 0.30:
                        time.sleep(self.punctuationPause)
                        # Delete the incorrect word
                        for _ in range(len(typo_part)):
                            pyautogui.press('backspace')
                            time.sleep(self.delay)
                        # Retype the word correctly
                        self.writer(word)
                        #type the rest of the sentance
                        self.writer(' '.join(words[index + 1:]))
                    else:
                        #type the rest of the sentance
                        self.writer(' '.join(words[index + 1:]))
                        time.sleep(self.punctuationPause)
                else:
                    self.writer(sentance)
      
    def writer(self, text:str):
        punctuation = {
            'comma': False,
            'simicolon': False,
            'explination': False,
            'question': False,
        }

        # 60% chance to pause for 2.5 seconds after a comma
        if ',' in text and random.random() < 0.60:
            punctuation['comma'] = True
        # 60% chance to pause for 2.5 seconds after a semicolon
        if ';' in text and random.random() < 0.60:
            punctuation['simicolon'] = True
        # Pause for 2.5 seconds after every period, exclamation mark, or question mark
        if '!' in text:
            punctuation['explination'] = True
        if '?' in text:
            punctuation['question'] = True
        
        #type the sentance and pause for any punctuation that is true
        if punctuation['comma'] or punctuation['simicolon'] or punctuation['explination'] or punctuation['question']:
            split = text
            #split sentance on commas if punctuation['comma'] is true, and replace the commas
            if punctuation['comma']:
                split = text.split(',')
                for i in range(len(split) - 1):
                    split[i] += ','
            if punctuation['simicolon']:
                split = text.split(';')
                for i in range(len(split) - 1):
                    split[i] += ';'
            if punctuation['explination']:
                split = text.split('!')
                for i in range(len(split) - 1):
                    split[i] += '!'
            if punctuation['question']:
                split = text.split('?')
                for i in range(len(split) - 1):
                    split[i] += '?'
            for i in range(len(split)):
                pyautogui.typewrite(split[i], interval=self.delay)
                if i != len(split) - 1:
                    time.sleep(self.punctuationPause)
        else:
            #check there is more than one word
            if ' ' in text:
                #pick random work to pause for 
                words = text.split(' ')
                index = random.randint(0, len(words) - 1)
                pyautogui.typewrite(' '.join(words[:index]), interval=self.delay)
                pyautogui.typewrite(' '+words[index]+' ', interval=self.delay)
                #pause
                time.sleep(self.punctuationPause)
                pyautogui.typewrite(' '.join(words[index + 1:]), interval=self.delay)
            else:
                pyautogui.typewrite(text, interval=self.delay)
                time.sleep(self.punctuationPause)
        time.sleep(self.punctuationPause)

if __name__ == '__main__':

    exampleParagraph = """This is an example paragraph using all the funtions above. /I/This is an italic sentance./I/ /B/This is a bold sentance./B/ /U/This is an underlined sentance./U/ and here are some more...
Testing for the mispelling function. bigwords, forthcoming bigs..
beofre bullets
 first bullet
 Thentences.%
more conent... and more content...
beofre bullets/+/ first bullet
This is a bullet point.
another
another
/-/
/T/after the bullets.


Lorem ipsum doldictum lorem. Pellentesque congue tincidunt ipsum vel rhoncus. Vivamus vestibulum, augue non pharetra tristique, nisi nibh scelerisque augue, vel bibendum mi lacus suscipit magna. Vivamus id erat augue. Morbi eu velit sed neque consequat auctor vitae et ex. Donec sollicitudin congue felis, id mattis arcu vulputate ut. Vestibulum eleifend vel eros vel interdum. Morbi lacus ante, condimentum eget justo sed, malesuada bibendum felis. Donec vitae varius enim, pellentesque vehicula dolor. Suspendisse bibendum dictum neque, ac sagittis orci posuere eu. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
"""
    time.sleep(5)
    Typeinator().timeToType(exampleParagraph, 1)
