import libtcodpy as rl

import boxes as bx

import time

class GameOverScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = None # The main menu box. In the first demo, New Game and Exit will likely be the only options available.
        self.imageFull = rl.image_load('gameOver.png'.encode()) # Load the title screen image. A placeholder, at the moment.
        self.imageLeft = rl.image_load('gameOverLeft.png'.encode()) # Load the title screen image. A placeholder, at the moment.
        self.imageRight = rl.image_load('gameOverRight.png'.encode()) # Load the title screen image. A placeholder, at the moment.
        self.startTime = time.time()

    def refresh(self):
        rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
        rl.console_set_default_background(0, rl.black) # Sets the background color to black.
        if self.box == None:
            if time.time() >= self.startTime + 1.0:
                self.box = self.box = bx.SelectBox(-1,17,-1,-1,None,("Return to Title",),-1) # The main menu box. In the first demo, New Game and Exit will likely be the only options available.
            else:
                rl.image_blit_2x(self.imageLeft, 0, int((time.time() - self.startTime) * 40) - 40, 0) # Display the title screen image.
                rl.image_blit_2x(self.imageRight, 0, 80 - int((time.time() - self.startTime) * 40), 0) # Display the title screen image.
        if self.box != None:
            rl.console_clear(0) # Fill the window the background color.
            rl.image_blit_2x(self.imageFull, 0, 0, 0) # Display the title screen image.
            self.box.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Note that this is a blocking function (will not proceed until a key is pressed), and thus should never be used if refresh() is capable of changing the scene.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                if self.box == None: # Don't do anything if there's no box yet.
                    return None
                command = self.box.forward() # Retrieve the selected option.
                if command == "Return to Title":
                    return "TitleScene"
                print(command) # Just print it for now.
                return None
            elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
                self.box.goDown() # Go down one item.
                return None
            elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
                self.box.goUp() # Go up one item.
                return None
        return None