import libtcodpy as rl

import random

import time

from objnav import objNavigate

class Actor:
    def __init__(self,charaObj=None): # Initialize the character.
        # At some point these self.variables may be replaced with simply a single object tree akin to charaObj. When/if this happens, the getters and setters will be modified accordingly, of course.
        if charaObj == None: # Set attributes to default if there is no existing data provided.
            self.stre = 60 # Strength.
            self.end = 60 # Endurance.
            self.dex = 60 # Dexterity.
            self.per = 60 # Perception.
            self.wil = 60 # Willpower.
            self.inte = 60 # Intelligence.
            self.cha = 60 # Charisma.
            self.luk = 60 # Luck.
            self.name = "CHARNAME" # The name to display.
        else: # If data is provided, populate the character's attributes and name.
            self.stre = objNavigate(charaObj,("Attributes","STRength"))
            self.end = objNavigate(charaObj,("Attributes","ENDurance"))
            self.dex = objNavigate(charaObj,("Attributes","DEXterity"))
            self.per = objNavigate(charaObj,("Attributes","PERception"))
            self.wil = objNavigate(charaObj,("Attributes","WILlpower"))
            self.inte = objNavigate(charaObj,("Attributes","INTelligence"))
            self.cha = objNavigate(charaObj,("Attributes","CHArisma"))
            self.luk = objNavigate(charaObj,("Attributes","LUcK"))
            self.name = objNavigate(charaObj,("Name",))
        self.healFull() # Set current HP, MP, and AP to the proper numbers.
        self.statusEffects = [] # List of current status effects, initially empty.
        self.statusIsScrolling = False # Whether the status effects list is scrolling due to insufficient space to show it all at once..
        self.startedScrolling = time.time() # If so, this is when it started.
    
    def receiveStatus(self,newEffect): # Add a new status effect to a character. This should be an array in the form of [string effect name, boorlean beneficial, integer duration, integer potency (if N/A, put 0)]
        # The valid status effects so far are:
        # Sharpen
        self.statusEffects.append(newEffect)
    
    def decrementStatusEffects(self): # Remove 1 from the duration of all status effects.
        i = 0 # Tracks position in the status effect list.
        while i < len(self.statusEffects): # Go through the list entry by entry.
            self.statusEffects[i][2] -= 1 # Decrement duration by 1.
            if self.statusEffects[i][2] <= 0: # If a status effect has run out, remove it.
                self.statusEffects.pop(i)
            else: # If nothing was removed, increment. If we incremented regardless, that would cause items to be skipped. This is also why a for-in loop is not used.
                i += 1
    
    def getStr(self): # Get strength, accounting for Sharpen.
        returnStat = self.stre
        for effect in self.statusEffects:
            if effect[0] == "Sharpen":
                returnStat += effect[3]
        return returnStat
    
    def setStr(self,x): # Set strength.
        self.stre = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getEnd(self): # Get endurance.
        return self.end
    
    def setEnd(self,x): # Set endurance and other stats that rely on it.
        oldMaxHP = self.getMaxHP() # Store the old max HP.
        oldMaxAP = self.getMaxAP() # Store the old max AP.
        self.end = min(x,1000) # Set the stat, but enforce the maximum.
        self.hp = max(self.hp + self.getMaxHP() - oldMaxHP, 1) # Adjust HP accordingly.
        self.ap = max(self.ap + self.getMaxAP() - oldMaxAP, 0) # Adjust AP accordingly.
        
    def getDex(self): # Get dexterity.
        return self.dex
    
    def setDex(self,x): # Set dexterity.
        self.dex = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getPer(self): # Get perception.
        return self.per
    
    def setPer(self,x): # Set perception.
        self.per = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getWil(self): # Get willpower.
        return self.wil
    
    def setWil(self,x): # Set endurance.
        oldMaxMP = self.getMaxMP() # Store the old max MP.
        oldMaxAP = self.getMaxAP() # Store the old max AP.
        self.wil = min(x,1000) # Set the stat, but enforce the maximum.
        self.mp = max(self.mp + self.getMaxMP() - oldMaxMP, 0) # Adjust MP accordingly.
        self.ap = max(self.ap + self.getMaxAP() - oldMaxAP, 0) # Adjust AP accordingly.
        
    def getInt(self): # Get intelligence.
        return self.inte
    
    def setInt(self,x): # Set intelligence.
        self.inte = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getCha(self): # Get charisma.
        return self.cha
    
    def setCha(self,x): # Set charisma.
        self.cha = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getLuk(self): # Get luck.
        return self.luk
    
    def setLuk(self,x): # Set luck.
        self.luk = min(x,1000) # Set the stat, but enforce the maximum.
    
    def setName(self,x): # Set character's name.
        self.name = x
    
    def getName(self): # Retrieve character's name.
        return self.name
    
    def healFull(self): # Fill up HP, MP, and AP to full. Remove status effects.
        self.hp = self.getMaxHP() # Fully restore HP.
        self.ap = self.getMaxAP() # Fully restore AP.
        self.mp = self.getMaxMP() # Fully restore MP.
        
    def getMaxHP(self): # Calculate and return max HP.
        return max(int(self.getEnd()/5) + self.getMod(self.getEnd()),1)
        
    def getMaxAP(self): # Calculate and return max AP.
        return max(15 + self.getMod(self.getEnd()) + self.getMod(self.getWil()),1)
        
    def getMaxMP(self): # Calculate and return max MP.
        return max(int(self.getWil()/5) + self.getMod(self.getWil()),1)
    
    def getMod(self,x): # Get the modifier for the provided attribute value.
        if x <= 5:
            return -15
        return int((x+4)/5)-12
    
    def getLine1(self): # Get first line of combat status.
        return "Use subclass!"
    
    def getOptions(self): # Get the basic options for a party member or a controlled enemy.
        moves = ["Attack",]
        if len(self.getSpellOptions()) > 0:
            moves.append("Magic")
        return moves
    
    def getAttackOptions(self): # Get options if Attack is chosen.
        moves = ["Basic",]
        if (self.name == "Gina" or self.name == "Alzoru") and self.ap >= 3: # Later on, this will be determined by race and class. Neither exist yet, though, so...
            moves.append("Bite")
        return moves
        
    def getSpellOptions(self): # Get options if Magic is chosen.
        moves = []
        if self.name == "Gina" and self.mp >= 3: # Again, this won't be hard-coded by name in the final game, of course.
            moves.append("Heal I")
        if self.name == "Benjamin" and self.mp >= 3: # As before.
            moves.append("Fire I")
        if self.name == "Alzoru" and self.mp >= 4: # As before.
            moves.append("Sharpen")
        return moves
    
    def isAI(self): # Whether the character is controlled by the AI. Later on, this won't be as simple. But for now, enemies are AI, allies aren't.
        return True
    
    def makeBar(self,current,maximum,length): # Make a bar for the current and max values given, of the length given.
        bar = "" # The value to return.
        for i in range(1,length+1): # For each segment to draw...
            if float(current)/float(maximum)>=(float(i)-0.25)/float(length): # Draw a full block if warranted
                bar+=chr(219)
            elif float(current)/float(maximum)>=(float(i)-0.75)/float(length): # Draw a half block if warranted.
                bar+=chr(221)
            else: # Draw an empty block, otherwise.
                bar+=" "
        return bar
    
    def getColoredName(self): # Get the name, with associated color coding, for use in the combat log.
        return chr(rl.COLCTRL_FORE_RGB)+chr(255)+chr(255)+chr(255)+self.name+chr(rl.COLCTRL_STOP)
    
    def damage(self,amount): # Lower HP by the given amount. Negative numbers are reduced to 0.
        self.hp -= max(amount,0) # Subtract the HP.
        if self.hp <= 0: # AP is reduced to 0 on KO.
            self.ap = 0
    
    def heal(self,amount): # Raise HP by the given amount. Negative numbers are reduced to 0.
        self.hp += max(amount,0) # Add the HP.
        if self.hp > self.getMaxHP(): # Enforce the health cap.
            self.hp = self.getMaxHP()
    
    def attack(self,target): # Attack the specified foe.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getPer()) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex())
        luckRoll = random.randint(1,6) # 6 is lucky strike. 1 is lucky defense.
        luckString = "" # The text to add for a lucky strike or defense.
        damageAmt = max(random.randint(1,6)+random.randint(1,6)+self.getAttackMod()-target.getDefenseMod() + int(self.getMod(self.getLuk()) / 4 + 0.5),0) # Damage to deal, if the attack hits.
        if luckRoll == 1: # Account for lucky defense.
            luckString = " (Luckless Defense)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Defense)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Defense)"
            dodgeRoll += target.getMod(self.getLuk())
            damageAmt -= target.getMod(self.getLuk())
        if luckRoll == 1: # Account for lucky strike.
            luckString = " (Luckless Strike)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Strike)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Strike)"
            hitRoll += self.getMod(self.getLuk())
            damageAmt += self.getMod(self.getLuk())
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}{2}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        if dodgeRoll == hitRoll:
            damageAmt = int(damageAmt / 2 + 0.5)
            message = "{0} grazes {1} for {2} damage{3}.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        else:
            message = "{0} hits {1} for {2} damage{3}.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt) # Damage the target by the appropriate amount.
        if target.getHP() <= 0: # Show a message for knockout.
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def bite(self,target): # Bite the specified foe.
        self.ap -= 3 # Remove AP for bite. No need to check here - if the character has insufficient AP, Bite shouldn't appear in the first place.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getPer()) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex())
        luckRoll = random.randint(1,6) # 6 is lucky strike. 1 is lucky defense.
        luckString = "" # The text to add for a lucky strike or defense.
        damageAmt = max(random.randint(9,18)+self.getMod(self.getStr())-target.getDefenseMod(),0) # This isn't a weapon attack, so does not include weapon mod. Instead, just simply use Strength.
        if luckRoll == 1: # Account for lucky defense.
            luckString = " (Luckless Defense)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Defense)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Defense)"
            dodgeRoll += target.getMod(self.getLuk())
            damageAmt -= target.getMod(self.getLuk())
        if luckRoll == 1: # Account for lucky strike.
            luckString = " (Luckless Strike)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Strike)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Strike)"
            hitRoll += self.getMod(self.getLuk())
            damageAmt += self.getMod(self.getLuk())
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}{2}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        if dodgeRoll == hitRoll:
            damageAmt = int(damageAmt / 2 + 0.5)
            message = "{0}'s tooth grazes {1} for {2} damage{3}.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        else:
            message = "{0} bites {1} for {2} damage{3}.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt) # ...but for now, it just deals 2d6 damage.
        if target.getHP() <= 0:
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def castHealI(self,target): # Cast Heal I on the specified ally.
        if target.hp == target.getMaxHP(): # Don't heal someone who's already at full health.
            return {'log': target.getColoredName()+" is already at full health!", 'cancel': None}
        self.mp -= 3 # Remove MP for Heal I. This is a flat 3 for now, since Heal I is a cross-class spell for Gina, but later there would be a check for circumstances like that.
        healAmt = random.randint(1,4) + self.getMod(self.getWil()) # Amount of HP to heal.
        message = "{0} casts Heal I on {1}, restoring {2}HP.".format(self.getColoredName(),target.getColoredName(),healAmt) # Announce the healing.
        wasUnconscious = target.hp <= 0 # Whether the actor was previously unconscious.
        target.heal(healAmt) # Do the healing.
        if target.hp > 0 and wasUnconscious: # Add an extra note if the actor recovered from unconsciousness.
            message += " "+target.getColoredName()+" gets back up!"
        return {'log': message} # Return the message to send to the combat log.
    
    def castFireI(self,target): # Cast Fire I the specified foe.
        self.mp -= 3 # Remove MP for Fire I.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getPer()) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex())
        luckRoll = random.randint(1,6) # 6 is lucky strike. 1 is lucky defense.
        luckString = "" # The text to add for a lucky strike or defense.
        damageAmt = max(random.randint(1,6) + self.getMod(self.getInt()) - target.getSpecialDefenseMod(),0)
        if luckRoll == 1: # Account for lucky defense.
            luckString = " (Luckless Defense)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Defense)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Defense)"
            dodgeRoll += target.getMod(self.getLuk())
        if luckRoll == 1: # Account for lucky strike.
            luckString = " (Luckless Strike)"
            if target.getMod(self.getLuk()) > 0:
                luckString = " (Lucky Strike)"
            elif target.getMod(self.getLuk()) < 0:
                luckString = " (Unlucky Strike)"
            hitRoll += self.getMod(self.getLuk())
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} casts Fire I, but misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        message = "{0} casts Fire I on {1} for {2} damage.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt) # Deal the damage.
        if target.getHP() <= 0: # Handle knockouts.
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def castSharpen(self,target): # Cast Sharpen on the specified ally.
        self.mp -= 4 # Remove MP for Sharpen.
        buffAmount = 5 + random.randint(1,6) + self.getMod(self.getInt()) # Determine amount to boost STR by.
        message = "{0} casts Sharpen on {1}, increasing STR by {2}.".format(self.getColoredName(),target.getColoredName(),buffAmount) # Announce the action.
        target.receiveStatus(["Sharpen",True,5,buffAmount]) # Activate the buff.
        return {'log': message} # Return the message to send to the combat log.
    
    def aiAct(self,party): # What the AI does with the character's turn. For now, just attack a random party member.
        return self.attack(random.choice(party))
    
    def getHP(self): # Retrieve current (not max) HP.
        return self.hp
        
    def getAttackMod(self): # Later, this will prperly calculate from the party's equipment. Equipment doesn't exist yet, so it's being simulated in this case.
        if self.name == "Benjamin": # Simulating Wooden Training Sword
            return 3 + self.getMod(self.getStr())
        if self.name == "Gina": # Simulating Quartz Orb
            return 3 + self.getMod(self.getWil())
        if self.name == "Alzoru": # Simulating Shell Ocarina
            return 2 + self.getMod(self.getCha())
        if self.name == "Dismas": # Simulating Worn Knife
            return 4 + self.getMod(self.getDex())
        return self.getMod(self.getStr()) # For anyone else, don't simulate equipment.
    
    def getDefenseMod(self): # Same applies here as to getAttackMod.
        if self.name == "Benjamin": # Simulating Circular Wood Shield
            return 2 + self.getMod(self.getEnd()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Gina": # Simulating Circular Wood Shield
            return 2 + self.getMod(self.getEnd()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Alzoru": # Simulating Anikto leather tunic, Anikto leather waistcoat
            return 5 + self.getMod(self.getEnd()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Dismas": # Simulating Leather Waistcoat
            return 2 + self.getMod(self.getEnd()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        return self.getMod(self.getEnd()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5) # For anyone else, don't simulate equipment.
    
    def getSpecialDefenseMod(self): # Same as getDefenseMod, but using Willpower.
        if self.name == "Benjamin": # Simulating Circular Wood Shield
            return 2 + self.getMod(self.getWil()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Gina": # Simulating Circular Wood Shield
            return 2 + self.getMod(self.getWil()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Alzoru": # Simulating Anikto leather tunic, Anikto leather waistcoat
            return 5 + self.getMod(self.getWil()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        if self.name == "Dismas": # Simulating Leather Waistcoat
            return 2 + self.getMod(self.getWil()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5)
        return self.getMod(self.getWil()) + random.randint(1,6) + random.randint(1,6) + int(self.getMod(self.getLuk()) / 4 + 0.5) # For anyone else, don't simulate equipment.
    
    def isDead(self): # Whether the actor is dead. The default is death at 0HP, but this works different for party members.
        return self.hp <= 0
    
    def turnStartRegen(self): # Regeneration at the beginning of every turn.
        message = None # Message to display in the log.
        if self.isDead(): # The dead don't regenerate (zombies and stuff aside - you know what I meant).
            return
        if self.getMod(self.getEnd()) >= 0: # Regenerate health, unless Endurance mod is negative.
            wasUnconscious = self.hp <= 0 # Whether the actor was previously unconscious.
            self.hp = min(self.hp + 1 + int(self.getMod(self.getEnd())/5),self.getMaxHP()) # Apply HP regeneration.
            if self.hp > 0 and wasUnconscious: # Extra message if the regeneration caused a revival.
                message = self.getColoredName()+" gets back up!"
        if self.getMod(self.getEnd()) >= 0 and self.hp > 0: # Regenerate stamina, unless Endurance mod is negative or character is unconscious.
            self.ap = min(self.ap + 1 + int(self.getMod(self.getEnd())/10),self.getMaxAP()) # Apply AP regeneration.
        if self.getMod(60) >= 0 and self.hp > 0: # Regenerate mana.
            self.mp = min(self.mp + 1, self.getMaxMP()) # Apply MP regeneration.
        return message
    
    def getStatusLine(self,width): # Return list of status effects. Later, I'll need to account for if the line overflows.
        statusLine = ""
        for i,effect in enumerate(self.statusEffects): # Add each effect to the line, separated by commas.
            if i == 0:
                statusLine = effect[0]
            else:
                statusLine += ", "+effect[0]
        if len(statusLine) > width and not self.statusIsScrolling: # If the status line won't all fit and isn't already scrolling, start it scrolling.
            self.statusIsScrolling = True
            self.startedScrolling = time.time()
        elif len(statusLine) <= width and self.statusIsScrolling: # Inversely, if it will all fit and the status is scrolling, stop it.
            self.statusIsScrolling = False
        if self.statusIsScrolling: # Handle status line scrolling.
            loopedStatusLine = statusLine + ", " + statusLine # A looped version of the status line.
            startingPoint = int((time.time() - self.startedScrolling) * 5) % (len(statusLine) + 2) # Where to start sampling from the looped line.
            return loopedStatusLine[startingPoint:startingPoint + width] # Take a sample from the looped line, making it look like it's scrolling over time.
        return statusLine

class Chara(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(1)+chr(191)+chr(255)+self.name+chr(rl.COLCTRL_STOP)
    
    def isAI(self):
        return False
        
    def isDead(self): # Return whether the party member is dead.
        return self.hp <= -max(self.getMaxHP(),10)
        
    def getHPLine(self): # Return HP text.
        return "{0:>3}/{1:>3}HP".format(self.hp,self.getMaxHP())
        
    def getAPLine(self): # Return AP text.
        return "{0:>3}/{1:>3}AP".format(self.ap,self.getMaxAP())
        
    def getMPLine(self): # Return MP text.
        return "{0:>3}/{1:>3}MP".format(self.mp,self.getMaxMP())
    
    def getHPBar(self): # Returns health bar.
        if self.hp > 0:
            return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),8),chr(rl.COLCTRL_STOP))
        else:
            return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(128),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(32),chr(32),chr(32),self.makeBar(max(self.getMaxHP(),10)+self.hp,max(self.getMaxHP(),10),8),chr(rl.COLCTRL_STOP))
        
    def getAPBar(self): # Return stamina bar.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),8),chr(rl.COLCTRL_STOP))
        
    def getMPBar(self): # Return mana bar.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(1),chr(128),chr(255),chr(rl.COLCTRL_BACK_RGB),chr(1),chr(64),chr(128),self.makeBar(self.mp,self.getMaxMP(),8),chr(rl.COLCTRL_STOP))

class Enemy(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(255)+chr(1)+chr(63)+self.name+chr(rl.COLCTRL_STOP)
        
    def getLine1(self): # Return all bars, no numbers.
        returnLine = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),5),chr(rl.COLCTRL_STOP)) # HP bar!
        returnLine += " {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),5),chr(rl.COLCTRL_STOP)) # AP bar!
        returnLine += " {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(1),chr(128),chr(255),chr(rl.COLCTRL_BACK_RGB),chr(1),chr(64),chr(128),self.makeBar(self.mp,self.getMaxMP(),5),chr(rl.COLCTRL_STOP)) # MP bar!
        # Heart!
        return returnLine # By your powers combined, I am CAPTAIN STATUS!
    
    def aiAct(self,party,enemies): # What the AI does with the character's turn. For now, just attack a random party member.
        partyMembersUp = [] # Conscious party members.
        enemiesUp = [] # Conscious enemies.
        for member in party: # Populate the former.
            if member.getHP() > 0:
                partyMembersUp.append(member) # Populate the latter.
        for member in enemies:
            if member.getHP() > 0:
                enemiesUp.append(member)
        moveNum = random.randint(0,4) # Decide randomly what to do.
        if moveNum == 3 and self.mp >= 4: # If chosen and able to use, do Sharpen on a random enemy.
            return self.castSharpen(random.choice(enemiesUp))
        if moveNum == 2 and self.mp >= 3: # If chosen and able to use, do Fire I on a random party member.
            return self.castFireI(random.choice(partyMembersUp))
        elif moveNum == 1 and self.ap >= 3: # If chosen and able to use, do a bite on a random party member.
            return self.bite(random.choice(partyMembersUp))
        return self.attack(random.choice(partyMembersUp)) # If nothing else, just randomly attack the party.
    
    def getHPBar(self): # Returns health bar.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),5),chr(rl.COLCTRL_STOP))
        
    def getAPBar(self): # Return stamina bar.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),5),chr(rl.COLCTRL_STOP))
        
    def getMPBar(self): # Return mana bar.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(1),chr(128),chr(255),chr(rl.COLCTRL_BACK_RGB),chr(1),chr(64),chr(128),self.makeBar(self.mp,self.getMaxMP(),5),chr(rl.COLCTRL_STOP))