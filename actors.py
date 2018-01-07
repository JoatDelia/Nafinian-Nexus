import libtcodpy as rl

import random

class Actor:
    def __init__(self): # Initialize the character.
        self.end = 60 # Endurance.
        self.healFull() # Set HP to the proper number.
        self.name = "CHARNAME" # The name to display.
    
    def setEnd(self,x): # Set endurance.
        oldMaxHP = self.getMod(self.end) # Store the old max HP.
        self.end = min(x,1000) # Set the stat, but enforce the maximum.
        self.hp += max(int(self.end/5) + self.getMod(self.end)) - oldMaxHP # Adjust HP accordingly.
    
    def setName(self,x): # Set character's name.
        self.name = x
    
    def getName(self): # Retrieve character's name.
        return self.name
    
    def healFull(self): # Fill up HP, MP, and AP to full. Remove status effects.
        self.hp = self.getMaxHP() # Fully restore HP.
        
    def getMaxHP(self): # Calculate and return max HP.
        return max(int(self.end/5) + self.getMod(self.end),1)
    
    def getMod(self,x): # Get the modifier for the specified stat.
        if x <= 5:
            return -15
        return int((x+4)/5)-12
    
    def getLine1(self): # Get first line of combat status.
        return "Use subclass!"
    
    def getOptions(self): # Get the basic options for a party member, or a controlled enemy.
        return ["Attack",]
    
    def getAttackOptions(self): # Get options if Attack is chosen.
        return ["Basic",]
    
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
    
    def attack(self,target): # Attack the specified foe. Later on, of course, this will be more complex...
        target.damage(1) # ...but for now, it just deals a flat 1 damage.
        message = self.getColoredName()+" hits "+target.getColoredName()+" for 1 damage."
        if target.getHP() <= 0:
            message += " Knockout!"
        if target.isDead(): # This should only ever show for party members.
            message += " Fatal blow..."
        return {'log': message, 'target': target} # Return the message to send to the combat log.
    
    def aiAct(self,party): # What the AI does with the character's turn. For now, just attack a random party member.
        return self.attack(random.choice(party))
    
    def getHP(self): # Retrieve current (not max) HP.
        return self.hp
    
    def isDead(self):
        return False

class Chara(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(1)+chr(191)+chr(255)+self.name+chr(rl.COLCTRL_STOP)
    
    def isAI(self):
        return False
        
    def isDead(self): # Return whether the party member is dead. Meanwhile, enemies don't have a distinction between "dead" and "unconscious", so their isDead() always returns false.
        return self.hp <= -self.getMaxHP()
        
    def getLine1(self): # Return health bar and HP.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9} {10:>3}/{11:>3}HP".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),8),chr(rl.COLCTRL_STOP),self.hp,self.getMaxHP())

class Enemy(Actor):
    def getColoredName(self):
        return chr(rl.COLCTRL_FORE_RGB)+chr(255)+chr(1)+chr(63)+self.name+chr(rl.COLCTRL_STOP)
        
    def getLine1(self): # Return all bars, no numbers.
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}".format(chr(rl.COLCTRL_FORE_RGB),chr(255),chr(1),chr(1),chr(rl.COLCTRL_BACK_RGB),chr(128),chr(1),chr(1),self.makeBar(self.hp,self.getMaxHP(),5),chr(rl.COLCTRL_STOP),self.hp,self.getMaxHP())
    
    def aiAct(self,party): # What the AI does with the character's turn. For now, just attack a random party member.
        partyMembersUp = []
        for member in party:
            if member.getHP() > 0:
                partyMembersUp.append(member)
        return self.attack(random.choice(partyMembersUp))