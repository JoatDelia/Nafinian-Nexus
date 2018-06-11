# This utility is to make it easier to navigate the object tree that functions as both the modding menu and its data. This isn't meant to be used for the modding menu itself, but rather for RUNNING the mod.

class ObjectIndexError(Exception):
    def __init__(self, parent, child):
        pass

def objNavigate(objTree,indexList): # The menu object tree to work with and the list of indeces and sub-indeces to reach the desired value.
    objTree = objTree[3] # Automatically head straight to the contents of the first menu.
    for index in indexList: # For each index and sub-index...
        subList = None # When found, this will change to the sub-list referred to by that index.
        if isinstance(index, int): # If an index NUMBER is specified, that's easy. Just use that.
            subList = objTree[index][3]
        else: # Otherwise, search.
            for i in objTree: # Look through the list tree.
                if index == i[0]: # Check to see if the index is found.
                    subList = i[3] # Set the sub-list to match the found sub-list.
        if subList == None: # If nothing was found, throw an error.
            raise ObjectIndexError(objTree[0],index)
        else:
            objTree = subList
    return objTree # Return the result of the search.