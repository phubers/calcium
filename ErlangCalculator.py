'''
Created on 6 mei 2014

Erlang Calculator for Pythonista (on iOS). 
Requires erlang.py (for core functions) and ErlangCalculator.pyui (for UI definitions)

@author: Patrick.Hubers
'''
from erlang import *
import ui
 
# def create_view:
#     view = ui.View()
#     view.name = "Erlang Calculator"
#     view.background_color = "white"

def button_tapped(sender):
	'@type sender: ui.Button'
	v = sender.superview
	calls = int(textfieldVolume.text)
	textfieldVolume.end_editing()
	aht = int(textfieldAHT.text)
	textfieldAHT.end_editing()
	svgoal = float(textfieldSLPercentage.text)/100.0
	textfieldSLPercentage.end_editing()
	waittime = int(textfieldSLWaittime.text)
	textfieldSLWaittime.end_editing()
	agents = AgentsForServiceLevel(calls, aht, 60, waittime, svgoal)
	textfieldAgents.text = '%s' % agents
	 
if __name__ == '__main__':
	v = ui.load_view('ErlangCalculator')
	textfieldVolume = v['textfieldVolume']
	textfieldVolume.keyboard_type = ui.KEYBOARD_NUMBER_PAD
	textfieldAHT = v['textfieldAHT']
	textfieldAHT.keyboard_type = ui.KEYBOARD_NUMBER_PAD
	textfieldSLPercentage = v['textfieldSLPercentage']
	textfieldSLPercentage.keyboard_type = ui.KEYBOARD_NUMBER_PAD
	textfieldSLWaittime = v['textfieldSLWaittime']
	textfieldSLWaittime.keyboard_type = ui.KEYBOARD_NUMBER_PAD
	textfieldAgents = v['textfieldAgents']
	textfieldAgents.enabled = False
	if ui.get_screen_size()[1] >= 768:
		# iPad
		v.present('popover')
	else:
		# iPhone
		v.present(orientations=['portrait'])    
