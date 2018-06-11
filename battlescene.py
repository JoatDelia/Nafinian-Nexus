import libtcodpy as rl

import boxes as bx

import random

import time

from actors import Chara,Enemy

# For convenience and code clarity, pseudo-constants representing two of the possible values for animTarget. None of the other values would be directly specified, so they can safely be skipped.
ALL_ALLIES = 10
ALL_ENEMIES = 11

class BattleScene: # As the name suggests, the title screen.
    def advanceTurn(self): # Move on to the next turn.
        self.moveBoxes = [] # Close any move boxes that may be open.
        self.turnOrder[0].decrementStatusEffects() # Decrement status effects of the old active combatant.
        self.turnOrder.append(self.turnOrder.pop(0)) # Send the actor at the front of the line to the back of the line.
        self.animPhase = 0 # Reset the animation to none.
        self.addToLog(self.turnOrder[0].turnStartRegen()) # Apply start-of-turn regeneration.
        if self.turnOrder[0].getHP() <= 0: # Keep advancing turns until a conscious combatant is reached.
            self.advanceTurn()

    def addToLog(self,message): # Appends to the log, then clears any lines necessary to make room for the new message.
        if message == None: # If nothing was sent, end the function.
            return
        self.log.append(message) # Add the message.
        while rl.console_get_height_rect(0,0,0,31,24,"\n".join(self.log))>12: # CLear lines as needed.
            self.log.pop(0)
    
    def checkBattleStatus(self): # Check if the battle is won or lost.
        partyAlive = False # Whether the party has any members conscious.
        for member in self.party: # Check each party membr in turn.
            if member.getHP() > 0:
                partyAlive = True
        if partyAlive == False: # If none are, game over.
            return "GameOverScene"
        enemiesAlive = False # Whether enemies remain.
        for member in self.enemies: # CHeck each enemy in turn.
            if member.getHP() > 0:
                enemiesAlive = True
        if enemiesAlive == False: # If none are, victory!
            return "TitleScene"
    
    def parseTurnResults(self,results=None): # This does various things based on what a given turn action returned.
        if results == None: # If there aren't any results (usually if the move is impossible for some reason), do nothing at all.
            return
        if 'log' in results: # If a log entry exists in the results, add it to the logs.
            self.addToLog(results['log'])
        if 'cancel' in results: # If a cancel entry exists in the results (the value doesn't matter), stop here.
            return
        self.moveBoxes = [] # Close any move boxes that may be open.
        if 'animTarget' in results: # If a target for the animation is defined
            self.animTarget = results['animTarget']
            if self.animPhas/e == 0: # If animPhase is 0, change it to 2.
                self.animPhase = 2
        elif 'target' in results: # If a target for the move is defined, this means the animTarget needs to be determined from the target provided.
            if results['target'] in self.party: # If the target can be found in the party...
                self.animTarget = self.party.index(results['target']) # ...set the animTarget according to where in the array it is found.
                if self.animPhase == 0: # If animPhase is 0, change it to 2.
                    self.animPhase = 2
            elif results['target'] in self.enemies: # Same, but for enemies.
                self.animTarget = self.enemies.index(results['target']) + 4
                if self.animPhase == 0:
                    self.animPhase = 2
            else: # If the target doesn't exist, as a failsafe, simply don't play an animation.
                self.animPhase = 0
        else: # If there is no sort of target specified, don't try to play an animation. Just go on to the next turn.
            self.animPhase = 0
            self.advanceTurn()
        if self.animPhase > 0: # If an animation was started, set animStarted accordingly.
            self.animStarted = time.time()
    
    def __init__(self,newParty,newEnemies):
        self.party = newParty # The adventuring party, retrieved from the previous scene.
        self.enemies = newEnemies # The enemies. Will later be retrieved from the previous scene, but for now will just be generated on the spot.
        self.nextScene = None # The scene to advance to. This is meant for when one side loses.
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
        self.turnBox = bx.Box(22,0,18,3) # This box has no function in itself, but will show whose turn it is via code in refresh().
        self.turnOrderBox = bx.Box(40,0,19,10,"Turn Order") # The idea behind this box should be clear. This one will also be dynamically resized based on party size.
        self.image = rl.image_load('battlebg2.png'.encode()) # Load the test battle background image. This will later be able to be toggled via an option in the options menu.
        self.moveBoxes = [] # The boxes for the character's action selection.
        self.animPhase = 0 # Which phase the animation is in. 1 is playing the animation itself, 2 is the target's box blinking, 0 is no animation.
        self.animStarted = time.time() # When the current animation phase started. This theoretically doesn't need to be initialized yet, but just in case...
        self.animTarget = 0 # Who the current animation is playing on. 0-3 are party members, 4-9 are enemies, 10 is all party members, 11 is all enemies.

    def refresh(self):
        # First, handle the flow of combat or the active animation.
        if self.animPhase == 2: # If the blinking box phase is active, handle that.
            if time.time() >= self.animStarted + 0.5: # If a second has passed since this animation phase started, end it.
                self.animPhase = 0
                if self.checkBattleStatus() != None: # If the battle is won or lost, change the current scene.
                    return self.checkBattleStatus()
                self.advanceTurn() # Move to the next turn.
        else: # If there is no animation going on, handle the flow of combat.
            if self.turnOrder[0].isAI(): # If it's an enemy's turn, act according to their AI.
                self.parseTurnResults(self.turnOrder[0].aiAct(self.party,self.enemies)) # Execute the enemy AI, thne add the result to the log.
            elif len(self.moveBoxes) == 0: # Otherwise, it must be the player's turn. If there aren't any move boxes open, open one.
                self.moveBoxes.append(bx.SelectBox(22,3,-1,-1,None,self.turnOrder[0].getOptions(),-1))
        # Now on to the actual display.
        rl.console_clear(0) # Fill the window with the background color.
        for i,box in enumerate(self.partyBoxes): # Display the party boxes. Only the boxes themselves for now.
            if len(self.party) <= i or self.party[i].isDead(): # Draw a gray box if party member is not present or dead.
                box.draw(rl.darker_gray)
            else: # Otherwise, draw normal stats, aside from the bars.
                rl.console_print(0, 12, i*6+1, self.party[i].getHPLine()) # Draw HP.
                rl.console_print(0, 12, i*6+2, self.party[i].getAPLine()) # Draw AP.
                rl.console_print(0, 12, i*6+3, self.party[i].getMPLine()) # Draw MP.
                rl.console_print(0, 2, i*6+4, self.party[i].getStatusLine(18)) # Draw status effects.
            if len(self.party) <= i or self.party[i].getHP() <= 0: # Draw a red box if party member is unconscious.
                box.draw(rl.darker_red)
            elif self.animPhase == 2 and (self.animTarget == i or self.animTarget == ALL_ALLIES) and int((time.time() - self.animStarted) * 8) % 2 == 0: # If the current animPhase is 2, this is the current animation target, and the time since the animation started dictates the box should be dark red, make it dark red.
                pass
            else: # Otherwise, draw the normal party box.
                box.draw(rl.sky)
        for i,box in enumerate(self.enemyBoxes): # Display the enemy boxes. Only the boxes themselves for now.
            if len(self.enemies) <= i or self.enemies[i].getHP() <= 0: # Draw a gray box if enemy is not present or KO'd.
                box.draw(rl.darker_gray)
            elif self.animPhase == 2 and (self.animTarget - 4 == i or self.animTarget == ALL_ENEMIES) and int((time.time() - self.animStarted) * 8) % 2 == 0: # If the current animPhase is 2, this is the current animation target, and the time since the animation started dictates the box should be dark red, make it dark red.
                rl.console_print(0, 61, i*4+2, self.enemies[i].getStatusLine(18)) # Draw status effects.
            else:
                box.draw(rl.crimson) # Otherwise, draw the normal party box.
                rl.console_print(0, 61, i*4+2, self.enemies[i].getStatusLine(18)) # Draw status effects.
        self.infoBox.draw(rl.white) # Draw the combat log box.
        self.turnBox.draw(rl.white) # Draw the X's Turn box.
        rl.console_print_ex(0, 31, 1, rl.BKGND_NONE, rl.CENTER, "{0}".format(self.turnOrder[0].getColoredName())) # Draw whose turn it is.
        numBattlers = 0 # The number of conscious actors in the fight that will be shown in the turn order box (as such, this should never exceed 7).
        actorList = "" # The list of conscious actors in the fight, in the order they appear in turnOrder.
        for actor in self.turnOrder: # For each actor...
            if numBattlers < 8 and actor.getHP() > 0: # If they're conscious and the turn order box isn't already filled up...
                numBattlers += 1 # Increase the size of the box by one.
                actorList += actor.getColoredName()+"\n" # Add the battler to the list.
        self.turnOrderBox.setHeight(numBattlers+2) # Adjust the turn order box's size to match the amount of conscious battlers.
        self.turnOrderBox.draw(rl.white) # Draw the turn order box.
        rl.console_set_char(0, 42, 1, ">") # Draw the cursor in the turn order box. Purely aesthetic.
        rl.console_print(0, 44, 1, actorList) # Draw the list of conscious battlers in the turn order box.
        y = 11 # The line to draw the current log entry at.
        for msg in self.log: # Draw the lines of the log, advancing y as appropriate.
            rl.console_set_char(0, 24, y, ">") # Draw something to indicate when a log line starts. This ensures it is clear when one entry ends and a new one begins.
            rl.console_print_rect(0, 26, y, 31, 12, msg) # Draw the log line.
            y += rl.console_get_height_rect(0, 0, 0, 31, 12, msg) # Lower the y coordinate.
        # Once all that is drawn, draw the background image.
        rl.image_blit_rect(self.image, 0, 0, 0, 80, 24, rl.BKGND_SET) # Display the battle background image.
        rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
        rl.console_set_default_background(0, rl.black) # Sets the background color to black.
        # However, only after that should the actual stats be drawn. This is so the life bar backgrounds can override the background image.
        for i,box in enumerate(self.partyBoxes): # Display the party boxes.
            if not len(self.party) <= i and not self.party[i].isDead(): # Don't draw stats if party member is not present or dead (should still show if merely KO'd.
                rl.console_print(0, 2, i*6+1, self.party[i].getHPBar()) # Draw HP bar.
                rl.console_print(0, 2, i*6+2, self.party[i].getAPBar()) # Draw AP bar.
                rl.console_print(0, 2, i*6+3, self.party[i].getMPBar()) # Draw MP bar.
        for i,box in enumerate(self.enemyBoxes): # Display the enemy boxes.
            if not len(self.enemies) <= i and not self.enemies[i].getHP() <= 0: # Don't draw stats if enemy is not present or KO'd.
                rl.console_print(0, 61, i*4+1, self.enemies[i].getHPBar()) # Draw HP bar.
                rl.console_print(0, 67, i*4+1, self.enemies[i].getAPBar()) # Draw AP bar.
                rl.console_print(0, 73, i*4+1, self.enemies[i].getMPBar()) # Draw MP bar.
        for i,box in enumerate(self.moveBoxes): # Draw all the move boxes, the current one being yellow. Since this can overlap the enemy stats, this must be drawn after that.
            if i+1 == len(self.moveBoxes):
                box.draw(rl.yellow)
            else:
                box.draw(rl.white)
    
    def handleInput(self):
        key = rl.Key() # Set up the variables for mouse and key input.
        mouse = rl.Mouse()
        rl.sys_check_for_event(rl.EVENT_KEY_PRESS|rl.EVENT_MOUSE,key,mouse) # Update the key and mouse variables if a key or mouse button was pressed.
        if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_KPENTER or mouse.lbutton_pressed:
            if len(self.moveBoxes) == 0 or self.animPhase > 0: # Don't do anything if the menu isn't open or a animation is playing.
                return None
            command = None
            if mouse.lbutton_pressed: # If the mouse was clicked, attempt to retrieve a result.
                self.handleCommand(self.moveBoxes[len(self.moveBoxes)-1].handleClick(mouse))
            if (key.vk == rl.KEY_ENTER or key.vk == rl.KEY_KPENTER) and command == None: # If a key was pressed and a mouse click did not occur or yield any results:
                self.handleCommand(self.moveBoxes[len(self.moveBoxes)-1].forward()) # Retrieve the selected option, then send it to a separate function for processing.
            return None
        elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
            if len(self.moveBoxes) > 0:
                self.moveBoxes[len(self.moveBoxes)-1].goDown() # Go down one item.
            return None
        elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
            if len(self.moveBoxes) > 0:
                self.moveBoxes[len(self.moveBoxes)-1].goUp() # Go up one item.
            return None
        elif key.vk == rl.KEY_ESCAPE or mouse.rbutton_pressed: # Remove the latest move box, if there are more than one.
            if len(self.moveBoxes) > 1:
                self.moveBoxes.pop()
        elif key.vk == rl.KEY_F4 and rl.console_is_key_pressed(rl.KEY_ALT):
            raise SystemExit # Pressing Alt+F4 is against the laws of the game and is punishable with exile.
            return None
        else: # Let the box handle any other input.
            if len(self.moveBoxes) == 0 or self.animPhase > 0: # Don't do anything if the menu isn't open or a animation is playing.
                return None
            self.moveBoxes[len(self.moveBoxes)-1].miscInput(key)
        return None
    
    def handleCommand(self,command): # Handle pressing Enter in a choice box. I put this in a separate function because there will be many options and I don't want the key handling function to get too large.
        if isinstance(command,Enemy):# If the command is an enemy use the move on said enemy.
            target = command
            previousCommand = self.moveBoxes[len(self.moveBoxes)-2].forward()
            if previousCommand == "Fire I":
                self.parseTurnResults(self.turnOrder[0].castFireI(target)) # Cast the Fire I spell.
            elif previousCommand == "Bite":
                self.parseTurnResults(self.turnOrder[0].bite(target)) # Do the bite special attack.
            else:
                self.parseTurnResults(self.turnOrder[0].attack(target)) # Do the attack itself.
        if isinstance(command,Chara):# If the command is an ally use the move on said ally.
            target = command
            previousCommand = self.moveBoxes[len(self.moveBoxes)-2].forward()
            if previousCommand == "Heal I":
                self.parseTurnResults(self.turnOrder[0].castHealI(target)) # Cast Heal I.
            if previousCommand == "Sharpen":
                self.parseTurnResults(self.turnOrder[0].castSharpen(target)) # Cast Heal I.
        if command == "Attack": # Open a box to select attack type.
            previousBox = self.moveBoxes[len(self.moveBoxes)-1] # The box that was active before this one.
            self.moveBoxes.append(bx.SelectBox(previousBox.getX()+previousBox.getWidth(),3,-1,-1,None,self.turnOrder[0].getAttackOptions(),-1))
        if command == "Magic": # Open a box to select magic type.
            previousBox = self.moveBoxes[len(self.moveBoxes)-1] # The box that was active before this one.
            self.moveBoxes.append(bx.SelectBox(previousBox.getX()+previousBox.getWidth(),3,-1,-1,None,self.turnOrder[0].getSpellOptions(),-1))
        if command == "Basic" or command == "Bite" or command == "Fire I":
            self.openTargetSelect(self.enemies)
        if command == "Heal I" or command == "Sharpen":
            self.openTargetSelect(self.party)
    
    def openTargetSelect(self, arrayToUse): # Opens the target selection window. This will be needed often enough to justify a separate function. If enemies is false, select from allies instead.
        previousBox = self.moveBoxes[len(self.moveBoxes)-1] # The box that was active before this one.
        self.moveBoxes.append(bx.TargetBox(previousBox.getX()+previousBox.getWidth(),3,arrayToUse))