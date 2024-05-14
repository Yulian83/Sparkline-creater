from matplotlib import pyplot
from flask import Flask, request, send_file, jsonify
import numpy
import mplcyberpunk
from typing import Literal
from scipy.interpolate import pchip_interpolate
from tempfile import NamedTemporaryFile

app = Flask(__name__)

class Sparkline:
    __style_choices = {'cyberpunk': 'cyberpunk',
                       'Solarize_Light2': 'Solarize_Light2',
                       'dark_background': 'dark_background',
                       'pitayasmoothie-dark': 'data/pitayasmoothie-dark.mplstyle',
                       'pitayasmoothie-light': 'data/pitayasmoothie-light.mplstyle'
                       }

    def __init__(self,
                 y_coord: list[int | float],
                 title: str = 'None',
                 style: Literal['cyberpunk', 'Solarize_Light2',
                                'dark_background',
                                'pitayasmoothie-dark',
                                'pitayasmoothie-light'] = 'cyberpunk'
                 ) -> None:

        self.y_coord = y_coord
        self.style = style
        self.__title = str(title)

    def create(self, file_path: str) -> int:
        if not type(file_path) is str:
            raise TypeError('The "style" variable should be str')

        pyplot.style.use(self.__style_choices[self.__style])
        pyplot.rcParams['font.sans-serif'] = ['Arial']

        fig = pyplot.figure(figsize=(9, 3))
        ax = fig.add_subplot()

        x_dots = numpy.array([i for i in range(len(self.__y_coord))])
        y_dots = numpy.array(self.__y_coord)

        x_lines = numpy.linspace(x_dots.min(), x_dots.max(), 100)

        spline_values = self.pchip_interpolation(x_dots, y_dots, x_lines)
        # pyplot.ylim(0, 100)

        if (self.title != 'None'):
            ax.set_title(self.title)

        if (self.__style == 'cyberpunk'):
            ax.plot(x_lines, spline_values)
            mplcyberpunk.add_glow_effects(ax=ax, gradient_fill=True)
        elif (self.__style == 'dark_background'):
            ax.plot(x_lines, spline_values, 'red')
            pyplot.fill_between(x_lines, spline_values, color='red', alpha=0.3)
        else:
            ax.plot(x_lines, spline_values)
            pyplot.fill_between(x_lines, spline_values, alpha=0.3)

        ax.set_axis_off()
        pyplot.savefig(file_path)
        return 1

    @classmethod
    def verify_style(cls, style: str) -> None:
        if type(style) is not str:
            raise TypeError('The "style" variable should be str')
        if style not in cls.__style_choices.keys():
            raise ValueError(f'style must be one of {cls.__style_choices.keys()}')

    @classmethod
    def verify_coord(cls, coord: list[int | float]) -> None:
        if type(coord) is not list:
            raise TypeError('the y_coordinate field must be a list[int | float]')
        if len(coord) <= 1:
            raise ValueError('there must be more than 1 value in y_coord')
        for dot in coord:
            if not (type(dot) is int or type(dot) is float):
                raise ValueError('the y_coord field only accepts float and int types')

    @staticmethod
    def pchip_interpolation(x, y, new_x):
        """This method makes the graph smooth"""
        new_x = numpy.clip(new_x, min(x), max(x))
        return pchip_interpolate(x, y, new_x)

    @property
    def style(self) -> str:
        return self.__style

    @style.setter
    def style(self, style: Literal['cyberpunk', 'Solarize_Light2',
                                   'dark_background',
                                   'pitayasmoothie-dark',
                                   'pitayasmoothie-light'] = 'cyberpunk'
              ) -> None:
        self.verify_style(style)
        self.__style = style

    @property
    def y_coord(self) -> list[int | float]:
        return self.__y_coord

    @y_coord.setter
    def y_coord(self, y_coord: list[int | float]) -> None:
        self.verify_coord(y_coord)
        self.__y_coord = y_coord

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = str(title)


@app.route('/')
def home():
    return 'Hello World'


@app.route('/sparkline', methods=['POST'])
def sparkline():
    data = request.get_json()
    y_coord = data.get('y_coord')
    title = data.get('title', 'None')
    style = data.get('style', 'cyberpunk')

    if not y_coord:
        return jsonify({"error": "y_coord is required"}), 400

    sparkline = Sparkline(y_coord=y_coord, title=title, style=style)

    with NamedTemporaryFile(delete=True, suffix='.png') as temp_file:
        sparkline.create(temp_file.name)
        temp_file.seek(0)
        return send_file(temp_file.name, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
