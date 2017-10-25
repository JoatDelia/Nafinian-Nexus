import libtcodpy as rl

import boxes as bx

class TitleScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = bx.SelectBox(33,17,14,6,None,("New Game","Continue","Modding","Exit"),4) # The main menu box.

    def refresh(self):
        rl.console_print(0, 7, 2, "#  #  ##  #### ###  #  # ###  ##  #  #     #  # #### #  # #  #  ###\n## # #  # #     #   ## #  #  #  # ## #     ## # #    #  # #  # #\n# ## #### ###   #   # ##  #  #### # ##     # ## ###   ##  #  #  ##\n#  # #  # #     #   #  #  #  #  # #  #     #  # #    #  # #  #    #\n#  # #  # #    ###  #  # ### #  # #  #     #  # #### #  #  ##  ###") # Draw the title.
        self.box.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                command = self.box.forward() # Retrieve the selected option.
                if command == "Exit":
                    raise SystemExit # Exit
                print(command) # Just print it for now.
            elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
                self.box.goDown() # Go down one item.
            elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
                self.box.goUp() # Go up one item.
            elif key.vk == rl.KEY_ESCAPE:
                raise SystemExit # Also exit
            elif key.vk == rl.KEY_F4 and rl.console_is_key_pressed(rl.KEY_ALT):
                raise SystemExit # Revenge of the exit