from cgitb import reset
from datetime import date
from flask import Flask
from flask import render_template,request
import numpy as np
import math
import random
import re


app = Flask(__name__)

@app.route("/")
@app.route("/",methods=["POST"])
def register():
    result=dict()
    result["date"]=date.today()
    result["average"]="Average of 8 and 3 is "+str(np.average(np.arange(1,10)))
    result["sum"]="2 power 12 is "+ str(math.pow(2,2))
    result['random']="This is a random number "+str(random.randint(1,100))
    pattern = '\d+'
    test_string = 'Twelve:12 Eighty nine:89.'
    result["regex='\d+'"] = "str=='Twelve:12 Eighty nine:89.' after ::split--->>> "+ str(re.split(pattern, test_string) )

    return render_template("display.html",result=result)