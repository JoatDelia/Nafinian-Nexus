import libtcodpy as rl

import boxes as bx

class TitleScene: # As the name suggests, the title screen.
    def refresh(self):
        rl.console_print(0, 7, 2, "#  #  ##  #### ###  #  # ###  ##  #  #     #  # #### #  # #  #  ###\n## # #  # #     #   ## #  #  #  # ## #     ## # #    #  # #  # #\n# ## #### ###   #   # ##  #  #### # ##     # ## ###   ##  #  #  ##\n#  # #  # #     #   #  #  #  #  # #  #     #  # #    #  # #  #    #\n#  # #  # #    ###  #  # ### #  # #  #     #  # #### #  #  ##  ###") # Draw the title.
        testBox = bx.Box(33,17,14,6,None,'{0} New Game\n  Continue\n  Modding\n  Exit'.format(chr(rl.CHAR_ARROW2_E)).encode()) # A test box. Will, of course, be replaced later with something more interactive.
        testBox.draw() # Draws the test box on the screen.
    
    def handleInput(self):
        rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.