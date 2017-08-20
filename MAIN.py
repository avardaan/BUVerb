#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Vardaan Aashish
email: vardaan@bu.edu

Purpose: Final Project for CS591
Instructor: Wayne Snyder

Topic: Convolution Reverb with IRs from around BU
"""

# main script (interface)


import buverbs as bu
import tkinter as tk
from PIL import Image, ImageTk



areaOptions = ["BU Central", "CAS 4th Floor Hallway", "CAS 522", "CAS Bathroom", \
                "CAS Elevator", "CAS Lobby", "CAS Stairway", "GSU Conference Auditorium", \
                "Marsh Chapel", "Warren C Tower Laundry"]

soundOptions = ["Acoustic Guitar Note", "Acoustic Guitar Repeated Note", \
                "Acoustic Guitar Riff", "Electric Guitar Note", "Electric Guitar Riff"]



def areaIR(s):
    """ return Wave instance based on string chosen by user"""
    if s == areaOptions[0]:
        return bu.bucentral_dsp
    
    elif s == areaOptions[1]:
        return bu.cas4_dsp
    
    elif s == areaOptions[2]:
        return bu.cas522_dsp
    
    elif s == areaOptions[3]:
        return bu.casbathroom_dsp
    
    elif s == areaOptions[4]:
        return bu.caselevator_dsp
    
    elif s == areaOptions[5]:
        return bu.caslobby_dsp
    
    elif s == areaOptions[6]:
        return bu.casstairs_dsp
    
    elif s == areaOptions[7]:
        return bu.gsuconference_dsp
    
    elif s == areaOptions[8]:
        return bu.marsh_dsp
    
    else: # s == areaOptions[9]:
        return bu.warrenlaundry_dsp
    

def soundIR(s):
    """ return Wave instance based on string chosen by user"""
    if s == soundOptions[0]:
        return bu.aguitarnote_dsp
    
    elif s == soundOptions[1]:
        return bu.repeate_dsp
    
    elif s == soundOptions[2]:
        return bu.aguitarriff_dsp
    
    elif s == soundOptions[3]:
        return bu.eguitarnote_dsp
    
    elif s == soundOptions[4]:
        return bu.eguitarriff_dsp
    
    
    

# final Wave instance that gets written
convolved = [0]
        





root = tk.Tk()

# set some window parameters
root.title = "BUverbs"
root.minsize(width=600, height=600)


# image
pic = Image.open("terrier.jpg")
img = ImageTk.PhotoImage(pic)
terrier = tk.Label(master=root, image=img) # make label with image
terrier.pack(side="top") # place on top



# buverbs title
buv = tk.Label(master=root, text="BUverbs", font=("Arial", 24))
buv.pack(side="top") # place on top below terrier

# buverbs sub title
buvs = tk.Label(master=root, text="BU's custom convolution reverb plugin", font=("Arial", 18))
buvs.pack(side="top") # place on top below terrier

# buverbs sub title
buvs = tk.Label(master=root, text="by Vardaan Aashish", font=("Arial", 18))
buvs.pack(side="top") # place on top below terrier




# SoundMenu
sound = tk.StringVar(master=root)
sound.set("Choose Sound")
chooseSound = tk.OptionMenu(root, sound, *soundOptions)
chooseSound.pack(side="left")

def storeSound():
    # store sound chosen by user
    global soundChosen
    soundChosen = sound.get()
    print("\n\n" + soundChosen)
    return soundChosen


# button to choose?
chooseS = tk.Button(master=root, text="Choose", command=storeSound)
chooseS.pack(side='left')
# update this string with the chosen sound
soundChosen = storeSound()



# AreaMenu
area = tk.StringVar(master=root)
area.set("Choose Reverb Space") # default value
chooseArea = tk.OptionMenu(root, area, *areaOptions)
chooseArea.pack(side="right")

def storeArea():
    # store sound chosen by user
    global areaChosen
    areaChosen = area.get()
    print(areaChosen)
    return areaChosen


# button to choose?
chooseA = tk.Button(master=root, text="Choose", command=storeArea)
chooseA.pack(side='right')
# update this string with the chosen sound
areaChosen = storeArea()



# get Wave instance of sound chosen by user
# sound_dsp = soundIR(soundChosen)

# get Wave instance of area
# area_dsp = areaIR(areaChosen)

#bottom frame for label
btmframe1 = tk.Frame(master=root)
btmframe1.pack(side="bottom")

#bottom frame for buttons
btmframe2 = tk.Frame(master=root)
btmframe2.pack(side="bottom")

def convolve():
    sound_dsp = soundIR(soundChosen)
    area_dsp = areaIR(areaChosen)
    print("Convolving...")
    global convolved
    convolved = sound_dsp.convolve(area_dsp)
    print("Successfully convolved", soundChosen, "and", areaChosen)
    return 

def write():
    s = soundChosen + " in " + areaChosen + ".wav"
    global convolved
    convolved.write(s)
    return

def convolveandwrite():
    convolve()
    write()
    return


# Convolve button
conv = tk.Button(master=btmframe2, text="Convolve & Write!", command=convolveandwrite)
conv.pack(side="bottom")

# write button
#conv = tk.Button(master=btmframe2, text="Write!", command=write)
#conv.pack(side="right")
"""
# bottommost label
done1 = tk.Label(master=btmframe1, text="Convolved!")
done1.pack(side="bottom")

done2 = tk.Label(master=btmframe1, text="Written!")
done2.pack(side="bottom")
"""















root.mainloop()


