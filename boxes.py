import libtcodpy as rl

class Box: # The class for completely non-interactive boxes, superclass for interactive boxes.
    def __init__(self,x,y,w,h,title=None,text=""):
        # Box coordinates.
        self.x = x
        self.y = y
        # Box dimensions.
        self.w = w
        self.h = h
        self.title = title # To show at the top of the box.
        self.text = text # To show in the box itself. It's up to the designer to ensure this does not exceed the bounds of the box. For story text boxes that may exceed the initial box, see NarrativeBox.
    
    def draw(self,color=rl.white):
        oldColor = rl.console_get_default_foreground(0) # Store old color.
        rl.console_set_default_foreground(0, color) # Apply window's color.
        # Draw the corners.
        rl.console_set_char(0, self.x, self.y, rl.CHAR_DNW)
        rl.console_set_char(0, self.x+self.w-1, self.y, rl.CHAR_DNE)
        rl.console_set_char(0, self.x, self.y+self.h-1, rl.CHAR_DSW)
        rl.console_set_char(0, self.x+self.w-1, self.y+self.h-1, rl.CHAR_DSE)
        # Draw the walls.
        for i in range(self.y+1,self.y+self.h-1):
            rl.console_set_char(0, self.x, i, rl.CHAR_DVLINE)
            rl.console_set_char(0, self.x+self.w-1, i, rl.CHAR_DVLINE)
        for i in range(self.x+1,self.x+self.w-1):
            rl.console_set_char(0, i, self.y, rl.CHAR_DHLINE)
            rl.console_set_char(0, i, self.y+self.h-1, rl.CHAR_DHLINE)
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

class SelectBox(Box): # This box allows selecting from a number of options.
    def __init__(self,x,y,w,h,title,options):
        # Box coordinates.
        self.x = x
        self.y = y
        # Box dimensions.
        self.w = w
        self.h = h
        self.title = title # To show at the top of the box.
        self.options = options # To show in the box itself. It's up to the designer to ensure this does not exceed the bounds of the box. For story text boxes that may exceed the initial box, see NarrativeBox.
        self.selectedOption = 0 # The number of the currently selected option.
    
    def draw(self,color=rl.white):
        oldColor = rl.console_get_default_foreground(0) # Store old color.
        rl.console_set_default_foreground(0, color) # Apply window's color.
        # Draw the corners.
        rl.console_set_char(0, self.x, self.y, rl.CHAR_DNW)
        rl.console_set_char(0, self.x+self.w-1, self.y, rl.CHAR_DNE)
        rl.console_set_char(0, self.x, self.y+self.h-1, rl.CHAR_DSW)
        rl.console_set_char(0, self.x+self.w-1, self.y+self.h-1, rl.CHAR_DSE)
        # Draw the walls.
        for i in range(self.y+1,self.y+self.h-1):
            rl.console_set_char(0, self.x, i, rl.CHAR_DVLINE)
            rl.console_set_char(0, self.x+self.w-1, i, rl.CHAR_DVLINE)
        for i in range(self.x+1,self.x+self.w-1):
            rl.console_set_char(0, i, self.y, rl.CHAR_DHLINE)
            rl.console_set_char(0, i, self.y+self.h-1, rl.CHAR_DHLINE)
        if self.title != None: # Draw the title, if present.
            rl.console_print(0,self.x+2,self.y," {0} ".format(self.title))
        rl.console_set_default_foreground(0, oldColor) # Revert color before drawing rest of window.
        for i,option in enumerate(self.options): # Draw the options.
            rl.console_print(0, self.x+4, self.y+1+i, option)
        rl.console_print(0, self.x+2, self.y+1+self.selectedOption, chr(rl.CHAR_ARROW2_E))
    
    def forward(self): # If enter or the like is pressed and this is the active box.
        return self.options[self.selectedOption] # Return the selected item.
    
    def backward(self): # If escape or the like is pressed and this is the active box.
        return "CLOSE" # Close the box.
    
    def goUp(self): # If up or the like is pressed.
        self.selectedOption = (self.selectedOption + len(self.options) - 1) % len(self.options) # Go up one option.
    
    def goDown(self): # If down or the like is pressed.
        self.selectedOption = (self.selectedOption + 1) % len(self.options) # Go down one option.