import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure
import sqlite3
from threading import Thread
import insert_random_DHT_data

logger = Thread(target=insert_random_DHT_data.run)
logger.start()

conn=sqlite3.connect('database.db', check_same_thread=False)
curs=conn.cursor()

app = Flask(__name__)

def getHistData (numSamples):
	curs.execute("SELECT * FROM dhtReadings ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
	return dates, temps, hums

def plotTemp():
    times, temps, hums = getHistData(4)
    # Generate the figure **without using pyplot**.
    print("times :",times)
    ys = temps
    xs = times
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3) 
    ax.tick_params(axis="x", which="both", rotation=30)
    ax = fig.subplots()
    ax.set_facecolor("#000") # inner plot background color HTML black
    fig.patch.set_facecolor('#000') # outer plot background color HTML black
    ax.plot(xs, ys, linestyle = 'dashed', c = '#11f', linewidth = '1.5',
     marker = 'o', mec = 'hotpink', ms = 10, mfc = 'hotpink' )
    ax.set_xlabel('X-axis ')
    ax.set_ylabel('Y-axis ')
    ax.xaxis.label.set_color('hotpink') #setting up X-axis label color to hotpink
    ax.yaxis.label.set_color('hotpink') #setting up Y-axis label color to hotpink
    ax.tick_params(axis='x', colors='white') #setting up X-axis tick color to white
    ax.tick_params(axis='y', colors='white') #setting up Y-axis tick color to white
    ax.spines['left'].set_color('blue') # setting up Y-axis tick color to blue
    ax.spines['top'].set_color('blue') #setting up above X-axis tick color to blue
    ax.spines['bottom'].set_color('blue') #setting up above X-axis tick color to blue
    ax.spines['right'].set_color('blue') #setting up above X-axis tick color to blue
    fig.subplots_adjust(bottom=0.3) 
    ax.tick_params(axis="x", which="both", rotation=30) 
   
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #print(data)
    return data

def plotHum():
    times, temps, hums = getHistData(4)
    # Generate the figure **without using pyplot**.
    ys = hums
    xs = times
    fig = Figure()
    ax = fig.subplots()
    ax.set_facecolor("#000") # inner plot background color HTML black
    fig.patch.set_facecolor('#000') # outer plot background color HTML black
    ax.plot(xs, ys, linestyle = 'dashed', c = '#11f', linewidth = '1.5',
     marker = 'o', mec = 'hotpink', ms = 10, mfc = 'hotpink' )
    ax.set_xlabel('X-axis ')
    ax.set_ylabel('Y-axis ')
    ax.xaxis.label.set_color('hotpink') #setting up X-axis label color to hotpink
    ax.yaxis.label.set_color('hotpink') #setting up Y-axis label color to hotpink
    ax.tick_params(axis='x', colors='white') #setting up X-axis tick color to white
    ax.tick_params(axis='y', colors='white') #setting up Y-axis tick color to white
    ax.spines['left'].set_color('blue') # setting up Y-axis tick color to blue
    ax.spines['top'].set_color('blue') #setting up above X-axis tick color to blue
    ax.spines['bottom'].set_color('blue') #setting up above X-axis tick color to blue
    ax.spines['right'].set_color('blue') #setting up above X-axis tick color to blue
    fig.subplots_adjust(bottom=0.3) 
    ax.tick_params(axis="x", which="both", rotation=30) 
   
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #print(data)
    return data

@app.route("/")
def home():
    temp = plotTemp() 
    hum = plotHum()
    return render_template('index.html', temp = temp, hum = hum)
@app.route("/sensors/")
def sensors():
    return render_template('sensors.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
