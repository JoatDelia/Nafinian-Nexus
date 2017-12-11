import libtcodpy as rl

import boxes as bx

class BattleScene: # As the name suggests, the title screen.
    def __init__(self):
        self.partyBoxes = (bx.Box(0,0,22,6,"Benjamin"),bx.Box(0,6,22,6,"Lucy"),bx.Box(0,12,22,6,"Yorrick"),bx.Box(0,18,22,6,None)) # The (empty) status boxes for the main party.
        self.enemyBoxes = (bx.Box(59,0,21,4,"Dust Bunny"),bx.Box(59,4,21,4,"Dust Bunny"),bx.Box(59,8,21,4,"Dust Bunny"),bx.Box(59,12,21,4,"Dust Bunny"),bx.Box(59,16,21,4,"Dust Bunny"),bx.Box(59,20,21,4,None)) # The (empty) status boxes for the enemies.
        self.infoBox = bx.Box(22,10,37,14,"Combat Log")
        self.turnBox = bx.Box(22,0,20,3,None,"CHARNAME's Turn")
        self.turnOrderBox = bx.Box(42,0,17,10,"Turn Order")

    def refresh(self):
        for box in self.partyBoxes:
            box.draw(rl.white)
        for box in self.enemyBoxes:
            box.draw(rl.white)
        self.infoBox.draw(rl.white)
        self.turnBox.draw(rl.white)
        self.turnOrderBox.draw(rl.white)
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                command = self.box.forward() # Retrieve the selected option.
                if command == "Exit":
                    raise SystemExit # Exit
                elif command == "Modding":
                    return "DevMenuScene"
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