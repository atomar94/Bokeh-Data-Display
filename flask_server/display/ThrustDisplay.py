# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 19:45:55 2016

@author: alex
"""

import numpy as np

from bokeh.client import push_session
from bokeh.driving import linear
from bokeh.plotting import figure, curdoc
from bokeh.models.sources import ColumnDataSource
from bokeh.io import show
from bokeh.embed import autoload_server, components

class ThrustDisplay:
    
    title = "Thrust"
    xaxis_label = "time"
    yaxis_label = "Thrust"
    points_to_display = 400
    TOOLS = "wheel_zoom,reset"
    figure = None #gets reassigned in init()    
    statsfigure = None #this displays the isp and other calculations
    impulse = 0
    lasttimestamp = 0
            
    #takes 2 ndarrays and inserts a line where they are.
    #you may only call this once unless additional functionality is added
    def initdatafields(self, mtime, thrust):
        self.cds = ColumnDataSource(data=dict(time=mtime, thrust=thrust))
        self.dataline = self.figure.line("time", "thrust", source=self.cds)
        
            
    #pass new ndarray's of the same size. you can put this in the update loop of a main
    def updateData(self, mtime, thrust):
        if mtime.size is not thrust.size:
            print("You must enter data arrays of the same size!")
        
    
        #combine the new and old data in tempTimeDict and remove the oldest
        #data in tempTimeDict2
        tempTimeDict = np.append(self.cds.data["time"], mtime) 
        if tempTimeDict.size > self.points_to_display:
            tempTimeDict = np.delete(tempTimeDict, np.arange(start=0, stop=tempTimeDict.size - self.points_to_display))
            
        tempThrustDict = np.append(self.cds.data["thrust"], thrust)
        if tempThrustDict.size > self.points_to_display:
            tempThrustDict = np.delete(tempThrustDict, np.arange(start=0, stop=tempThrustDict.size - self.points_to_display))
        
        self.dataline.data_source.data["time"] = tempTimeDict
        self.dataline.data_source.data["thrust"] = tempThrustDict
    
    def __init__(self):
        self.figure = figure(plot_width=800, plot_height=400, tools=self.TOOLS,
                             title=self.title, x_axis_label=self.xaxis_label,
                             y_axis_label=self.yaxis_label)
        #removing these makes the graph less jittery
        self.figure.xgrid.grid_line_color = None
        self.figure.toolbar_location = None
        self.figure.min_border_right = 0


thrustdisplay = ThrustDisplay()
x = np.linspace(0, 10, 20)
y = np.random.rand()*10 * x
thrustdisplay.initdatafields(x, y)

@linear(m=1, b=0)
def update(step):
    step = step / 4
    x = np.array(step)
    y = np.random.rand() * 10 * x
    thrustdisplay.updateData(x, y)

    
# open a session to keep our local document in sync with server
session = push_session(curdoc())
curdoc().add_periodic_callback(update, 10)

#currently configured to print a script to the console and thats it
script = autoload_server(thrustdisplay.figure, session_id=session.id)
print(script)
script2, div = components(thrustdisplay.figure)
print(script2)
print(div)
#session.show() # open the document in a browser
#session.loop_until_closed() # run forever'''
        
