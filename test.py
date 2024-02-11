import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk
from typing import Literal
from scipy.interpolate import pchip_interpolate


class Sparkline:
    __style_choices = {'cyberpunk': 'cyberpunk',
                       'Solarize_Light2': 'Solarize_Light2',
                       'dark_background': 'dark_background',
                       'pitayasmoothie-dark': 'data/pitayasmoothie-dark.mplstyle',
                       'pitayasmoothie-light': 'data/pitayasmoothie-light.mplstyle'
                       }

    def __init__(self, 
                 y_coord: list[int | float], 
                 title = None, 
                 style: Literal['cyberpunk', 'Solarize_Light2', 'dark_background',
                                'pitayasmoothie-dark', 'pitayasmoothie-light'] ='cyberpunk'
                 ) -> None:

        self.verify_y_coord(y_coord)
        self.verify_style(style)

        self.__y_coord = np.array(y_coord)
        self.__x_coord = np.array([i for i in range(len(self.__y_coord))])
        self.__style = style
        self.title = title

    def create(self) -> int:
        plt.style.use(self.__style_choices[self.__style])
        plt.rcParams['font.sans-serif'] = ['Arial'] 
        
        fig = plt.figure(figsize=(9, 3))
        ax = fig.add_subplot() 
            
        x_dots = self.__x_coord
        y_dots = self.__y_coord     

        x_lines = np.linspace(x_dots.min(), x_dots.max(), 100)
        spline_values = self.pchip_interpolation(x_dots, y_dots, x_lines)

        if(self.title != None):
            ax.set_title(self.title)
      
        if(self.__style == 'cyberpunk'):
            ax.plot(x_lines, spline_values)
            mplcyberpunk.add_glow_effects(ax=ax,gradient_fill=True)
        elif(self.__style == 'dark_background'):
            ax.plot(x_lines, spline_values, 'red')
            plt.fill_between(x_lines, spline_values, color='red', alpha=0.3)
        else:
            ax.plot(x_lines, spline_values)
            plt.fill_between(x_lines, spline_values, alpha=0.3)

        ax.set_axis_off()
        plt.savefig('./data/sparkline.png')
        return 1
    
    @classmethod
    def verify_style(cls, style: Literal['cyberpunk', 'Solarize_Light2', 'dark_background',
                                         'pitayasmoothie-dark', 'pitayasmoothie-light'] ='cyberpunk') -> None:
        
        if not style in cls.__style_choices.keys():
            raise ValueError(f'style must be one of {cls.__style_choices.keys()}')       
        
    @classmethod
    def verify_y_coord(cls, y_coord: list[int | float]) -> None:
        if(type(y_coord) != list):
            raise ValueError('the y_coordinate field must be a list[int | float]')    
        if len(y_coord) <= 1:
            raise ValueError('there must be more than 1 value in y_coord')    
        for coord in y_coord:
            if not (type(coord) is int or type(coord) is float):
                raise ValueError('the y_coord field only accepts float and int types')     

    @staticmethod
    def pchip_interpolation(x, y, new_x) :
        """This method makes the graph smooth"""
        new_x = np.clip(new_x, min(x), max(x))
        return pchip_interpolate(x, y, new_x)
    
    @property
    def style(self):
        return self.__style
    
    @property
    def y_coord(self):
        return self.y_coord
    
    @style.setter
    def style(self, style: Literal['cyberpunk', 'Solarize_Light2', 'dark_background',
                                   'pitayasmoothie-dark', 'pitayasmoothie-light'] ='cyberpunk') -> None:
        self.verify_style(style)
        self.__style = style     

    @y_coord.setter
    def y_coord(self, y_coord: list[int | float]) -> None:
        self.verify_y_coord(y_coord)
        self.__y_coord = np.array(y_coord)
        self.__x_coord = np.array([i for i in range(len(self.__y_coord))])
        
