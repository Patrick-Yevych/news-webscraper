import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category20c
from bokeh.io import save, output_file
from math import pi

class PieChartView():

    df = None
    figure = None
    
    def __init__(self, points: dict, out_file: str):
        output_file(out_file)
        
        if (points == {} or points == None):
            return None

        self.df = pd.Series(points).reset_index(name='value').rename(columns={'index': 'source'})
        self.df['color'] = Category20c[len(points)]
        self.df['angle'] = self.df['value']/self.df['value'].sum() * 2*pi

        self.figure = figure(plot_height=350, title="Number of Articles By Source", toolbar_location=None, tools="hover", tooltips="@source; @value article(s)", x_range=(-0.5, 1.0))
        
        self.figure.wedge(x=0, y=1, radius=0.35,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='source', source=self.df)

        self.figure.axis.axis_label=None
        self.figure.axis.visible=False
        self.figure.grid.grid_line_color=None

        save(self.figure)

if __name__ == '__main__':
    from DatabaseConnection import DatabaseConnection
    db = DatabaseConnection("./config.json")
    pie = PieChartView(db.sources_count('ethereum', 'google'), 'pie_test.html')
    db.destroy()