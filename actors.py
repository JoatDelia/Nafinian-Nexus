import libtcodpy as rl

import random

import time

class Actor:
    def __init__(self): # Initialize the character.
        self.stre = 60 # Strength.
        self.end = 60 # Endurance.
        self.dex = 60 # Dexterity.
        self.per = 60 # Perception.
        self.wil = 60 # Willpower.
        self.inte = 60 # Intelligence.
        self.cha = 60 # Charisma.
        self.luk = 60 # Luck.
        self.healFull() # Set HP to the proper number.
        self.name = "CHARNAME" # The name to display.
        self.statusEffects = [] # List of current status effects.
        self.statusIsScrolling = False # Whether the status effects list is scrolling due to insufficient space.
        self.startedScrolling = time.time() # If so, this is when it started.
    
    def receiveStatus(self,newEffect): # Add a new status effect to a character. This should be an array in the form of [string effect name, boolean beneficial, integer duration, integer potency (if N/A, put 0)]
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
    
    def getStr(self): # Get strength.
        returnStat = self.stre
        for effect in self.statusEffects:
            if effect[0] == "Sharpen":
                returnStat += effect[3]
        return returnStat
    
    def setStr(self,x): # Set strength.
        self.stre = min(x,1000) # Set the stat, but enforce the maximum.
    
    def getEnd(self): # Get endurance.
        return self.end
    
    def setEnd(self,x): # Set endurance.
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
    
    def setCha(self,x): # Set strength.
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
    
    def getMod(self,x): # Get the modifier for the specified stat.
        if x <= 5:
            return -15
        return int((x+4)/5)-12
    
    def getLine1(self): # Get first line of combat status.
        return "Use subclass!"
    
    def getOptions(self): # Get the basic options for a party member, or a controlled enemy.
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
        if self.name == "Benjamin" and self.mp >= 3: # Again, this won't be hard-coded by name in the final game, of course.
            moves.append("Fire I")
        if self.name == "Alzoru" and self.mp >= 4: # As before.
            moves.append("Sharpen")
        return moves
    
    def isAI(self): # Whether the character is controlled by the AI.
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
        self.hp -= max(amount,0)
        if self.hp <= 0: # AP is reduced to 0 on KO.
            self.ap = 0
    
    def heal(self,amount): # Raise HP by the given amount. Negative numbers are reduced to 0.
        self.hp += max(amount,0)
        if self.hp > self.getMaxHP(): # Enforce the health cap.
            self.hp = self.getMaxHP()
    
    def attack(self,target): # Attack the specified foe.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getPer()) + int(self.getMod(self.getLuk()) / 2 + 0.5) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex()) + int(target.getMod(self.getLuk()) / 2 + 0.5)
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        damageAmt = max(random.randint(1,6)+random.randint(1,6)+self.getAttackMod()-target.getDefenseMod() + int(self.getMod(self.getLuk()) / 4 + 0.5),0)
        if dodgeRoll == hitRoll:
            damageAmt = int(damageAmt / 2 + 0.5)
        if random.randint(1,12) == 12: # Handle critical hits. This is a flat chance.
            damageAmt *= 2
            message = "{0} critically hits {1} for {2} damage!".format(self.getColoredName(),target.getColoredName(),damageAmt)
        else:
            message = "{0} hits {1} for {2} damage.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt) # ...but for now, it just deals 2d6 damage.
        if target.getHP() <= 0:
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def bite(self,target): # Bite the specified foe.
        self.ap -= 3 # Remove AP for bite. No need to check here - if the character has insufficient AP, Bite shouldn't appear in the first place.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getPer()) + int(self.getMod(self.getLuk()) / 2 + 0.5) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex()) + int(target.getMod(self.getLuk()) / 2 + 0.5)
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        damageAmt = max(random.randint(9,18)+self.getMod(self.getStr())-target.getDefenseMod(),0) # This isn't a weapon attack, so does not include weapon mod. Instead, just simply use Strength.
        if dodgeRoll == hitRoll:
            damageAmt = int(damageAmt / 2 + 0.5)
        if random.randint(1,12) == 12: # Handle critical hits. This is a flat chance.
            damageAmt *= 2
            message = "{0} critically bites {1} for {2} damage!".format(self.getColoredName(),target.getColoredName(),damageAmt)
        else:
            message = "{0} bites {1} for {2} damage.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt) # ...but for now, it just deals 2d6 damage.
        if target.getHP() <= 0:
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def castHealI(self,target): # Cast Heal I on the specified ally.
        if target.hp == target.getMaxHP():
            return {'log': target.getColoredName()+" is already at full health!", 'cancel': None}
        self.mp -= 3 # Remove MP for Heal I. This is a flat 3 for now, since Heal I is a cross-class spell for Gina, but later there would be a check for circumstances like that.
        healAmt = random.randint(1,4) + self.getMod(self.getWil())
        message = "{0} casts Heal I on {1}, restoring {2}HP.".format(self.getColoredName(),target.getColoredName(),healAmt)
        wasUnconscious = target.hp <= 0 # Whether the actor was previously unconscious.
        target.heal(healAmt)
        if target.hp > 0 and wasUnconscious:
            message += " "+target.getColoredName()+" gets back up!"
        return {'log': message} # Return the message to send to the combat log.
    
    def castFireI(self,target): # Cast Fire I the specified foe.
        self.mp -= 3 # Remove MP for Fire I.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) + self.getMod(self.getDex()) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20) + target.getMod(target.getDex())
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} casts Fire I, but misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        damageAmt = max(random.randint(1,6) + self.getMod(self.getInt()) - target.getSpecialDefenseMod(),0)
        message = "{0} casts Fire I on {1} for {2} damage.".format(self.getColoredName(),target.getColoredName(),damageAmt)
        target.damage(damageAmt)
        if target.getHP() <= 0:
            message += " Knockout!"
        if target.isDead() and isinstance(target, Chara): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def castSharpen(self,target): # Cast Sharpen on the specified ally.
        self.mp -= 4 # Remove MP for Heal I. This is a flat 3 for now, since Heal I is a cross-class spell for Gina, but later there would be a check for circumstances like that.
        buffAmount = 5 + random.randint(1,6) + self.getMod(self.getInt())
        message = "{0} casts Sharpen on {1}, increasing STR by {2}.".format(self.getColoredName(),target.getColoredName(),buffAmount)
        target.receiveStatus(["Sharpen",True,5,buffAmount])
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
    
    def isDead(self):
        return self.hp <= 0
    
    def turnStartRegen(self): # Regeneration at the beginning of every turn.
        message = None # Message to display in the log.
        if self.isDead(): # The dead don't regenerate (zombies and stuff aside - you know what I meant).
            return
        if self.getMod(self.getEnd()) >= 0: # Regenerate health, unless Endurance mod is negative.
            wasUnconscious = self.hp <= 0 # Whether the actor was previously unconscious.
            self.hp = min(self.hp + 1 + int(self.getMod(self.getEnd())/5),self.getMaxHP()) # Apply HP regeneration.
            if self.hp > 0 and wasUnconscious:
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
        if self.statusIsScrolling:
            loopedStatusLine = statusLine + ", " + statusLine # A looped version of the status line.
            startingPoint = int((time.time() - self.startedScrolling) * 5) % (len(statusLine) + 2) # Where to start sampling from the looped line.
            return loopedStatusLine[startingPoint:startingPoint + width] # Take a sample from the looped line, making it look like it's scrolling over time.
        return statusLine

