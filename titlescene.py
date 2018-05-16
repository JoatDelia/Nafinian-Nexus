import libtcodpy as rl

import boxes as bx

import actors # This will eventually go unused, but it's temporarily needed.

class TitleScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = bx.SelectBox(-1,17,-1,-1,None,("New Game","Continue","Modding","Exit"),-1) # The main menu box. In the first demo, New Game and Exit will likely be the only options available.
        self.image = rl.image_load('nntitle.png'.encode()) # Load the title screen image. A placeholder, at the moment.

    def refresh(self):
        rl.console_clear(0) # Fill the window the background color.
        rl.image_blit_2x(self.image, 0, 0, 0) # Display the title screen image.
        rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
        rl.console_set_default_background(0, rl.black) # Sets the background color to black.
        self.box.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.console_check_for_keypress(True) # Halt until a key is pressed. Note that this is a blocking function (will not proceed until a key is pressed), and thus should never be used if refresh() is capable of changing the scene.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_KPENTER:
                command = self.box.forward() # Retrieve the selected option.
                if command == "Exit":
                    raise SystemExit # Exit
                elif command == "Modding":
                    return "DevMenuScene"
                elif command == "New Game":
                    return "BattleScene"
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
        return None
    
    def getParty(self):
        members = []
        newMember = actors.Chara()
        newMember.setName("Benjamin")
        newMember.setStr(25)
        newMember.setEnd(35)
        newMember.setDex(55)
        newMember.setWil(90)
        newMember.setInt(102)
        members.append(newMember)
        newMember = actors.Chara()
        newMember.setName("Gina")
        newMember.setStr(35)
        newMember.setDex(55)
        newMember.setWil(110)
        newMember.setInt(62)
        members.append(newMember)
        newMember = actors.Chara()
        newMember.setName("Alzoru")
        newMember.setStr(41)
        newMember.setEnd(65)
        newMember.setDex(55)
        newMember.setWil(55)
        newMember.setInt(70)
        members.append(newMember)
        newMember = actors.Chara()
        newMember.setName("Dismas")
        newMember.setEnd(70)
        newMember.setDex(50)
        members.append(newMember)
        return members
        # There is no party yet, so generate a new one. For now, just a dummy one. Later on in development, this will generate an error.
    
    def getEnemies(self):
        members = []
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny A")
        members.append(newMember)
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny B")
        members.append(newMember)
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny C")
        members.append(newMember)
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny D")
        members.append(newMember)
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny E")
        members.append(newMember)
        newMember = actors.Enemy()
        newMember.setName("Dust Bunny F")
        members.append(newMember)
        return members