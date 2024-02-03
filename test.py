import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk
from scipy.interpolate import pchip_interpolate


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

                x_lines = np.linspace(x_dots.min(), x_dots.max(), 100)
                spline_values = self.pchip_interpolation(x_dots, y_dots, x_lines)

                fig = plt.figure()
                ax = fig.add_subplot()    

                if(self.__title != None):
                    ax.set_title(self.__title)
                ax.plot(x_lines, spline_values)
                ax.set_axis_off()
                mplcyberpunk.add_glow_effects(gradient_fill=True)

                plt.savefig('./data/foo.png')
            return 1
        except:
            return 0
    
    @staticmethod
    def pchip_interpolation(x, y, new_x):
        # Ограничиваем новые точки интерполяции в пределах существующих данных
        new_x = np.clip(new_x, min(x), max(x))
        return pchip_interpolate(x, y, new_x)
        
        

sl = Sparkline(y_coord=[1, 0, 1, 0, 1, 2, 3, 4, 5, 0, 5, 6, 7, 8, 8, 8, 10, 12], title="TITLE")

result = sl.create()