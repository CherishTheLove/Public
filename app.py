from flask import Flask, request, render_template
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 'templates/index.html' 파일을 렌더링

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        date = request.form['date']
        time = request.form['time']

        korea_timezone = timezone("Asia/Seoul")
        input_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").replace(tzinfo=korea_timezone)

        solar_altitude = get_altitude(latitude, longitude, input_datetime)
        solar_azimuth = get_azimuth(latitude, longitude, input_datetime)

        optimal_angle = solar_altitude

        return render_template('index.html', result=True, altitude=solar_altitude, azimuth=solar_azimuth, optimal_angle=optimal_angle)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == "__main__":
    app.run(debug=False)
