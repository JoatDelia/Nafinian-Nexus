import libtcodpy as rl

import time

import math

class Box: # The class for completely non-interactive boxes, superclass for interactive boxes.
    def __init__(self,x,y,w,h,title=None,text=""):
        # Box dimensions.
        if w <= 0: # If non-positive, base width on length of options.
            self.w = min(80,len(text)+4)
        else:
            self.w = w
        if h <= 0: # If non-positive, base height on optCap.
            self.h = rl.console_get_height_rect(0, 0, 0, self.w, 24, text)
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
    
    def goUp(self): # If up or the like is pressed.
        return # Do nothing. This isn't a selection box.
    
    def goDown(self): # If down or the like is pressed.
        return # Do nothing. This isn't a selection box.
    
    def setHeight(self,newH): # This is pretty much just here for the turn order box. Most boxes have no business changing size after creation.
        self.h = newH

class SelectBox(Box): # This box allows selecting from a number of options.
    def __init__(self,x,y,w,h,title,options,optCap):
        self.options = options # To show in the box itself. It's up to the designer to ensure this does not exceed the bounds of the box. For story text boxes that may exceed the initial box, see NarrativeBox.
        if optCap <= 0: # If non-positive, base cap on number of options.
            self.optCap = min(len(options),22)
        else:
            self.optCap = optCap # The maximum number of options to show at once.
        # Box dimensions.
        if w <= 0: # If non-positive, base width on length of options.
            self.w = len(options[0])+6
            for option in options[1:]:
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