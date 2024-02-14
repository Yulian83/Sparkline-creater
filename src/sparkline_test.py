import unittest
import numpy
from sparkline import Sparkline


class Sparkline_test(unittest.TestCase):

    def setUp(self):
        self.sparkline1 = Sparkline(y_coord=[1, 2, 3, 2, 1])
        self.sparkline2 = Sparkline(y_coord=[1, 1, 2, 1, 3], title='TITLE', style='pitayasmoothie-dark')

    def test_init(self):
        sl_1 = Sparkline(y_coord=[1, 2, 3, 2, 1])
        self.assertEqual(sl_1.y_coord, [1, 2, 3, 2, 1])
        self.assertEqual(sl_1.title, 'None')
        self.assertEqual(sl_1.style, 'cyberpunk')


        sl_2 = Sparkline(y_coord=[1, 2, 3, 2, 1], title = [1, 2, 3])
        self.assertEqual(sl_2.y_coord, [1, 2, 3, 2, 1])
        self.assertEqual(sl_2.title, '[1, 2, 3]')
        self.assertEqual(sl_1.style, 'cyberpunk')


        sl_3 = Sparkline(y_coord=[1, 2, 3, 2, 1], title = 'True', style='pitayasmoothie-light')
        self.assertEqual(sl_3.y_coord, [1, 2, 3, 2, 1])
        self.assertEqual(sl_3.title, 'True')
        self.assertEqual(sl_3.style, 'pitayasmoothie-light')

        with self.assertRaises(ValueError):
            Sparkline(y_coord=[1])

        with self.assertRaises(TypeError):
            Sparkline(y_coord='1w,kd')

        with self.assertRaises(ValueError):
            Sparkline(y_coord=[1, 2, 3], style='wjk1jwknjdwwd')

        with self.assertRaises(TypeError):
            Sparkline(y_coord=[1, 2, 3], style=[122, 122])


    def test_pchip_interpolation(self):
        a = '''[1.         1.04040404 1.08080808 1.12121212 1.16161616 1.2020202
 1.24242424 1.28282828 1.32323232 1.36363636 1.4040404  1.44444444
 1.48484848 1.52525253 1.56565657 1.60606061 1.64646465 1.68686869
 1.72727273 1.76767677 1.80808081 1.84848485 1.88888889 1.92929293
 1.96969697 2.01020201 2.05292698 2.09842224 2.14629202 2.19614057
 2.24757214 2.30019097 2.35360131 2.40740741 2.4612135  2.51462384
 2.56724267 2.61867424 2.6685228  2.71639258 2.76188783 2.8046128
 2.84417174 2.8801689  2.9122085  2.93989482 2.96283208 2.98062453
 2.99287642 2.999192   2.999192   2.99287642 2.98062453 2.96283208
 2.93989482 2.9122085  2.8801689  2.84417174 2.8046128  2.76188783
 2.71639258 2.6685228  2.61867424 2.56724267 2.51462384 2.4612135
 2.40740741 2.35360131 2.30019097 2.24757214 2.19614057 2.14629202
 2.09842224 2.05292698 2.01020201 1.96969697 1.92929293 1.88888889
 1.84848485 1.80808081 1.76767677 1.72727273 1.68686869 1.64646465
 1.60606061 1.56565657 1.52525253 1.48484848 1.44444444 1.4040404
 1.36363636 1.32323232 1.28282828 1.24242424 1.2020202  1.16161616
 1.12121212 1.08080808 1.04040404 1.        ]'''
        x_dots = numpy.array([i for i in range(len(self.sparkline1.y_coord))])
        y_dots = numpy.array(self.sparkline1.y_coord)
        x_lines = numpy.linspace(x_dots.min(), x_dots.max(), 100)
        spline_values = Sparkline.pchip_interpolation(x=x_dots, y=y_dots, new_x=x_lines)
        self.assertEqual(a, str(spline_values))

    def test_get_style(self):
        self.assertEqual(self.sparkline1.style, 'cyberpunk')
        self.assertEqual(self.sparkline2.style, 'pitayasmoothie-dark')

    def test_get_y_coord(self):
        self.assertEqual(self.sparkline1.y_coord, [1, 2, 3, 2, 1])
        self.assertEqual(self.sparkline2.y_coord, [1, 1, 2, 1, 3])

    def test_set_style(self):
        self.sparkline1.style = 'pitayasmoothie-dark'
        self.sparkline2.style = 'cyberpunk'
        self.assertEqual(self.sparkline1.style, 'pitayasmoothie-dark')
        self.assertEqual(self.sparkline2.style, 'cyberpunk')

    def test_set_y_coord(self):
        self.sparkline1.y_coord = [1, 1, 2, 1, 3]
        self.sparkline2.y_coord = [1, 2, 3, 2, 1]
        self.assertEqual(self.sparkline1.y_coord, [1, 1, 2, 1, 3])
        self.assertEqual(self.sparkline2.y_coord, [1, 2, 3, 2, 1])
        
    def test_create(self):
        self.assertEqual(self.sparkline1.create('./data/test1'), 1)
        self.assertEqual(self.sparkline2.create('./data/test2'), 1)

        with self.assertRaises(TypeError):
            self.sparkline1.create(1231)

        
if __name__ ==  '__main__':
    unittest.main(verbosity=2)