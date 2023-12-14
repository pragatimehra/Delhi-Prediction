import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request
import pickle

app = Flask(__name__, template_folder='/Users/pragatimehra/Desktop/Delhi/templates'    )
data = pd.read_excel("Cleaned-Delhi-Prices.xlsx")
model = pickle.load(open('model.pkl', 'rb'))
le = LabelEncoder()
x = le.fit_transform(data['Location'])

@app.route('/')
def index():
    locations = sorted(data['Location'].unique())
    return render_template('home.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    area = request.form.get('area')
    bhk = request.form.get('bhk')
    ne = request.form.get('toggle')
    at = request.form.get('atm')
    se = request.form.get('security')
    ca = request.form.get('car')
    li = request.form.get('lift')
    n = 0
    for i in range(414):
        if data['Location'][i] == location:
            n = i
            break
    if at == 'on':
        atm = 1
    else:
        atm = 0
    if se == 'on':
        security = 1
    else:
        security = 0
    if ca == 'on':
        car = 1
    else:
        car = 0
    if li == 'on':
        lift = 1
    else:
        lift = 0
    if ne == 'on':
        new = 1
    else:
        new = 0
    print(area, x[n], bhk, new, atm, security, car, lift)
    input_data = pd.DataFrame([[area, x[n], bhk, new, atm, security, car, lift]],
                              columns=['Area', 'Location', 'No. of Bedrooms', 'Resale', 'ATM', '24X7Security', 'CarParking', 'LiftAvailable'])
    pred = model.predict(input_data)[0] * 1e6
    return str(np.round(pred, 2))

if __name__ == "__main__":
    app.run(debug=True)
