import libtcodpy as rl

import boxes as bx

import json

import copy

class DevMenuScene: # As the name suggests, the title screen.
    def __init__(self):
        self.box = bx.SelectBox(-1,-1,-1,-1,"Modding Menu",("Edit","Save","Load","Exit"),-1) #("Basic Details","Biomes","Classes","Dialogues","Enemies","Equipment","Feats","Items","Names","Races","Screens","Spells","Save","Load","Exit"),-1) # The main menu box.
        self.currentBox = self.box
        self.boxes = []
        self.defaultMenuObj = ["Edit", "Menu", "", # The entire modding menu and its current values are stored in this array. Each entry in the menu has at least four items, the first four being the label, the type, and the help text, the current value. Some items have a fifth value, representing the max value for numbers, the character limit for text, or the list of options for a multiple-choice selection field. If the fourth entry is another list, then that list represents the new menu to go into. Or, in the case of the "Add" field type, the type of submenu to add to this menu directly above the current item. However, in the case of a selection box, the fourth value is a list of the current values to select from and the fifth is the menu for when creating a new entry. If a menu has a first value of None, that means the value should instead be equal to the value of that menu's first entry.
            [
                ["Input Test", "Menu", "Test various types of input. This will obviously be removed in the final game.",
                    [
                        ["Text Test", "Text", "Test text input.", "HPX!", 20],
                        ["Number Test", "Number", "Test numeric input.", 0, 100],
                        ["Yes/No Test", "Boolean", "Test yes/no input.", "Yes"],
                        ["File Test", "Image", "Test file input (image)", ""],
                        ["Multiple Choice Test", "Select", "Test choosing from multiple options.", "A", ("A","B","C","D","F-")]
                    ]
                ],
                ["Project Properties", "Menu", "Modify various overall aspects of the project itself.",
                    [
                        ["Name", "Text", "The name of this project.", "Project1", 50],
                        ["Title Image", "Image", "The image to show on the title screen. Remember, part of this will be covered by the main menu.", ""],
                        ["Default Game Parameters", "Menu", "Various misc. parameters that affect gameplay in various ways.", 
                            [
                                ["Override battle BGM", "Boolean", "Do not change the music when entering or exiting combat.", "No"],
                                ["Disable random encounters", "Boolean", "With this on, random encounters do not occur. Battles triggered by events still work normally.", "No"],
                                ["Permadeath", "Boolean", "With this on, dead characters are permanently removed from the party. If a character marked as vital, this results in a game over.", "No"],
                                ["Reserve Party EXP %%", "Number", "The percentage of EXP gained by a character in the reserve party.", 0, 100],
                                ["KO'd member EXP %%", "Number", "The percentage of EXP gained by a character who is unconscious at the battle's conclusion.", 100, 100],
                                ["Dead member EXP %%", "Number", "The percentage of EXP gained by a character who is dead at the battle's conclusion. Dead characters won't level up until they are revived.", 0, 100],
                                ["Can modify party anywhere", "Boolean", "If this is false, then the player must rely on an event that explicitly allows changing party members.", "No"],
                                ["Can modify party in combat", "Boolean", "If this is true, any member may be swapped out on their turn with a reserve party member, even if unconscious or dead.", "No"],
                                ["Bring in reserve if party KO'd", "Boolean", "If this is true, full active party defeat will instead trigger party member selection as long as at least one reserve party member is conscious.", "No"],
                                ["Can target reserve members", "Boolean", "If this is true, the player can target reserve members with single-target beneficial effects.", "No"],
                            ]
                        ]
                    ]
                ],
                ["Characters", "Menu", "Modify the list of characters.",
                    [
                        ["New Character", "Add", "Create a new character.",
                            [None, "Menu", "Modify this character.",
                                [
                                    ["Name", "Text", "The character's name.", "Unnamed Chara", 16],
                                    ["Vital", "Boolean", "If reviving this character becomes impossible, the game is over.", "No"],
                                    ["Type", "Select", "Custom characters are customized by the player, generic characters may be put in the party multiple times.", "Normal", ("Normal","Custom","Generic")],
                                    ["Mortality", "Select", "Permadeath means the character cannot be revived, Immortal means they can be knocked out but not killed, Invincible means they cannot be harmed.", "Normal", ("Normal","Permadeath","Immortal","Invincible")],
                                    ["Attributes", "Menu", "These attributes can be anything, but the normal sum is Level*16+490.",
                                        [
                                            ["STRength", "Number", "A measure of muscular power.", 60, 1000],
                                            ["ENDurance", "Number", "A measure of physical resiliency and how far one can push their body.", 60, 1000],
                                            ["DEXterity", "Number", "A measure of general balance, coordination, and agility.", 60, 1000],
                                            ["PERception", "Number", "A measure of ability to notice fine details.", 60, 1000],
                                            ["WILlpower", "Number", "A measure of general force of will.", 60, 1000],
                                            ["INTelligence", "Number", "A measure of ability to remember, reason, and process information.", 60, 1000],
                                            ["CHArisma", "Number", "A measure of skill in social situations.", 60, 1000],
                                            ["LUcK", "Number", "A measure of how fortune leans in dire situations.", 60, 1000],
                                            ["Per Level", "Menu", "Attribute gains per level, in addition to class and race gains. These values are ignored for Custom-type characters.",
                                                [
                                                    ["STRength", "Number", "A measure of muscular power.", 60, 1],
                                                    ["ENDurance", "Number", "A measure of physical resiliency and how far one can push their body.", 60, 1],
                                                    ["DEXterity", "Number", "A measure of general balance, coordination, and agility.", 60, 1],
                                                    ["PERception", "Number", "A measure of ability to notice fine details.", 60, 1],
                                                    ["WILlpower", "Number", "A measure of general force of will.", 60, 1],
                                                    ["INTelligence", "Number", "A measure of ability to remember, reason, and process information.", 60, 1],
                                                    ["CHArisma", "Number", "A measure of skill in social situations.", 60, 1],
                                                    ["LUcK", "Number", "A measure of how fortune leans in dire situations.", 60, 1]
                                                ]
                                            ]
                                        ]
                                    ]
                                ]
                            ],
                        ],
                    ]
                ]
            ]
        ]
        self.menuObj = copy.deepcopy(self.defaultMenuObj)

    def refresh(self):
        rl.console_clear(0) # Fill the window with the background color.
        self.currentBox.draw() # Draws the menu box on the screen.
    
    def handleInput(self):
        key = rl.Key() # Set up the variables for mouse and key input.
        mouse = rl.Mouse()
        rl.sys_check_for_event(rl.EVENT_KEY_PRESS|rl.EVENT_MOUSE,key,mouse) # Update the key and mouse variables if a key or mouse button was pressed.
        # The input handling itself.
        if key.vk == rl.KEY_ENTER or key.vk == rl.KEY_KPENTER or mouse.lbutton_pressed:
            command = None
            if mouse.lbutton_pressed: # If the mouse was clicked, attempt to retrieve a result.
                command = self.currentBox.handleClick(mouse)
            if (key.vk == rl.KEY_ENTER or key.vk == rl.KEY_KPENTER) and command == None: # If a key was pressed and a mouse click did not occur or yield any results:
                command = self.currentBox.forward() # Retrieve the selected option.
            if isinstance(command, list):
                self.boxes.append(self.currentBox)
                self.currentBox = bx.ModdingBox(command)
            elif command == "Exit":
                if len(self.boxes) == 0:
                    return "TitleScene"
                else:
                    self.currentBox = self.boxes.pop()
                return "TitleScene"
            elif command == "Edit":
                self.boxes.append(self.currentBox)
                self.currentBox = bx.ModdingBox(self.menuObj)
            elif command == "Save":
                try:
                    with open('testsave.txt', 'w') as sf:
                        self.boxes.append(self.currentBox)
                        self.currentBox = bx.Box(-1,-1,22,-1,"File Saved","The file was saved successfully.")
                        sf.write(json.dumps(self.menuObj))
                except IOError:
                    self.boxes.append(self.currentBox)
                    self.currentBox = bx.Box(-1,-1,22,-1,"Error!","The file could not be written. It may be in use by another program.")
            elif command == "Load":
                try:
                    with open('testsave.txt', 'r') as sf:
                        self.menuObj = json.loads(sf.read())
                        self.menuObj[0] = "Edit"
                        self.menuObj[1] = "Menu"
                        self.mergeLoadVals(self.menuObj[3],self.defaultMenuObj[3])
                        self.boxes.append(self.currentBox)
                        self.currentBox = bx.Box(-1,-1,22,-1,"File Saved","The file was loaded successfully.")
                except IOError:
                    self.boxes.append(self.currentBox)
                    self.currentBox = bx.Box(-1,-1,22,-1,"Error!","The file could not be written. It may be in use by another program or may not exist.")
                except ValueError:
                    self.boxes.append(self.currentBox)
                    self.currentBox = bx.Box(-1,-1,22,-1,"Error!","The file contains invalid data. It may have become corrupt or was incorrectly modified by an external program.")
            elif command == "CLOSE":
                if len(self.boxes) == 0:
                    return "TitleScene"
                else:
                    self.currentBox = self.boxes.pop()
            return None
        elif key.vk == rl.KEY_DOWN or key.vk == rl.KEY_KP2:
            self.currentBox.goDown() # Go down one item.
            return None
        elif key.vk == rl.KEY_UP or key.vk == rl.KEY_KP8:
            self.currentBox.goUp() # Go up one item.
            return None
        elif key.vk == rl.KEY_ESCAPE or mouse.rbutton_pressed:
            command = self.currentBox.backward()
            if command == "CLOSE":
                if len(self.boxes) == 0:
                    return "TitleScene"
                else:
                    self.currentBox = self.boxes.pop()
        elif key.vk == rl.KEY_F4 and rl.console_is_key_pressed(rl.KEY_ALT):
            raise SystemExit # Exit the program.
            return None
        else: # Let the box handle any other input.
            self.currentBox.miscInput(key)
        return None

    def mergeLoadVals(self,loaded,default): # Checks whether each item in a certain position in the default tree or sub-tree is in the corresponding position in the loaded tree or sub-tree. This is so that mod files from earlier versions, which may lack certain items that later versions have, are brought up to the modern standard. Note that this does not remove "excess" items from later files being edited by earlier versions. In fact, the program will see and allow editing those "excess" items just fine!
        for defaultItem in default: # Look through each current item in the default (sub-)tree.
            itemPresent = False # Becomes true if the corresponding item is found in the loaded (sub-)tree.
            for i,loadedItem in enumerate(loaded): # Look through each current item in the loaded (sub-)tree.
                if not itemPresent and defaultItem[0] == loadedItem[0]: # If a match is found (and don't keep searching if it was already found)...
                    if len(loadedItem) != len(defaultItem) or loadedItem[1] != defaultItem[1]: # This should never happen except from outside tampering, but if the type or length, overwrite the whole entry with the default.
                        loaded[i] = copy.deepcopy(defaultItem)
                    else:
                        if len(defaultItem) > 4 and loadedItem[4] != defaultItem[4]: # If the fifth parameter mismatches, simply correct it.
                            loaded[i][4] = copy.deepcopy(defaultItem[4])
                        loadedItem[2] = defaultItem[2] # Change the loaded description to match the default in case it changed.
                        if defaultItem[1] == "Menu":
                            self.mergeLoadVals(loadedItem[3],defaultItem[3])
                    itemPresent = True # This item has been found.
            if not itemPresent: # If the item isn't present, add it.
                loaded.append(copy.deepcopy(defaultItem))