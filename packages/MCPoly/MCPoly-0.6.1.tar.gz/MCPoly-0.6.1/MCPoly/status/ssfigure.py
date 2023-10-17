import sys
import os
import re
import ipywidgets as widgets

mydir = os.path.dirname( __file__ )
statusdir = os.path.join(mydir, '..', 'status')
sys.path.append(statusdir)
from status import status

def ssfigure():
    """
        A method to create a visualised manipulation to see the geometry structure of different external force.
        ssfigure()
        You will know how to do as long as you get into the GUI platform.
    """
    ssfigureoutput = widgets.Output()
    
    def ssfigureshow(poly, loc):
        options = []
        for path in os.listdir(loc):
            if os.path.isfile(os.path.join(loc, path)):
                a = re.search('.xyz', path)
                if a:
                    b = re.search(poly, path)
                    if b and '_trj' not in path:
                        options.append(path[-9:-4])
        options.sort()
        scroll.options = options
    
    def ssfigurescroll(loc, scroll):
        ssfigureoutput.clear_output()
        a = status(file=poly.value+'_'+scroll, loc=loc)
        num = a.steps()
        with ssfigureoutput:
            if poly == '':
                pass
            else:
                try:
                    a.figure(num)
                except:
                    a.figure(-1)
    
    def changecombo(loc):
        options2 = []
        for path in os.listdir(loc):
            if os.path.isfile(os.path.join(loc, path)):
                a = re.search('.xyz', path)
                if a and '_trj' not in path and path[:-10] not in options2:
                    options2.append(path[:-10])
        options2.sort()
        poly.options = options2
    
    poly = widgets.Combobox(value='', description='Polymer:')
    loc = widgets.Text(value='./', description='Location:')
    scroll = widgets.SelectionSlider(options=['Enter your polymer', '0.000'], value='0.000',\
                                     description='Force:')    
    
    changecomboout = widgets.interactive_output(changecombo, {'loc': loc})
    ssfigureout = widgets.interactive_output(ssfigureshow, {'poly': poly, 'loc': loc})
    ssfigureout2 = widgets.interactive_output(ssfigurescroll, {'scroll': scroll, 'loc': loc})
    display(widgets.VBox([loc, poly, scroll, ssfigureoutput]))