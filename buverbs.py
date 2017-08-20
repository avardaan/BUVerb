#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Vardaan Aashish
email: vardaan@bu.edu

Purpose: Final Project for CS591
Instructor: Wayne Snyder

Topic: Convolution Reverb with IRs from around BU
"""

# all the sound files in all formats

import custom as f
import cs591Utilities as cs
# from PIL import Image




# read all available reverbs as Wave class instances
bucentral_dsp = f.read('Reverbs/bucentral.wav')
cas4_dsp = f.read('Reverbs/cas4thfloor.wav')
cas522_dsp = f.read('Reverbs/cas522.wav')
casbathroom_dsp = f.read('Reverbs/casbathroom.wav')
caselevator_dsp = f.read('Reverbs/caselevator.wav')
caslobby_dsp = f.read('Reverbs/caslobby.wav')
casstairs_dsp = f.read('Reverbs/casstairway.wav')
gsuconference_dsp = f.read('Reverbs/gsuconferenceauditorium.wav')
marsh_dsp = f.read('Reverbs/marshchapel.wav')
warrenlaundry_dsp = f.read('Reverbs/warrenlaundry.wav')

areaDSP = [bucentral_dsp, cas4_dsp, cas522_dsp, casbathroom_dsp, caselevator_dsp,\
           caslobby_dsp, casstairs_dsp, gsuconference_dsp, marsh_dsp,\
           warrenlaundry_dsp]




# read all available reverbs as ndarrays
bucentral_cs = cs.readWaveFile('Reverbs/bucentral.wav')
cas4_cs = cs.readWaveFile('Reverbs/cas4thfloor.wav')
cas522_cs = cs.readWaveFile('Reverbs/cas522.wav')
casbathroom_cs = cs.readWaveFile('Reverbs/casbathroom.wav')
caselevator_cs = cs.readWaveFile('Reverbs/caselevator.wav')
caslobby_cs = cs.readWaveFile('Reverbs/caslobby.wav')
casstairs_cs = cs.readWaveFile('Reverbs/casstairway.wav')
gsuconference_cs = cs.readWaveFile('Reverbs/gsuconferenceauditorium.wav')
marsh_cs = cs.readWaveFile('Reverbs/marshchapel.wav')
warrenlaundry_cs = cs.readWaveFile('Reverbs/warrenlaundry.wav')

areaCS = [bucentral_cs, cas4_cs, cas522_cs, casbathroom_cs, caselevator_cs,\
           caslobby_cs, casstairs_cs, gsuconference_cs, marsh_cs,\
           warrenlaundry_cs]



# read sounds as Wave class instances
aguitarnote_dsp = f.read('Sounds/logicguitarnote.wav')
aguitarriff_dsp = f.read('Sounds/logicguitarriff.wav')
repeate_dsp = f.read('Sounds/guitarrepeatE.wav')
eguitarnote_dsp = f.read('Sounds/electricnote.wav')
eguitarriff_dsp = f.read('Sounds/electricriff.wav')

soundCS = [aguitarnote_dsp, aguitarriff_dsp, repeate_dsp,\
           eguitarnote_dsp, eguitarriff_dsp]





areaOptions = ["BU Central", "CAS 4th Floor Hallway", "CAS 522", "CAS Bathroom", \
                "CAS Elevator", "CAS Lobby", "CAS Stairway", "GSU Conference Auditorium", \
                "Marsh Chapel", "Warren C Tower Laundry"]
"""
picsArray = [Image.open('Pics/1.jpeg'), Image.open('Pics/2.jpeg'), Image.open('Pics/3.jpeg'), \
             Image.open('Pics/4.jpeg'), Image.open('Pics/5.jpeg'), Image.open('Pics/6.jpeg'), \
             Image.open('Pics/7.jpeg'), Image.open('Pics/8.jpeg'), Image.open('Pics/9.jpeg'), \
             Image.open('Pics/10.jpeg')]
"""

def printgraph():
    
    for s in range(len(areaCS)):
        cs.displaySignal(areaCS[s], title=areaOptions[s])
        print("\n\n\n")
    return

printgraph()


"""
def showImages():
    for s in range(len(picsArray)):
        picsArray[s].show()
    return
"""




















