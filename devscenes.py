import libtcodpy as rl

import boxes as bx

class DevMenuScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = bx.SelectBox(-1,-1,-1,-1,"Modding Menu",("Basic Details","Biomes","Classes","Dialogues","Enemies","Equipment","Feats","Items","Names","Races","Screens","Spells","Save","Load","Exit"),-1) # The main menu box.

    def refresh(self):
        self.box.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                command = self.box.forward() # Retrieve the selected option.
                if command == "Exit":
                    return "TitleScene"
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