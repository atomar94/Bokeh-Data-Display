import numpy as np

from bokeh.client import push_session
from bokeh.driving import repeat, linear
from bokeh.plotting import figure, curdoc
from bokeh.models import Range1d
from bokeh.models.sources import ColumnDataSource
from bokeh.io import hplot, show


class PressureDisplay:
    
    title = "Pressure"
    xaxis_label = "Time"
    yaxis_label = "Pressure"
    points_to_display = 400
    TOOLS = "wheel_zoom,reset"
    minPressure = -3 #what we expect
    maxPressure = 3
    newestPressure = [] #stored as a list so we can add it to ColumnDataSource. else we get errors
    figure = None #gets reassigned in init()    
    gaugefigure = None #this displays the isp and other calculations
    
    def getFigure(self):
        return hplot(self.figure, self.gaugefigure)
    
    def initdatafields(self, mtime, mpressure):
        #the data coming in here is of type ndarray
        try:
            self.newestPressure.append(mpressure[0])
        except IndexError:
            #mpressure wasnt initialized
            self.newestPressure.append(0)
        except ValueError:
            #mpressure wasnt init
            self.newestPressure.append(0)
        
        self.cds = ColumnDataSource(data=dict(time=mtime, pressure=mpressure, gaugereading=self.newestPressure))
        self.dataline = self.figure.line("time", "pressure", source=self.cds)
        self.dataquad = self.gaugefigure.quad(top='gaugereading', bottom=self.minPressure, left=-1, right=1, source=self.cds)
   

    #this function only takes single data points, not arrays
    #TODO: Make this accept arrays
    def updateData(self, mtime, mpressure):
        tempTimeDict = np.append(self.cds.data["time"], mtime) 
        if tempTimeDict.size > self.points_to_display:
            tempTimeDict = np.delete(tempTimeDict, np.arange(start=0, stop=tempTimeDict.size - self.points_to_display))
            
        tempPressureDict = np.append(self.cds.data["pressure"], mpressure)
        if tempPressureDict.size > self.points_to_display:
            tempPressureDict = np.delete(tempPressureDict, np.arange(start=0, stop=tempPressureDict.size - self.points_to_display))
            
        self.dataline.data_source.data['time'] = tempTimeDict
        self.dataline.data_source.data['pressure'] = tempPressureDict
        self.dataquad.data_source.data['gaugereading'] = np.array([mpressure])
        
    def __init__(self):
        self.figure = figure(plot_width=650, plot_height=350, tools=self.TOOLS, title=self.title, x_axis_label=self.xaxis_label,
                       y_axis_label=self.yaxis_label)
        self.gaugefigure = figure(plot_width=150, plot_height=350, tools=self.TOOLS)
        
        self.figure.toolbar_location = None
        self.figure.xgrid.grid_line_color = None

        self.gaugefigure.xgrid.grid_line_color = None
        self.gaugefigure.xaxis.visible = None
        self.gaugefigure.ygrid.grid_line_color = None
        self.gaugefigure.y_range = Range1d(self.minPressure, self.maxPressure)
        self.gaugefigure.toolbar_location = None
        
        self.initdatafields(np.array([]), np.array([])) #init graph with an empty data set
