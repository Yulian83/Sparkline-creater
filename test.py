import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
import mplcyberpunk
from scipy.interpolate import make_interp_spline


class Sparkline:
    def __init__(self, y_coord: list, title: str = None) -> None:
        self.__y_coord = np.array(y_coord)
        self.__x_coord = np.array([i for i in range(len(self.__y_coord))])
        self.__title = title



    
    def create(self) -> int:
        try:
            with plt.style.context('cyberpunk'):
                x_dots = self.__x_coord
                y_dots = self.__y_coord         

                x_lines = np.linspace (x_dots.min(), x_dots.max(), 100)
                spl = make_interp_spline(x_dots, y_dots, k = 3)
                y_lines = spl(x_lines)     

                fig = plt.figure()
                ax = fig.add_subplot()    

                if(self.__title != None):
                    ax.set_title(self.__title)
                ax.plot(x_lines, y_lines)
                ax.set_axis_off()
                mplcyberpunk.add_glow_effects(gradient_fill=True)

                plt.savefig('./data/foo.png')
            return 1
        except:
            return 0
    
        
        

sl = Sparkline(y_coord=[1, 0, 1, 0, 1], title="TITLE")

result = sl.create()