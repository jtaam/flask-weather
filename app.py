import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Add city
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    # Fetch & show data
    cities = City.query.order_by('-id').all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=22e798af81a0e446f923a9745766b7e6'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        # print(r)
        weather = {
            'city': city.name,
            'temparature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        # print(weather)
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)
