from bqplot import pyplot as plt
LaTeX = False

traduction_marker = {
    'circle_cross': 'o',
    'o+': 'o',
    'circle_x': 'o',
    'ox': 'o',
    'circle': 'o',
    'square_cross': 's',
    'square_x': 's',
    'square': 's',
    'diamond': 'd',
    'cross': 'p',
    'triangle': '^',
    'inverted_triangle': 'v',
    'asterisk': '*',
}

class Fig():
    """
    Class Fig using bqplot module

    Parameters
    ----------

    x_range : a tuple for min and max value of the x coordinate
    y_range : a tuple for min and max value of the y coordinate
    width : integer, optional (default value is 450)
    height : integer, optional (default value is 300)

    """
    def __init__(self, x_range = (0,0), y_range = None,
                 width=450,
                 height=300,
                 x_label=None, y_label=None,
                 x_axis_type=None, y_axis_type=None):

        self.fig = plt.figure()
        self.

        self.fig, self.ax = plt.subplots(figsize = (int(width/75), int(height/75)))
        self.ax.set_xlim(*x_range)
        if y_range is not None:
            self.ax.set_ylim(*y_range)
        if x_label is not None:
            self.ax.set_xlabel(x_label)
        if y_label is not None:
            self.ax.set_ylabel(y_label)
        self.ax.grid(False)
        if x_axis_type is not None:
            self.ax.set_xscale(x_axis_type)
        if y_axis_type is not None:
            self.ax.set_yscale(y_axis_type)

    def title(self, title_str, title_color = 'black', title_align = 'center'):
        """
        Set the title of the figure

        Parameters
        ----------

        title_str : string that contains the title
        title_color : string, optional
        title_align : string, optional

        """
        self.ax.set_title(title_str, color = title_color, loc = title_align)

    def legend(self, location = None, orientation = None, click_policy = None):
        if location is not None:
            self.ax.legend(loc = location.replace('top', 'upper').replace('bottom', 'lower').replace('_', ' '))
        if orientation is not None:
            pass
        if click_policy is not None:
            pass

    def line(self, x, y, line_width = 2, line_color = 'black', line_alpha = 1, line_marker = None, label = None):
        """
        plot a line

        Parameters
        ----------

        x : numpy array of the x coordinate
        y : numpy array of the y coordinate
        line_width : integer, optional
        color : string, optional

        """
        marker = traduction_marker.get(line_marker, line_marker)
        return line(self.ax, x, y, line_width, line_color, line_alpha, marker, label)

    def scatter(self, x, y, marker = 'circle_x', size = 10, color = 'black', alpha = 0.5, label = None):
        """
        plot scatters

        Parameters
        ----------

        x : numpy array of the x coordinate
        y : numpy array of the y coordinate
        marker : string, optional
        size : integer, optional
        line_width : integer, optional
        color : string, optional

        """
        m = traduction_marker.get(marker, marker)
        return scatter(self.ax, x, y, m, size, color, alpha, label)

    def plot(self):
        pass

    def update(self):
        pass

    def savefig(self, filename):
        if filename is not None:
            plt.savefig(filename)


class line():
    """
    line object
    """
    def __init__(self, ax, x, y, lw, c, alpha, marker, label):
        self.l = ax.plot(x, y, color = c, linewidth = lw, alpha = alpha, marker = marker, label = label)
    def visible(self, b = True):
        plt.setp(self.l, visible = b)
    def update(self, x, y):
        self.l[0].set_data(x, y)
    def line_color(self, color):
        plt.setp(self.l, color = color)

class scatter():
    """
    scatter object
    """
    def __init__(self, fig, x, y, m, s, c, alpha, label):
        self.l = fig.scatter(x, y,
                             marker = m,
                             s = 5*s,
                             edgecolors = 'black',
                             color = c,
                             alpha = alpha,
                             label = label)
    def visible(self, b = True):
        plt.setp(self.l, visible = b)
    def update(self, x, y):
        #self.l.set_offsets(np.array([[x[k], y[k]] for k in range(x.size)]))
        self.l.set_offsets(np.hstack((x[:,np.newaxis], y[:,np.newaxis])))
    def line_color(self, c):
        plt.setp(self.l, edgecolors = c)
    def fill_color(self, c):
        plt.setp(self.l, color = c)
