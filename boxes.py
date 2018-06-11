import libtcodpy as rl

import time

import math

import copy

import tkinter as tk

from tkinter import filedialog

from objnav import objNavigate

class Box: # The class for completely non-interactive boxes, superclass for interactive boxes.
    def __init__(self,x,y,w,h,title=None,text=""):
        # Box dimensions.
        if w <= 0: # If non-positive, base width on length of options.
            self.w = min(80,len(text)+4)
        else:
            self.w = w
        if h <= 0: # If non-positive, base height on optCap.
            self.h = rl.console_get_height_rect(0, 0, 0, self.w-4, 24, text) + 2
        else:
            self.h = h
        # Box coordinates.
        if x < 0: # If negative, center it.
            self.x = 40-int(math.ceil(self.w/2))
        else:
            self.x = x
        if y < 0: # If negative, center it.
            self.y = 12-int(math.ceil(self.h/2))
        else:
            self.y = y
        self.title = title # To show at the top of the box.
        self.text = text # To show in the box itself. It's up to the designer to ensure this does not exceed the bounds of the box. For story text boxes that may exceed the initial box, see NarrativeBox.
    
    def draw(self,color=rl.white):
        oldColor = rl.console_get_default_foreground(0) # Store old color.
        rl.console_set_default_foreground(0, color) # Apply window's color.
        # Draw the corners.
        rl.console_put_char_ex(0, self.x, self.y, rl.CHAR_DNW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y, rl.CHAR_DNE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x, self.y+self.h-1, rl.CHAR_DSW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y+self.h-1, rl.CHAR_DSE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        # Draw the walls.
        for i in range(self.y+1,self.y+self.h-1):
            rl.console_put_char_ex(0, self.x, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.x+self.w-1, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        for i in range(self.x+1,self.x+self.w-1):
            rl.console_put_char_ex(0, i, self.y, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, i, self.y+self.h-1, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        if self.title != None: # Draw the title, if present.
            rl.console_print(0,self.x+2,self.y," {0} ".format(self.title))
        rl.console_set_default_foreground(0, oldColor) # Revert color before drawing rest of window.
        rl.console_print_rect(0, self.x+2, self.y+1, self.w-4, self.h-2, self.text) # Draw the inner text.
    
    def forward(self): # If enter or the like is pressed and this is the active box.
        return "CLOSE" # Close the box.
    
    def backward(self): # If escape or the like is pressed and this is the active box.
        return "CLOSE" # Close the box.
    
    def miscInput(self, key): # Any other input is handled here.
        return
    
    def goUp(self): # If up or the like is pressed.
        return # Do nothing. This isn't a selection box.
    
    def goDown(self): # If down or the like is pressed.
        return # Do nothing. This isn't a selection box.
    
    def getWidth(self): # Retrieves the box's width.
        return self.w
    
    def getX(self): # Retrieves the box's x position.
        return self.x
    
    def setHeight(self,newH): # This is pretty much just here for the turn order box. Most boxes have no business changing size after creation.
        self.h = newH
    
    def handleClick(self, mouse): # Handle a left click.
        if mouse.cx >= self.x and mouse.cx < self.x + self.w and mouse.cy >= self.y and mouse.cy < self.y + self.h: # If the click is in bounds, call forward().
            return self.forward()

class SelectBox(Box): # This box allows selecting from a number of options.
    def __init__(self,x,y,w,h,title,options,optCap):
        self.options = options # To show in the box itself. It's up to the designer to ensure this does not exceed the bounds of the box. For story text boxes that may exceed the initial box, see NarrativeBox.
        if optCap <= 0: # If non-positive, base cap on number of options.
            self.optCap = min(len(options),22)
        else:
            self.optCap = optCap # The maximum number of options to show at once.
        # Box dimensions.
        if w <= 0: # If non-positive, base width on length of options.
            if title == None:
                self.w = 7
            else:
                self.w = len(title)+6
            for option in options:
                self.w = max(self.w,len(option)+6)
        else:
            self.w = w
        if h <= 0: # If non-positive, base height on optCap.
            self.h = self.optCap+2
        else:
            self.h = h
        # Box coordinates.
        if x < 0: # If negative, center it.
            self.x = 40-int(math.ceil(self.w/2))
        else:
            self.x = x
        if y < 0: # If negative, center it.
            self.y = 12-int(math.ceil(self.h/2))
        else:
            self.y = y
        self.title = title # To show at the top of the box.
        self.selectedOption = 0 # The number of the currently selected option.
        self.optOffset = 0 # Controls which option should be the top option. This is needed for one to scroll through more options than the box has room for.
    
    def draw(self,color=rl.white):
        oldColor = rl.console_get_default_foreground(0) # Store old color.
        rl.console_set_default_foreground(0, color) # Apply window's color.
        rl.console_rect(0, self.x, self.y, self.w, self.h, True) # Reset background color for the box.
        # Draw the corners.
        rl.console_put_char_ex(0, self.x, self.y, rl.CHAR_DNW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y, rl.CHAR_DNE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x, self.y+self.h-1, rl.CHAR_DSW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y+self.h-1, rl.CHAR_DSE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        # Draw the walls.
        for i in range(self.y+1,self.y+self.h-1):
            rl.console_put_char_ex(0, self.x, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.x+self.w-1, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        for i in range(self.x+1,self.x+self.w-1):
            rl.console_put_char_ex(0, i, self.y, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, i, self.y+self.h-1, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        if self.title != None: # Draw the title, if present.
            rl.console_print(0,self.x+2,self.y," {0} ".format(self.title))
        rl.console_set_default_foreground(0, oldColor) # Revert color before drawing rest of window.
        for i,option in enumerate(self.options[self.optOffset:min(self.optOffset+self.optCap,len(self.options))]): # Draw the options.
            rl.console_print(0, self.x+4, self.y+1+i, option)
        rl.console_print(0, self.x+2, self.y+1+self.selectedOption-self.optOffset, chr(rl.CHAR_ARROW2_E))
        # Draw scroll arrows as needed.
        if int(time.clock()*2) % 2 == 0:
            if self.optOffset > 0:
                rl.console_print(0, self.x+int(self.w/2), self.y, chr(rl.CHAR_ARROW2_N))
            if self.optOffset + self.optCap < len(self.options):
                rl.console_print(0, self.x+int(self.w/2), self.y+self.h-1, chr(rl.CHAR_ARROW2_S))
    
    def forward(self): # If enter or the like is pressed and this is the active box.
        return self.options[self.selectedOption] # Return the selected item.
    
    def backward(self): # If escape or the like is pressed and this is the active box.
        return "CLOSE" # Close the box.
    
    def goUp(self): # If up or the like is pressed.
        self.selectedOption = (self.selectedOption + len(self.options) - 1) % len(self.options) # Go up one option.
        if self.selectedOption < self.optOffset: # If the option selected is above the listed options, fix that.
            self.optOffset = self.selectedOption
        if self.selectedOption + 1 >= self.optOffset + self.optCap: # If the option selected is below the listed options, fix that.
            self.optOffset = self.selectedOption - self.optCap + 1
    
    def goDown(self): # If down or the like is pressed.
        self.selectedOption = (self.selectedOption + 1) % len(self.options) # Go down one option.
        if self.selectedOption < self.optOffset: # If the option selected is above the listed options, fix that.
            self.optOffset = self.selectedOption
        if self.selectedOption + 1 >= self.optOffset + self.optCap: # If the option selected is below the listed options, fix that.
            self.optOffset = self.selectedOption - self.optCap + 1
    
    def handleClick(self, mouse): # Handle a left click.
        if mouse.cx >= self.x + 1 and mouse.cx < self.x + self.w - 1 and mouse.cy >= self.y + 1 and mouse.cy < self.y + self.h - 1: # If the click is in bounds
            if mouse.cy - self.y - 1 + self.optOffset < len(self.options): # If the click is in a space that has an option in it.
                self.selectedOption = mouse.cy - self.y - 1 + self.optOffset # Select the clicked option
                return self.forward() # Then call forward()

class TargetBox(SelectBox): # This box allows selecting between conscious enemies.
    def __init__(self,x,y,members):
        options = [] # A temporary array for the visible options for the selection box.
        self.members = [] # An array of the enemy IDs (where they appear in the array) that correspond to the selections.
        for member in members:
            if not member.isDead():
                options.append(member.getName())
                self.members.append(member)
        super().__init__(x,y,-1,-1,None,options,-1)
    
    def forward(self): # If enter or the like is pressed and this is the active box.
        return self.members[self.selectedOption] # Return the selected item's ID, not the item itself.

class ModdingBox(Box): # This box allows modifying properties of an object represting the game mod being modified. Or rather, representing the section of the game mod being worked with. More detail on this may be found in devscenes.py
    def __init__(self,menuObj,baseMenuObj):
        self.optCap = min(len(menuObj[3]),19)
        self.w = 80
        self.h = self.optCap + 5
        self.x = 0
        self.y = 12 - math.ceil(self.h/2)
        self.dividerX = 5 # The dividing line between the options and their values.
        for option in menuObj[3]: # Determine where the dividing line should be.
            if option[0] == None: # If the first field of the sub-menu is used, go by its MAX length, not its current. 
                if option[3][0][4] + 5 > self.dividerX:
                    self.dividerX = option[3][0][4] + 5
            else:
                if len(option[0]) + 5 > self.dividerX:
                    self.dividerX = len(option[0]) + 5
        self.title = menuObj[0] # To show at the top of the box.
        self.selectedOption = 0 # The number of the currently selected option.
        self.optOffset = 0 # Controls which option should be the top option. This is needed for one to scroll through more options than the box has room for.
        self.menuObj = menuObj[3] # Store the menuObj for later.
        self.baseMenuObj = baseMenuObj # Store the BASE menu object.
        self.inputMode = "" # The input mode can text or number. Empty means "No, I'm not inputting anything right now."
        self.currentInput = "" # The current input value, if applicable.
        self.cursorPos = 0 # The position of the cursor.
        self.inputOffset = 0 # How much the drawing of the input is offset (max 76 characters can be shown at a time).
        self.subBox = None # The box to show choices in, when selecting the value for a multiple-choice field.
    
    def draw(self,color=rl.white):
        if self.subBox != None: # If there is a sub-box, draw that instead.
            self.subBox.draw()
            return
        rl.console_rect(0, self.x, self.y, self.w, self.h, True) # Reset background color for the box.
        # Draw the corners.
        rl.console_put_char_ex(0, self.x, self.y, rl.CHAR_DNW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y, rl.CHAR_DNE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x, self.y+self.h-1, rl.CHAR_DSW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        rl.console_put_char_ex(0, self.x+self.w-1, self.y+self.h-1, rl.CHAR_DSE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        # Draw the walls.
        for i in range(self.y+1,self.y+self.h-1):
            rl.console_put_char_ex(0, self.x, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.x+self.w-1, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        for i in range(self.y+1,self.y+self.h-4):
            rl.console_put_char_ex(0, self.dividerX, i, rl.CHAR_DVLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        for i in range(self.x+1,self.x+self.w-1):
            rl.console_put_char_ex(0, i, self.y, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, i, self.y+self.h-1, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, i, self.y+self.h-4, rl.CHAR_DHLINE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            # Draw the dividing joints between sections.
            rl.console_put_char_ex(0, self.dividerX, self.y, rl.CHAR_DTEES, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.dividerX, self.y+self.h-4, rl.CHAR_DTEEN, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.x, self.y+self.h-4, rl.CHAR_DTEEE, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
            rl.console_put_char_ex(0, self.x+self.w-1, self.y+self.h-4, rl.CHAR_DTEEW, rl.console_get_default_foreground(0), rl.console_get_default_background(0))
        if self.title != None: # Draw the title, if present.
            rl.console_print(0,self.x+2,self.y," {0} ".format(self.title))
        # Draw every option and its current value (or "..." if it leads to a new menu).
        for i,option in enumerate(self.menuObj[self.optOffset:min(self.optOffset+self.optCap,len(self.menuObj))]): # Draw the options.
            if option[0] == None:
                print(option)
                rl.console_print(0, self.x+4, self.y+1+i, option[3][0][3])
            else:
                rl.console_print(0, self.x+4, self.y+1+i, option[0])
            if isinstance(option[3], list):
                rl.console_print(0, self.dividerX+2, self.y+1+i, "...")
            else:
                rl.console_print(0, self.dividerX+2, self.y+1+i, str(option[3])[0:min(len(str(option[3])),76-self.dividerX)])
        # Draw the description of the current option or the current input, whichever is needed.
        color = "" # The color to draw the input in. Or more specifically, the ascii mid-string color change code. Since the default is white, by default nothing needs to be done here.
        if self.inputMode != "":
            if self.inputIsValid(self.currentInput,self.menuObj[self.selectedOption][1],self.menuObj[self.selectedOption][4]) == False: # If the input isn't valid, make the color red.
                color = chr(rl.COLCTRL_FORE_RGB)+chr(255)+chr(64)+chr(64)
            if self.inputMode == "Text":
                rl.console_print(0, 2, self.y+self.h-3, "Input the new value. Max length is {0}\n{2}{1}{3}".format(self.menuObj[self.selectedOption][4],self.currentInput[self.inputOffset:min(self.inputOffset+76,len(self.currentInput))],color,chr(rl.COLCTRL_STOP)))
            elif self.inputMode == "Number":
                rl.console_print(0, 2, self.y+self.h-3, "Input the new value. Max value is {0}\n{2}{1}{3}".format(self.menuObj[self.selectedOption][4],self.currentInput[self.inputOffset:min(self.inputOffset+76,len(self.currentInput))],color,chr(rl.COLCTRL_STOP)))
        else:
            rl.console_print_rect(0, 2, self.y+self.h-3, 76, 2, self.menuObj[self.selectedOption][2])
            rl.console_print(0, self.x+2, self.y+1+self.selectedOption-self.optOffset, chr(rl.CHAR_ARROW2_E))
        # Draw input cursor.
        if self.inputMode != "":
            rl.console_set_char_background(0, 2+self.cursorPos-self.inputOffset, self.y+self.h-2, rl.white)
            rl.console_set_char_foreground(0, 2+self.cursorPos-self.inputOffset, self.y+self.h-2, rl.black)
        # Draw scroll arrows as needed.
        if int(time.clock()*2) % 2 == 0:
            if self.optOffset > 0:
                rl.console_print(0, self.x+int(self.w/2), self.y, chr(rl.CHAR_ARROW2_N))
            if self.optOffset + self.optCap < len(self.menuObj):
                rl.console_print(0, self.x+int(self.w/2), self.y+self.h-1, chr(rl.CHAR_ARROW2_S))
            if self.inputOffset > 0:
                rl.console_print(0, self.x, self.y+self.h-2, chr(rl.CHAR_ARROW2_W))
            if self.inputOffset < len(self.currentInput) - 75:
                rl.console_print(0, self.x+self.w-1, self.y+self.h-2, chr(rl.CHAR_ARROW2_E))
    
    def forward(self): # If enter or the like is pressed and this is the active box.
        if self.subBox != None: # If there is a sub-box, interact with that instead.
            if self.inputMode == "Delete": # If it's a deletion confirmation box.
                if self.subBox.forward() == "Yes": # If yes, delete the entry and resize the box.
                    self.menuObj.pop(self.selectedOption)
                    # After removing the item, recalculate certain values this may affect.
                    self.optCap = min(len(self.menuObj),19)
                    self.h = self.optCap + 5
                    self.y = 12 - math.ceil(self.h/2)
                    self.dividerX = 5 # The dividing line between the options and their values.
                    for option in self.menuObj:
                        if option[0] == None:
                            if option[3][0][4] + 5 > self.dividerX:
                                self.dividerX = option[3][0][4] + 5
                        else:
                            if len(option[0]) + 5 > self.dividerX:
                                self.dividerX = len(option[0]) + 5
                    if self.selectedOption >= len(self.menuObj): # This should be impossible, but ust in case the cursor ends up out-of-bounds as a result, correct that.
                        self.selectedOption = len(self.menuObj) - 1
                self.inputMode = "" # Exit delete mode.
            else: # If it's a normal multiple-choice selection box.
                self.menuObj[self.selectedOption][3] = self.subBox.forward() # Store the selected option.
            self.subBox = None # Close the sub-box either way..
            return
        if self.inputMode != "": # If it's input, confirm and apply said input if it's valid, then exit input mode.
            if self.inputIsValid(self.currentInput,self.menuObj[self.selectedOption][1],self.menuObj[self.selectedOption][4]):
                self.inputMode = ""
                if self.menuObj[self.selectedOption][1] == "Number":
                    self.menuObj[self.selectedOption][3] = int(self.currentInput)
                else:
                    self.menuObj[self.selectedOption][3] = self.currentInput
                self.inputOffset = 0 # Reset the offset.
                self.currentInput = "" # Reset the input. These two are to prevent blinking arrows on the description/input section from occurring when they shouldn't.
        elif self.menuObj[self.selectedOption][1] == "Menu" or self.menuObj[self.selectedOption][1] == "DisposableMenu": # If it's a menu, return said menu.
            return self.menuObj[self.selectedOption]
        elif self.menuObj[self.selectedOption][1] == "Add": # If it's a request to add a submenu, add said submenu and return nothing.
            self.menuObj.insert(self.selectedOption,copy.deepcopy(self.menuObj[self.selectedOption][3]))
            # After adding the item, recalculate certain values this may affect.
            self.optCap = min(len(self.menuObj),19)
            self.h = self.optCap + 5
            self.y = 12 - math.ceil(self.h/2)
            self.dividerX = 5 # The dividing line between the options and their values.
            for option in self.menuObj:
                if option[0] == None:
                    if option[3][0][4] + 5 > self.dividerX:
                        self.dividerX = option[3][0][4] + 5
                else:
                    if len(option[0]) + 5 > self.dividerX:
                        self.dividerX = len(option[0]) + 5
            return ""
        # Toggle the boolean if it is one.
        elif self.menuObj[self.selectedOption][1] == "Boolean":
            if self.menuObj[self.selectedOption][3] == "Yes":
                self.menuObj[self.selectedOption][3] = "No"
            else:
                self.menuObj[self.selectedOption][3] = "Yes"
        # Open file selection dialogue if needed for an image. A seperate entry will be made for audio files later, once I have chosen a method of playing audio, as that will influence what file types will be accepted there.
        elif self.menuObj[self.selectedOption][1] == "Image":
            root = tk.Tk() # Initialize tkinter for this purpose.
            root.withdraw() # Without this, an empty box would be drawn before opening the file selection dialogue. Both annoying and unprofessional.
            filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Bitmap File","*.bmp"),))
            if filename.endswith(".bmp"):
                self.menuObj[self.selectedOption][3] = filename # I know this produces an absolute path, which is undesirable. I have plans to make this a relative path in a later update.
            # Sadly, I do not know of any way to return focus to the main window after this process is completed. Annoying, but hey, it's still more convenient then the user having to navigate a file select screen made by libtcod.
        # Open multiple choice selection if needed.
        elif self.menuObj[self.selectedOption][1] == "Select":
            self.subBox = SelectBox(-1,-1,-1,-1,self.menuObj[self.selectedOption][0],self.menuObj[self.selectedOption][4],-1)
        # Handle a LINKED (to another menu's disposable values) multiple choice selection if needed.
        elif self.menuObj[self.selectedOption][1] == "LinkedSelect":
            options = ["None"]
            for entry in objNavigate(self.baseMenuObj,("Characters",)):
                if entry[1] == "DisposableMenu":
                    options.append(entry[3][0][3])
            self.subBox = SelectBox(-1,-1,-1,-1,self.menuObj[self.selectedOption][0],options,-1)
        # Otherwise, just set the input mode to the option type, but only if it's a valid type.
        elif self.menuObj[self.selectedOption][1] in ("Text","Number"):
            self.inputMode = self.menuObj[self.selectedOption][1]
            print(self.inputMode)
            self.currentInput = str(self.menuObj[self.selectedOption][3])
            self.inputOffset = 0
            self.cursorPos = len(self.currentInput)
            self.cursorRulesEnforce()
        return "" # Return nothing.
    
    def backward(self): # If escape or the like is pressed and this is the active box.
        if self.subBox != None: # If there is a sub-box, interact with that instead.
            self.subBox = None # Close the sub-box.
            self.inputMode = "" # Revert the input mode.
            return
        if self.inputMode != "":
            self.inputMode = ""
            self.inputOffset = 0 # Reset the offset.
            self.currentInput = "" # Reset the input. These two are to prevent blinking arrows on the description/input section from occurring when they shouldn't.
        else:
            return "CLOSE" # Close the box.
    
    def goUp(self): # If up or the like is pressed.
        if self.subBox != None: # If there is a sub-box, interact with that instead.
            self.subBox.goUp()
            return
        if self.inputMode != "": # Don't do anything if entering input.
            return
        self.selectedOption = (self.selectedOption + len(self.menuObj) - 1) % len(self.menuObj) # Go up one option.
        if self.selectedOption < self.optOffset: # If the option selected is above the listed options, fix that.
            self.optOffset = self.selectedOption
        if self.selectedOption + 1 >= self.optOffset + self.optCap: # If the option selected is below the listed options, fix that.
            self.optOffset = self.selectedOption - self.optCap + 1
    
    def goDown(self): # If down or the like is pressed.
        if self.subBox != None: # If there is a sub-box, interact with that instead.
            self.subBox.goDown()
            return
        if self.inputMode != "": # Don't do anything if entering input.
            return
        self.selectedOption = (self.selectedOption + 1) % len(self.menuObj) # Go down one option.
        if self.selectedOption < self.optOffset: # If the option selected is above the listed options, fix that.
            self.optOffset = self.selectedOption
        if self.selectedOption + 1 >= self.optOffset + self.optCap: # If the option selected is below the listed options, fix that.
            self.optOffset = self.selectedOption - self.optCap + 1
    
    def inputIsValid(self,inputVal,inputType,inputLimit): # Check if the input given is valid for the given input type, with the given limitation.
        if inputType == "Text": # Check if text is short enough.
            if len(inputVal) <= inputLimit:
                return True
        elif inputType == "Number": # Check if number is short enough (and not negative).
            try:
                if int(inputVal) <= inputLimit and int(inputVal) >= 0:
                    return True
            except ValueError:
                return False
        return False
    
    def miscInput(self, key): # Any other keyboard input is handled here.
        if self.inputMode == "": # Don't do anything if not inputting a value, UNLESS it's to delete a disposable menu (meaning, a character entry or the like).
            if key.vk == rl.KEY_DELETE and self.menuObj[self.selectedOption][1] == "DisposableMenu":
                self.inputMode = "Delete"
                self.subBox = SelectBox(-1,-1,-1,-1,"Permanently delete this item?",("Yes","No"),-1)
            return
        if key.vk == rl.KEY_BACKSPACE and self.cursorPos > 0: # Handle backspace.
            self.currentInput = self.currentInput[:self.cursorPos-1] + self.currentInput[self.cursorPos:]
            self.cursorPos -= 1
        elif key.vk == rl.KEY_DELETE and self.cursorPos < len(self.currentInput): # Handle delete.
            self.currentInput = self.currentInput[:self.cursorPos] + self.currentInput[self.cursorPos+1:]
        elif key.vk == rl.KEY_LEFT: # Handle left/right arrow keys.
            self.cursorPos -= 1
        elif key.vk == rl.KEY_RIGHT:
            self.cursorPos += 1
        elif key.c >= 32 and key.c <= 126: # Handle typing characters.
            self.currentInput = self.currentInput[:self.cursorPos] + chr(key.c) + self.currentInput[self.cursorPos:]
            self.cursorPos += 1
        self.cursorRulesEnforce()
        return

    def cursorRulesEnforce(self): # Make sure the cursor position and offset make sense.
        if self.cursorPos < 0: # Don't let the cursor go out-of-bounds on the left.
            self.cursorPos = 0
        elif self.cursorPos > len(self.currentInput): # Don't let the cursor go out-of-bounds on the right.
            self.cursorPos = len(self.currentInput)
        if self.inputOffset < 0: # Don't let the input offset go out-of-bounds on the left.
            self.inputOffset = 0
        elif self.inputOffset > len(self.currentInput) - 75 and self.inputOffset > 0: # Don't let the input offset go out-of-bounds on the right.
            self.inputOffset = max(len(self.currentInput)-75,0)
        if self.cursorPos - self.inputOffset < 0: # If the cursor is too far left, scroll the input to catch up.
            self.inputOffset = self.cursorPos
        elif self.cursorPos - self.inputOffset > 75: # If the cursor is too far right, scroll the input to catch up.
            self.inputOffset = self.cursorPos - 75
    
    def handleClick(self, mouse): # Handle a left click.
        if self.subBox != None: # Handle sub-box input.
            if self.subBox.handleClick(mouse) != None:
                self.forward()
                return
        if mouse.cx >= self.x + 1 and mouse.cx < self.x + self.w - 1 and mouse.cy >= self.y + 1 and mouse.cy < self.y + self.h - 1: # If the click is in bounds
            if mouse.cy - self.y - 1 + self.optOffset < len(self.menuObj): # If the click is in a space that has an option in it.
                self.selectedOption = mouse.cy - self.y - 1 + self.optOffset # Select the clicked option
                return self.forward() # Then call forward()