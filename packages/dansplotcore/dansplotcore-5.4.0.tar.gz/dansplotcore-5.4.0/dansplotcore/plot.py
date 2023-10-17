from . import primitives
from . import transforms

import datetime
import math

class Plot:
    def __init__(
        self,
        title='plot',
        transform=None,
        hide_axes=False,
        primitive=None,
        datetime_unit=1,
    ):
        self.title = title
        self.points = []
        self.lines = []
        self.rects = []
        self.late_vertexors = []
        self.texts = []
        self.x_min =  math.inf
        self.x_max = -math.inf
        self.y_min =  math.inf
        self.y_max = -math.inf
        self.epochs = {}
        self.series = 0
        self.transform = transform or transforms.Default()
        self.hide_axes = hide_axes
        self.set_primitive(primitive or primitives.Point())
        self.datetime_unit = datetime_unit

    def point(self, x, y, r=255, g=255, b=255, a=255):
        x, y = self._to_screen(x, y)
        self.points.append([x, y, r, g, b, a])
        self._include(x, y)

    def line(self, xi, yi, xf, yf, r=255, g=255, b=255, a=255):
        xi, yi = self._to_screen(xi, yi)
        xf, yf = self._to_screen(xf, yf)
        self.lines.append([xi, yi, xf, yf, r, g, b, a])
        self._include(xi, yi)
        self._include(xf, yf)

    def rect(self, xi, yi, xf, yf, r=255, g=255, b=255, a=255):
        xi, yi = self._to_screen(xi, yi)
        xf, yf = self._to_screen(xf, yf)
        self.rects.append([xi, yi, xf, yf, r, g, b, a])
        self._include(xi, yi)
        self._include(xf, yf)

    def late_vertexor(self, vertexor, x, y, r=255, g=255, b=255, a=255):
        x, y = self._to_screen(x, y)
        self.late_vertexors.append([vertexor, x, y, r, g, b, a])
        self._include(x, y)

    def text(self, s, x, y, r=255, g=255, b=255, a=255, max_w=math.inf, max_h=math.inf, scale=10):
        '`scale` is the number of pixels between the left side of each character.'
        self.texts.append([s, x, y, r, g, b, a, max_w, max_h, scale])
        self._include(x, y)

    def show(self, w=640, h=480):
        from .show import show
        show(self, w, h)

    def plot_list(self, l):
        for i, v in enumerate(l):
            self.primitive(**self.transform(i, v, i, self.series))
        self.next_series()

    def plot_lists(self, ls):
        for l in ls: self.plot_list(l)

    def plot_scatter(self, x, y):
        for i in range(min(len(x), len(y))):
            self.primitive(**self.transform(x[i], y[i], i, self.series))
        self.next_series()

    def plot_scatter_pairs(self, pairs):
        for i, pair in enumerate(pairs):
            self.primitive(**self.transform(pair[0], pair[1], i, self.series))
        self.next_series()

    def plot_scatter_xs(self, xs, y):
        for x in xs: self.plot_scatter(x, y)

    def plot_scatter_ys(self, x, ys):
        for y in ys: self.plot_scatter(x, y)

    def plot_dict(self, d):
        for i, (x, y) in enumerate(d.items()):
            self.primitive(**self.transform(x, y, i, self.series))
        self.next_series()

    def plot_dicts(self, ds):
        for d in ds: self.plot_dict(d)

    def plot_f(self, f, x=(-1, 1), steps=100):
        args_prev = None
        for i in range(steps):
            x_curr = x[0] + (x[1]-x[0]) * i/(steps-1)
            y_curr = f(x_curr)
            self.primitive(**self.transform(x_curr, y_curr, i, self.series))
        self.next_series()

    def plot(self, *args, **kwargs):
        plot_func = None
        if len(args) == 1:
            if   _is_dim(args[0], 1): plot_func = self.plot_list
            elif _is_dim(args[0], 2): plot_func = self.plot_lists
            elif _type_r(args[0], 1) == _type_r([()]): plot_func = self.plot_scatter_pairs
            elif type(args[0]) == dict: plot_func = self.plot_dict
            elif _type_r(args[0]) == _type_r([{}]): plot_func = self.plot_dicts
            elif callable(args[0]): plot_func = self.plot_f
        elif len(args) == 2:
            if   _is_dim(args[0], 1) and _is_dim(args[1], 1): plot_func = self.plot_scatter
            elif _is_dim(args[0], 2) and _is_dim(args[1], 1): plot_func = self.plot_scatter_xs
            elif _is_dim(args[0], 1) and _is_dim(args[1], 2): plot_func = self.plot_scatter_ys
        if not plot_func:
            raise Exception('unknown plot type for argument types {}'.format([_type_r(i) for i in args]))
        plot_func(*args, **kwargs)
        return self

    def next_series(self):
        self.series += 1
        self.primitive.reset()

    def set_primitive(self, primitive):
        self.primitive = primitive.set_plot(self)

    def _include(self, x, y):
        self.x_min = min(x, self.x_min)
        self.x_max = max(x, self.x_max)
        self.y_min = min(y, self.y_min)
        self.y_max = max(y, self.y_max)

    def _to_screen(self, x, y):
        c = [x, y]
        for i, v in enumerate(c):
            if type(v) == datetime.datetime:
                if i not in self.epochs:
                    self.epochs[i] = v
                c[i] = (v - self.epochs[i]).total_seconds() / self.datetime_unit
        return c[0], c[1]

def plot(
    *args,
    title='plot',
    transform=None,
    hide_axes=False,
    primitive=None,
    **kwargs,
):
    Plot(
        title,
        transform,
        hide_axes,
        primitive,
    ).plot(*args, **kwargs).show()

def _type_r(v, max_depth=None, _depth=0):
    if type(v).__name__ in ['int', 'float', 'float64']: return 'number'
    if max_depth != None and _depth == max_depth:
        return str(type(v))
    try:
        v[0]
        return '{}({})'.format(type(v), _type_r(v[0], max_depth, _depth+1))
    except:
        return str(type(v))

def _is_dim(v, dim):
    u = 0
    for i in range(dim): u = [u]
    return _type_r(v, dim) == _type_r(u)
