import numpy as np
from . import viewers
from . import pyWiGL

class graphique():
    def __init__(self, scheme, viewer = 'bokeh'):
        self.viewer = viewers.list_viewers.get(viewer, None)
        if self.viewer is None:
            print("Unknown viewer (matplotlib by default)")
            print("The allowed viewers are:")
            for v in viewers.list_viewers.keys():
                print("\t{0}".format(v))
            self.viewer = viewers.list_viewers['matplotlib']
        self.scheme = scheme
        self.g = pyWiGL.interactive_graph()
        for d in self.scheme.p_model:
            self.g.add_parameter(d)
        self._init_graph()

    def _init_graph(self):
        self.scheme.eigenvalues()
        self.fig = self.viewer.Fig(x_range = (-1.1, 1.1),
                                   y_range = (-1.1, 1.1),
                                   x_label = 'real part',
                                   y_label = 'imaginary part',
                                   width=400,
                                   height=400,)
        self.fig.title(self.scheme._name,
                       title_size = 20,
                       title_color = 'black',
                       title_align = 'center')
        self.points = self.fig.scatter(np.real(self.scheme.vvp), np.imag(self.scheme.vvp),
                                       color = 'orange',
                                       marker = 'circle',
                                       size = 5,
                                       alpha = 0.5)
        t = np.linspace(0, 2*np.pi, 1000)
        self.fig.line(np.cos(t), np.sin(t),
                      line_width = 2,
                      line_color = 'navy',
                      line_alpha = 1)

        self.fig.plot()

    def update(self, **args):
        self.scheme.fix_parameters(args)
        self.scheme.compute_eqeq()
        print(self.scheme.eqeq)
        self.scheme.eigenvalues()
        self.points.update(np.real(self.scheme.vvp), np.imag(self.scheme.vvp))
        self.fig.update()

def interactive_plot(scheme, viewer = 'bokeh'):
    graph = graphique(scheme, viewer = viewer)
    graph.g.build(graph.update)
    graph.g.plot()
