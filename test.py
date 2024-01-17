import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
import mplcyberpunk
from scipy.interpolate import make_interp_spline


class Graph:
    title: str

    def __init__(self) -> None:
        pass









class Sparkline(Graph):
    def __init__(self, y_coord: list, title: str = None) -> None:
        self.y_coord = np.array(y_coord)
        self.x_coord = np.array([i for i in range(len(self.y_coord))])
        self.title = title


    
    def create(self):
        with plt.style.context('cyberpunk'):
            x_dots = self.x_coord
            y_dots = self.y_coord         

            x_lines = np.linspace (x_dots.min(), x_dots.max(), 100)
            spl = make_interp_spline(x_dots, y_dots, k = 2)
            y_lines = spl(x_lines)     

            fig = plt.figure()
            ax = fig.add_subplot()    

            ax.plot(x_lines, y_lines)
            ax.set_axis_off()
            mplcyberpunk.add_glow_effects(gradient_fill=True)
            plt.savefig('foo.png')
            plt.show()
    
        
        

sl = Sparkline(y_coord=[3, 0, 5, 0, 7, 3, 2])

sl.create()