import libtcodpy as rl

import _thread as thread

from titlescene import TitleScene

from battlescene import BattleScene

import devscenes

from gameoverscene import GameOverScene

currentScene = TitleScene()

def checkForSceneChange(command): # The return command handling is now in a separate function, because now both main() and refreshDisplay() can issue a command. That said, they being in separate threads, care should be taken that they never issue instructions at the same time.
    global currentScene
    if command == "TitleScene":
        currentScene = TitleScene()
    if command == "BattleScene":
        currentScene = BattleScene(currentScene.getParty(),currentScene.getEnemies())
    if command == "DevMenuScene":
        currentScene = devscenes.DevMenuScene()
    if command == "GameOverScene":
        currentScene = GameOverScene()

def refreshDisplay(): # Handles refreshing the screen.
    rl.console_set_default_foreground(0, rl.white) # Sets the foreground (text) color to white.
    rl.console_set_default_background(0, rl.black) # Sets the background color to black.
    checkForSceneChange(currentScene.refresh())
    rl.console_flush() # Update the console (if this isn't done, the console will always just show a blank white screen).

def main(): # The main function for the game. Individual scenes handle most of the actual game logic.
    rl.console_set_custom_font('terminal8x14_gs_ro.png'.encode(), rl.FONT_TYPE_GREYSCALE | rl.FONT_LAYOUT_ASCII_INROW) # Sets the default font to something less square, making the resulting window look less flat. #8x14 normally
    rl.console_init_root(80, 24, 'Nafinian Nexus'.encode()) # Opens the pseudo-console window.
    rl.sys_set_fps(30) # The program can (and will) TRY to update the screen faster than this, but this will impose a cap on how often it will actually happen.
    rl.console_set_background_flag(0, rl.BKGND_SET)
    while not rl.console_is_window_closed(): # As long as the X icon is not pressed...
        checkForSceneChange(currentScene.handleInput()) # Ask the current scene to handle input for us. In most cases, nothing further needs to be done. However, if a command comes back, we need to change the scene accordingly (invalid commands are ignored).
        refreshDisplay()
        
    
main()