import requests
import pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():
#    if request.method == 'POST':
        app.vars['ticker'] = request.form['ticker']
        
        url = 'https://finnhub.io/api/v1/stock/candle?symbol=%s&resolution=1&from=1590969600&to=1593561600&token=btjvvjf48v6vivbo1eag' %app.vars['ticker']
        r = requests.get(url)

        a = r.json()
        df = pandas.DataFrame(a, columns=['t','c','h','l','o'])

        df['t'] = pandas.to_datetime(df['t'], unit='s')
        t = df['t']
        c = df['c']
        h = df['h']
        l = df['l']
        o = df['o']

        # select the tools we want
        TOOLS="pan,wheel_zoom,box_zoom,reset,save"

        p = figure(title='Stock prices for %s' % app.vars['ticker'],
            x_axis_label='date',
            x_axis_type='datetime')

        # build our figures
        if request.form.get('c'):
            p.line(x=t, y=c,line_width=2, legend='Close')
        if request.form.get('h'):
            p.line(x=t, y=h,line_width=2, legend='Close')
        if request.form.get('l'):
            p.line(x=t, y=l,line_width=2, legend='Close')
        if request.form.get('o'):
            p.line(x=t, y=o,line_width=2, legend='Close')


        # plots can be a single Bokeh Model, a list/tuple, or even a dictionary
        script, div = components(p)
        return render_template('graph.html', script=script, div=div)
 

if __name__ == '__main__':
    app.run(port=33507)