class Chara(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(1)+chr(191)+chr(255)+self.name+chr(rl.COLCTRL_STOP)
    
    def isAI(self):
        return False
        
    def isDead(self): # Return whether the party member is dead. Meanwhile, enemies don't have a distinction between "dead" and "unconscious", so their isDead() always returns false.
        return self.hp <= -max(self.getMaxHP(),10)
        
    def getLine1(self): # Return health bar and HP.
        if self.hp > 0:
            return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}HP".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),8),chr(rl.COLCTRL_STOP),self.hp,self.getMaxHP())
        else:
            return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}HP".format(chr(rl.COLCTRL_FORE_RGB),chr(128),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(32),chr(32),chr(32),self.makeBar(max(self.getMaxHP(),10)+self.hp,max(self.getMaxHP(),10),8),chr(rl.COLCTRL_STOP),self.hp,self.getMaxHP())
        
    def getLine2(self): # Return stamina bar and AP.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}AP".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),8),chr(rl.COLCTRL_STOP),self.ap,self.getMaxAP())
        
    def getLine3(self): # Return stamina bar and AP.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}MP".format(chr(rl.COLCTRL_FORE_RGB),chr(1),chr(128),chr(255),chr(rl.COLCTRL_BACK_RGB),chr(1),chr(64),chr(128),self.makeBar(self.mp,self.getMaxMP(),8),chr(rl.COLCTRL_STOP),self.mp,self.getMaxMP())
        

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
        partyMembersUp = []
        enemiesUp = []
        for member in party:
            if member.getHP() > 0:
                partyMembersUp.append(member)
        for member in enemies:
            if member.getHP() > 0:
                enemiesUp.append(member)
        moveNum = random.randint(0,4) # Decide randomly what to do.
        if moveNum == 3 and self.mp >= 4: # If chosen and able to use, do Sharpen.
            return self.castSharpen(random.choice(enemiesUp))
        if moveNum == 2 and self.mp >= 3: # If chosen and able to use, do Fire I.
            return self.castFireI(random.choice(partyMembersUp))
        elif moveNum == 1 and self.ap >= 3: # If chosen and able to use, do a bite.
            return self.bite(random.choice(partyMembersUp))
        return self.attack(random.choice(partyMembersUp)) # If nothing else, just randomly attack.