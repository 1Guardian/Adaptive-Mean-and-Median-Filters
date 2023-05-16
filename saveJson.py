from imports import *

#================================================================
#
# Function: saveJson(currentJson, newMetaData)
#
# Description: This function simply combines a new json object
#              to an already established unpacked Json dictionary. 
#              this Json dictionary, when fully ready, will be packed
#              and written as a metadata file for images in the 
#              corpus.
#
# Returns: jsonObject | type: Unpacked Json List of Dictionary
#
#================================================================
def saveJson(currentJson, newMetaData):

    #this probably doesn't need it's own function right now, 
    #but since I plan on using this for Json tokenization 
    #down the road, I feel like making the function now is 
    #decent future-proofing

    #just add the new metadata to the old list and return it
    currentJson.append(newMetaData)
    return (currentJson)