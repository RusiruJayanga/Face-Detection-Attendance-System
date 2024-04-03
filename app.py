from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_subject = request.form.get('selected_subject')
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Select the last record for each student ID on the selected date
    cursor.execute("SELECT name, MAX(time) FROM attendance WHERE date = ? AND subject = ? GROUP BY name", (formatted_date, selected_subject))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)

    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)