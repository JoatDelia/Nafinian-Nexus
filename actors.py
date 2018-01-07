import libtcodpy as rl

import random

class Actor:
    def __init__(self): # Initialize the character.
        self.end = 60 # Endurance.
        self.healFull() # Set HP to the proper number.
        self.name = "CHARNAME" # The name to display.
    
    def setEnd(self,x): # Set endurance.
        oldMaxHP = self.getMaxHP() # Store the old max HP.
        oldMaxAP = self.getMaxAP() # Store the old max AP.
        self.end = min(x,1000) # Set the stat, but enforce the maximum.
        self.hp = max(self.hp + self.getMaxHP() - oldMaxHP, 1) # Adjust HP accordingly.
        self.ap = max(self.ap + self.getMaxAP() - oldMaxAP, 1) # Adjust AP accordingly.
    
    def setName(self,x): # Set character's name.
        self.name = x
    
    def getName(self): # Retrieve character's name.
        return self.name
    
    def healFull(self): # Fill up HP, MP, and AP to full. Remove status effects.
        self.hp = self.getMaxHP() # Fully restore HP.
        self.ap = self.getMaxAP() # Fully restore AP.
        
    def getMaxHP(self): # Calculate and return max HP.
        return max(int(self.end/5) + self.getMod(self.end),1)
        
    def getMaxAP(self): # Calculate and return max AP.
        return max(15 + self.getMod(self.end),1)
    
    def getMod(self,x): # Get the modifier for the specified stat.
        if x <= 5:
            return -15
        return int((x+4)/5)-12
    
    def getLine1(self): # Get first line of combat status.
        return "Use subclass!"
    
    def getOptions(self): # Get the basic options for a party member, or a controlled enemy.
        return ["Attack",]
    
    def getAttackOptions(self): # Get options if Attack is chosen.
        moves = ["Basic",]
        if (self.name == "Gina" or self.name == "Alzoru") and self.ap >= 3: # Later on, this will be determined by race and class. Neither exist yet, though, so...
            moves.append("Bite")
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
    
    def attack(self,target): # Attack the specified foe.
        message = "" # The message to send back to the log.
        hitRoll = random.randint(1,20) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20)
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        damageAmt = random.randint(1,6)+random.randint(1,6)
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
        hitRoll = random.randint(1,20) # These "rolls" correspond to their tabletop equivalent.
        dodgeRoll = random.randint(1,20)
        if dodgeRoll > hitRoll: # Handle misses.
            message = "{0} misses {1}.".format(self.getColoredName(),target.getColoredName())
            return {'log': message}
        damageAmt = random.randint(9,18)
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
    
    def aiAct(self,party): # What the AI does with the character's turn. For now, just attack a random party member.
        return self.attack(random.choice(party))
    
    def getHP(self): # Retrieve current (not max) HP.
        return self.hp
    
    def isDead(self):
        return self.hp <= 0
    
    def turnStartRegen(self): # Regeneration at the beginning of every turn.
        message = None # Message to display in the log.
        if self.isDead(): # The dead don't regenerate (zombies and stuff aside - you know what I meant).
            return
        if self.getMod(self.end) >= 0: # Regenerate health, unless Endurance mod is negative.
            wasUnconscious = self.hp <= 0 # Whether the actor was previously unconscious.
            self.hp = min(self.hp + 1 + int(self.getMod(self.end)/5),self.getMaxHP()) # Apply HP regeneration.
            if self.hp > 0 and wasUnconscious:
                message = self.getColoredName()+" gets back up!"
        if self.getMod(self.end) >= 0 and self.hp > 0: # Regenerate stamina, unless Endurance mod is negative or character is unconscious.
            self.ap = min(self.ap + 1 + int(self.getMod(self.end)/10),self.getMaxAP()) # Apply AP regeneration.
        return message

class Chara(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(1)+chr(191)+chr(255)+self.name+chr(rl.COLCTRL_STOP)
    
    def isAI(self):
        return False
        
    def isDead(self): # Return whether the party member is dead. Meanwhile, enemies don't have a distinction between "dead" and "unconscious", so their isDead() always returns false.
        return self.hp <= -self.getMaxHP()
        
    def getLine1(self): # Return health bar and HP.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}HP".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),8),chr(rl.COLCTRL_STOP),self.hp,self.getMaxHP())
        
    def getLine2(self): # Return stamina bar and AP.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}AP".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),8),chr(rl.COLCTRL_STOP),self.ap,self.getMaxAP())

class Enemy(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(255)+chr(1)+chr(63)+self.name+chr(rl.COLCTRL_STOP)
        
    def getLine1(self): # Return all bars, no numbers.
        returnLine = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),5),chr(rl.COLCTRL_STOP)) # HP bar!
        returnLine += " {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(255),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(128),chr(1),self.makeBar(self.ap,self.getMaxAP(),5),chr(rl.COLCTRL_STOP)) # AP bar!
        # Heart!
        return returnLine # By your powers combined, I am CAPTAIN STATUS!
    
    def aiAct(self,party): # What the AI does with the character's turn. For now, just attack a random party member.
        partyMembersUp = []
        for member in party:
            if member.getHP() > 0:
                partyMembersUp.append(member)
        return self.attack(random.choice(partyMembersUp))