#!/usr/lib/env python

import Tkinter as tk
import ttk
import erlang

def createMainFrame(root):
    mainframe = ttk.Frame(root, padding = '5 5 10 10')
    mainframe.grid()
    return mainframe

def createWidgets(root, mainframe):
    cur_row = 0
    root.volume = tk.StringVar()
    ttk.Label(mainframe, text = 'Volume:', justify = 'left').grid(column = 0, row = cur_row, sticky = "w")
    ttk.Entry(mainframe, textvariable = root.volume, width = 8, justify = 'center').grid(column = 1, row = cur_row)
    ttk.Label(mainframe, text = 'calls/hour', justify = 'left').grid(column = 2, row = cur_row, sticky = "w")

    cur_row += 1
    root.aht = tk.StringVar()
    ttk.Label(mainframe, text = 'AHT:', justify = 'left').grid(column = 0, row = cur_row, sticky = "w")
    ttk.Entry(mainframe, textvariable = root.aht, width = 8, justify = 'center').grid(column = 1, row = cur_row)
    ttk.Label(mainframe, text = 'seconds', justify = 'left').grid(column = 2, row = cur_row, sticky = "w")

    cur_row += 1
    slFrame = ttk.LabelFrame(mainframe, text = 'Service level:', padding = '3 3 8 8')
    slFrame.grid(column = 0, row = cur_row, columnspan = 3)
    root.slPercent = tk.StringVar()
    root.slTime = tk.StringVar()
    ttk.Entry(slFrame, textvariable = root.slPercent, width = 8, justify = 'center').grid(column = 0, row = 1)
    ttk.Label(slFrame, text = '% in').grid(column = 1, row = 1)
    ttk.Entry(slFrame, textvariable = root.slTime, width = 8, justify = 'center').grid(column = 2, row = 1)
    ttk.Label(slFrame, text = 'sec').grid(column = 3, row = 1)

    cur_row += 1
    ttk.Button(mainframe, text = 'Calculate agents', command = calculate).grid(columnspan = 3, row = cur_row)

    cur_row += 1
    root.workload = tk.StringVar()
    ttk.Label(mainframe, text = 'Workload:', justify = 'left').grid(column = 0, row = cur_row, sticky = "w")
    ttk.Entry(mainframe, textvariable = root.workload, width = 8, justify = 'center').grid(column = 1, row = cur_row)
    ttk.Label(mainframe, text = 'Erlang', justify = 'left').grid(column = 2, row = cur_row, sticky = "w")

    cur_row += 1
    root.agents = tk.StringVar()
    ttk.Label(mainframe, text = 'Staffing:', justify = 'left').grid(column = 0, row = cur_row, sticky = "w")
    ttk.Entry(mainframe, textvariable = root.agents, width = 8, justify = 'center').grid(column = 1, row = cur_row)
    ttk.Label(mainframe, text = 'agents', justify = 'left').grid(column = 2, row = cur_row, sticky = "w")

    cur_row += 1
    root.occupancy = tk.StringVar()
    ttk.Label(mainframe, text = 'Occupancy:', justify = 'left').grid(column = 0, row = cur_row, sticky = "w")
    ttk.Entry(mainframe, textvariable = root.occupancy, width = 8, justify = 'center').grid(column = 1, row = cur_row)
    ttk.Label(mainframe, text = '%', justify = 'left').grid(column = 2, row = cur_row, sticky = "w")

def calculate():
    calls = int(root.volume.get())
    aht = int(root.aht.get())
    svgoal = float(root.slPercent.get())/100.0
    waittime = int(root.slTime.get())
    workload = erlang.Workload(calls, aht, 60)
    root.workload.set('%4.2f' % workload)
    agents = erlang.AgentsForServiceLevel(calls, aht, 60, waittime, svgoal)
    root.agents.set('%s' % agents)
    occupancy = workload / agents
    root.occupancy.set('%4.2f' % (occupancy * 100))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Erlang calculator')
    mainframe = createMainFrame(root)
    createWidgets(root, mainframe)
    root.mainloop()

