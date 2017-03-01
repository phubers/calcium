#!python2

'''
Created on 6 mei 2014

Erlang Calculator for Pythonista (on iOS). 
Requires erlang.py (for core functions) and ErlangCalculator.pyui (for UI definitions)

@author: Patrick.Hubers
'''
from erlang import *
from io import BytesIO
import matplotlib.pyplot as plt
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
	workload = Workload(calls, aht, 60)
	textfieldWorkload.text = '%4.2f' % workload
	agents = AgentsForServiceLevel(calls, aht, 60, waittime, svgoal)
	textfieldAgents.text = '%s' % agents
	occupancy = workload / agents
	textfieldOccupancy.text = '%4.2f' % (occupancy * 100)
	
	agent_range = list(range(trunc(ceil(workload)), agents+3))
	plt.clf()
	plt.plot(agent_range, [ServiceLevel(agent, calls, aht, 60, waittime)*100 for agent in agent_range])
	plt.grid(True)
	plt.axis(ymin=0, ymax=100)
	plt.xlabel('Agents')
	plt.ylabel('Service level %')
	plt.xticks(agent_range)
	
	b = BytesIO()
	plt.savefig(b)
	img = ui.Image.from_data(b.getvalue())
	imageviewPlot.image = img
	 
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
	textfieldWorkload = v['textfieldWorkload']
	textfieldWorkload.enabled = False 
	textfieldAgents = v['textfieldAgents']
	textfieldAgents.enabled = False
	textfieldOccupancy = v['textfieldOccupancy']
	textfieldOccupancy.enabled = False
	imageviewPlot = v['plotView']
	imageviewPlot.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
	if ui.get_screen_size()[1] >= 768:
		# iPad
		v.present('popover')
	else:
		# iPhone
		v.present(orientations=['portrait'])    
