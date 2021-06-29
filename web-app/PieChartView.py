import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Turbo256
from bokeh.io import show, output_file
from math import pi
from DatabaseConnection import DatabaseConnection

class PieChartView():

    df = None
    figure = None
    
    def __init__(self, points: dict, out_file: str):
        output_file(out_file)

        self.df = pd.Series(points).reset_index(name='value').rename(columns={'index': 'source'})
        self.df['color'] = Turbo256[len(points)]
        self.df['angle'] = self.df['value']/self.df['value'].sum() * 2*pi

        self.figure = figure(plot_height=350, title="Sources", toolbar_location=None, tools="hover", tooltips="@source @num_posts", x_range=(-0.5, 1.0))
        
        self.figure.wedge(x=0, y=1, radius=0.4,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='source', source=self.df)

        self.figure.axis.axis_label=None
        self.figure.axis.visible=False
        self.figure.grid.grid_line_color=None

        show(self.figure)

if __name__ == '__main__':
    db = DatabaseConnection("./config.json")
    pie = PieChartView(db.sources_count('bitcoin', 'google'), 'pie_test.html')
    db.destroy()