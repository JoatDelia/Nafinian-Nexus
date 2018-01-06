import libtcodpy as rl

import boxes as bx

import random

class BattleScene: # As the name suggests, the title screen.
    def advanceTurn(self): # Move on to the next turn.
        self.moveBoxes = [] # Close any move boxes that may be open.
        self.turnOrder.append(self.turnOrder.pop(0)) # Send the actor at the front of the line to the back of the line.

    def addToLog(self,message): # Appends to the log, then clears any lines necessary to make room for the new message.
        self.log.append(message)
        while rl.console_get_height_rect(0,0,0,31,24,"\n".join(self.log))>13:
            self.log.pop(0)
    
    def __init__(self,newParty,newEnemies):
        self.party = newParty # The adventuring party, retrieved from the previous scene.
        self.enemies = newEnemies # The enemies. Will later be retrieved from the previous scene, but for now will just be generated on the spot.
        # Determine turn order.
        self.turnOrder = [] # Store the turn order.
        for ally in self.party: # Add all allies.
            self.turnOrder.append(ally)
        for enemy in self.enemies: # Add all enemies.
            self.turnOrder.append(enemy)
        random.shuffle(self.turnOrder) # Shuffle the array.
        # Later, there will be the extra step of sorting by DEX, but for now, leaving it as-is. Even then, the initial shuffle will be necessary, to randomly break any ties resulting from two actors having the same DEX.
        self.log = [] # The current combat log.
        self.partyBoxes = [] # The boxes to display on the left.
        for i in range(4): # Draw party boxes, deciding whether to have a name displaying in each or not.
            if len(self.party) > i:
                self.partyBoxes.append(bx.Box(0,i*6,22,6,self.party[i].getName()))
            else:
                self.partyBoxes.append(bx.Box(0,i*6,22,6,None))
        self.enemyBoxes = [] # The boxes to display on the right.
        for i in range(6): # Draw enemy boxes, deciding whether to have a name displaying in each or not.
            if len(self.enemies) > i:
                self.enemyBoxes.append(bx.Box(59,i*4,21,4,self.enemies[i].getName()))
            else:
                self.enemyBoxes.append(bx.Box(59,i*4,21,4,None))
        self.infoBox = bx.Box(22,10,37,14,"Combat Log") # This box has no function in itself, but will show the combat log via code in refresh().
        self.turnBox = bx.Box(22,0,20,3) # This box has no function in itself, but will show whose turn it is via code in refresh().
        self.turnOrderBox = bx.Box(42,0,17,10,"Turn Order") # The idea behind this box should be clear. This one will also be dynamically resized based on party size.
        self.image = rl.image_load('battlebg2.png'.encode()) # Load the test battle background image. This will later be able to be toggled via an option in the options menu.
        self.moveBoxes = []

    def refresh(self):
        # First, handle the flow of combat.
        if self.turnOrder[0].isAI(): # If it's an enemy's turn, act according to their AI.
            self.addToLog(self.turnOrder[0].aiAct(self.party)) # Execute the enemy AI, thne add the result to the log.
            self.advanceTurn() # Move to the next turn.
        elif len(self.moveBoxes) == 0: # Otherwise, it must be the player's turn. If there aren't any move boxes open, open one.
            self.moveBoxes.append(bx.SelectBox(22,3,-1,-1,None,("Attack",),-1))
        # Now on to the actual display.
        for i,box in enumerate(self.partyBoxes): # Display the party boxes. Only the boxes themselves for now.
            if len(self.party) <= i: # Draw a gray box if party member is not present.
                box.draw(rl.darkest_gray)
            else:
                box.draw(rl.sky) # Otherwise, draw the normal party box.
        for i,box in enumerate(self.enemyBoxes): # Display the enemy boxes. Only the boxes themselves for now.
            if len(self.enemies) <= i: # Draw a gray box if enemy is not present.
                box.draw(rl.darkest_gray)
            else:
                box.draw(rl.crimson) # Otherwise, draw the normal party box.
        self.infoBox.draw(rl.white) # Draw the combat log box.
        self.turnBox.draw(rl.white) # Draw the X's Turn box.
        rl.console_print_ex(0, 32, 1, rl.BKGND_NONE, rl.CENTER, "{0}".format(self.turnOrder[0].getColoredName())) # Draw whose turn it is.
        numBattlers = 0 # The number of conscious actors in the fight that will be shown in the turn order box (as such, this should never exceed 7).
        actorList = "" # The list of conscious actors in the fight, in the order they appear in turnOrder.
        for actor in self.turnOrder: # For each actor...
            if numBattlers < 7 and actor.getHP() > 0: # If they're conscious and the turn order box isn't already filled up...
                numBattlers += 1 # Increase the size of the box by one.
                actorList += actor.getColoredName()+"\n" # Add the battler to the list.
        self.turnOrderBox.setHeight(numBattlers+2) # Adjust the turn order box's size to match the amount of conscious battlers.
        self.turnOrderBox.draw(rl.white) # Draw the turn order box.
        rl.console_set_char(0, 44, 1, ">") # Draw the cursor in the turn order box. Purely aesthetic.
        rl.console_print(0, 46, 1, actorList) # Draw the list of conscious battlers in the turn order box.
        for i,box in enumerate(self.moveBoxes): # Draw all the move boxes, the current one being yellow.
            if i+1 == len(self.moveBoxes):
                box.draw(rl.yellow)
            else:
                box.draw(rl.white)
        y = 11 # The line to draw the current log entry at.
        for msg in self.log: # Draw the lines of the log, advancing y as appropriate.
            rl.console_set_char(0, 24, y, ">") # Draw something to indicate when a log line starts. This ensures it is clear when one entry ends and a new one begins.
            rl.console_print_rect(0, 26, y, 33, 12, msg) # Draw the log line.
            y += rl.console_get_height_rect(0, 0, 0, 32, 12, msg) # Lower the y coordinate.
        # Once all that is drawn, draw the background image.
        rl.image_blit_rect(self.image, 0, 0, 0, 80, 24, rl.BKGND_SET) # Display the battle background image.
        rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
        rl.console_set_default_background(0, rl.black) # Sets the background color to black.
        # However, only after that should the actual stats be drawn. This is so the life bar backgrounds can override the background image.
        for i,box in enumerate(self.partyBoxes): # Display the party boxes.
            if not len(self.party) <= i: # Draw a gray box if party member is not present.
                rl.console_print(0, 2, i*6+1, self.party[i].getLine1()) # Draw first line of stats.
        for i,box in enumerate(self.enemyBoxes): # Display the enemy boxes.
            if not len(self.enemies) <= i: # Draw a gray box if party member is not present.
                rl.console_print(0, 61, i*4+1, self.enemies[i].getLine1()) # Draw first line of stats.
    
    def handleInput(self):
        key = rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
        if key.pressed == True: # Only process key press, not key release.
            if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_SPACE or key.vk == rl.KEY_KPENTER:
                if len(self.moveBoxes) == 0: # Don't do anything if the menu isn't open.
                    return None
                command = self.moveBoxes[len(self.moveBoxes)-1].forward() # Retrieve the selected option.
                if command == "Attack": # If the command is to attack, then do so. Later, this will switch to an attack type selector.
                    self.addToLog(self.party[0].attack(self.enemies[0])) # Do the attack itself.
                    self.advanceTurn()
                return None
            elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
                if len(self.moveBoxes) > 0:
                    self.moveBoxes[len(self.moveBoxes)-1].goDown() # Go down one item.
                return None
            elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
                if len(self.moveBoxes) > 0:
                    self.moveBoxes[len(self.moveBoxes)-1].goUp() # Go up one item.
                return None
            elif key.vk == rl.KEY_ESCAPE: # Remove the latest move box, if there are more than one.
                if len(self.moveBoxes) > 1:
                    self.moveBoxes.pop()
            elif key.vk == rl.KEY_F4 and rl.console_is_key_pressed(rl.KEY_ALT):
                raise SystemExit # Pressing Alt+F4 is against the laws of the game and is punishable with exile.
                return None
        return None