import libtcodpy as rl

import boxes as bx

def main():
    rl.console_set_custom_font('terminal8x14_gs_ro.png'.encode(), rl.FONT_TYPE_GREYSCALE | rl.FONT_LAYOUT_ASCII_INROW) # Sets the default font to something less square, making the resulting window look less flat. #8x14 normally
    rl.console_init_root(80, 24, 'Nafinian Nexus'.encode()) # Opens the pseudo-console window.
    rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
    rl.console_set_default_background(0, rl.black) # Sets the background color to black.
    while not rl.console_is_window_closed(): # As long as the X icon is not pressed...
        rl.console_clear(0) # Fill the window the background color.
        rl.console_print(0, 7, 2, "#  #  ##  #### ###  #  # ###  ##  #  #     #  # #### #  # #  #  ###\n## # #  # #     #   ## #  #  #  # ## #     ## # #    #  # #  # #\n# ## #### ###   #   # ##  #  #### # ##     # ## ###   ##  #  #  ##\n#  # #  # #     #   #  #  #  #  # #  #     #  # #    #  # #  #    #\n#  # #  # #    ###  #  # ### #  # #  #     #  # #### #  #  ##  ###") # Draw the title.
        testBox = bx.Box(33,17,14,5,None,'{0} New Game\n  Continue\n  Modding'.format(chr(rl.CHAR_ARROW2_E)).encode()) # A test box. Will, of course, be replaced later with something more interactive.
        testBox.draw() # Draws the test box on the screen.
        rl.console_flush() # Update the console (if this isn't done, the console will always just show a blank white screen).
        rl.console_wait_for_keypress(True) # Halt until a key is pressed. Do nothing withthe key press in this case.
    
main()