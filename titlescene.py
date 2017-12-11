import libtcodpy as rl

import boxes as bx

class TitleScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = bx.SelectBox(-1,17,-1,-1,None,("New Game","Continue","Modding","Exit"),-1) # The main menu box.
        self.image = rl.image_load('nntitle.png'.encode()) # Load the title screen image.

    def refresh(self):
        rl.image_blit_2x(self.image, 0, 0, 0) # Display the title screen image.
        rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
        rl.console_set_default_background(0, rl.black) # Sets the background color to black.
        # rl.console_print(0, 7, 2, "#  #  ##  #### ###  #  # ###  ##  #  #     #  # #### #  # #  #  ###\n## # #  # #     #   ## #  #  #  # ## #     ## # #    #  # #  # #\n# ## #### ###   #   # ##  #  #### # ##     # ## ###   ##  #  #  ##\n#  # #  # #     #   #  #  #  #  # #  #     #  # #    #  # #  #    #\n#  # #  # #    ###  #  # ### #  # #  #     #  # #### #  #  ##  ###") # Draw the title.
        self.box.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                command = self.box.forward() # Retrieve the selected option.
                if command == "Exit":
                    raise SystemExit # Exit
                elif command == "Modding":
                    return "DevMenuScene"
                elif command == "New Game":
                    return "BattleScene"
                print(command) # Just print it for now.
                return None
            elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
                self.box.goDown() # Go down one item.
                return None
            elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
                self.box.goUp() # Go up one item.
                return None
            elif key.vk == rl.KEY_ESCAPE:
                raise SystemExit # Also exit
                return None
            elif key.vk == rl.KEY_F4 and rl.console_is_key_pressed(rl.KEY_ALT):
                raise SystemExit # Revenge of the exit
                return None
        return None