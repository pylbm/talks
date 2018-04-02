import ipywidgets as widgets
from IPython.display import display

class interactive_graph():
    def __init__(self):
        self.wid = []
        self.variables = {}
        self.form_item_layout = widgets.Layout(
            display='flex',
            flex_flow='row',
            justify_content='space-between',
            #border='solid 2px',
            align_items='stretch',
            width='100%'
        )

    def add_parameter(self, dico):
        t = dico.get('type', 'slider')
        if t == 'slider':
            self._add_slider_parameter(dico)
        elif t == 'intslider':
            self._add_intslider_parameter(dico)
        # elif t == 'html':
        #     self._add_html_parameter(dico)
        # elif t == 'rangeslider':
        #     self._add_rangeslider_parameter(dico)
        # elif t == 'checkbox':
        #     self._add_checkbox_parameter(dico)
        # elif t == 'selectmultiple':
        #     self._add_selectmultiple_parameter(dico)
        # elif t == 'dropdown':
        #     self._add_dropdown_parameter(dico)

    def _add_intslider_parameter(self, dico):
        wid_label = widgets.Label(dico['description'])
        wid_slide = widgets.IntSlider(
                        value = dico['value'],
                        min = dico['min'],
                        max = dico['max'],
                        step = dico.get('step', 1),
                        continuous_update = True,
                        orientation = 'horizontal',
                        readout = True,
                        readout_format = 'd',
                        layout= widgets.Layout(width='75%'),#, height='50px'),
        )
        self.wid.append(widgets.Box([wid_label, wid_slide], layout = self.form_item_layout))
        self.variables[dico['variable']] = wid_slide

    def _add_slider_parameter(self, dico):
        wid_label = widgets.Label(dico['description'])
        wid_slide = widgets.FloatSlider(
                        value = dico['value'],
                        min = dico['min'],
                        max = dico['max'],
                        step = dico.get('step', (dico['max']-dico['min'])/100),
                        continuous_update = dico.get('continuous_update', True),
                        orientation = 'horizontal',
                        readout = True,
                        readout_format = '.2f',
                        layout= widgets.Layout(width='75%'),#, height='50px'),
        )
        self.wid.append(widgets.Box([wid_label, wid_slide], layout = self.form_item_layout))
        self.variables[dico['variable']] = wid_slide

    # def _add_html_parameter(self, dico):
    #     wid_label = widgets.Label(dico['description'])
    #     wid_html = widgets.HTMLMath(
    #         value = dico['value'],
    #         #placeholder = 'Some HTML',
    #         #description = None,
    #         continuous_update = dico.get('continuous_update', True),
    #         orientation = 'horizontal',
    #         layout= widgets.Layout(width='75%', border='solid 2px'),
    #     )
    #     self.wid.append(widgets.Box([wid_label, wid_html], layout = self.form_item_layout))
    #     #self.variables[dico['variable']] = wid

    # def _add_rangeslider_parameter(self, dico):
    #     wid_label = widgets.Label(dico['description'])
    #     wid_slide = widgets.FloatRangeSlider(
    #                     value=dico['value'],
    #                     min=dico['min'],
    #                     max=dico['max'],
    #                     step=dico.get('step', (dico['max']-dico['min'])/100),
    #                     disabled=False,
    #                     continuous_update = dico.get('continuous_update', True),
    #                     orientation='horizontal',
    #                     readout=True,
    #                     readout_format=dico.get('readout_format', '.1f'),
    #                     layout= widgets.Layout(width='75%'),
    #     )
    #     self.wid.append(widgets.Box([wid_label, wid_slide], layout = self.form_item_layout))
    #     self.variables[dico['variable']] = wid_slide
    #
    # def _add_selectmultiple_parameter(self, dico):
    #     wid = widgets.SelectMultiple(
    #         options = dico['options'],
    #         value = dico['value'],
    #         rows=len(dico['value']),
    #         description = dico['description'],
    #         disabled=False,
    #     )
    #     n = len(self.wid)
    #     self.wid.append(wid)
    #     self.variables[dico['variable']] = self.wid[n]
    #
    # def _add_dropdown_parameter(self, dico):
    #     wid = widgets.Dropdown(
    #         options = dico['options'],
    #         value = dico['value'],
    #         description = dico['description'],
    #         disabled=False,
    #     )
    #     n = len(self.wid)
    #     self.wid.append(wid)
    #     self.variables[dico['variable']] = self.wid[n]
    #
    # def _add_checkbox_parameter(self, dico):
    #     wid = widgets.Checkbox(
    #             value=dico['value'],
    #             description=dico['description'],
    #             disabled=False,
    #     )
    #     n = len(self.wid)
    #     self.wid.append(wid)
    #     self.variables[dico['variable']] = self.wid[n]

    def build(self, f):
        # self.ui = widgets.Box(self.wid, layout=widgets.Layout(
        #             display='flex',
        #             flex_flow='column',
        #             #border='solid 2px',
        #             align_items='stretch',
        #             width='100%',
        #             #height='300px',
        # ))
        #self.out = widgets.interactive_output(f, self.variables)
        self.wid.append(widgets.interactive_output(f, self.variables))
        self.interactive_plot = widgets.Box(self.wid,
                                            layout=widgets.Layout(display='flex',
                                                                   flex_flow='column',
                                                                   #border='solid 2px',
                                                                   align_items='stretch',
                                                                   width='100%',
                                                                   #height='300px',
                                                                   )
                                             )

    def plot(self):
        display(self.interactive_plot)
