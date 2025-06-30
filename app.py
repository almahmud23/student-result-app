import csv
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from student import Student, SpecialStudent

app = Flask(__name__)
students = []

CSV_FILE = "students.csv"

# --- Load from CSV on startup ---
def load_from_csv():
    try:
        with open(CSV_FILE, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                marks = list(map(int, row["marks"].split()))
                if row["is_special"] == "True":
                    s = SpecialStudent(row["name"], row["roll"], marks)
                else:
                    s = Student(row["name"], row["roll"], marks)
                students.append(s)
    except FileNotFoundError:
        pass  # Ignore if file doesn't exist yet

# --- Save to CSV on student add ---
def save_to_csv(student):
    with open(CSV_FILE, mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            student.roll,
            student.name,
            " ".join(map(str, student.marks)),
            round(student.average(), 2),
            student.grade(),
            isinstance(student, SpecialStudent)
        ])

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll = request.form['roll']
    marks = list(map(int, request.form['marks'].split()))
    is_special = request.form.get('special') == 'on'

    student = SpecialStudent(name, roll, marks) if is_special else Student(name, roll, marks)
    students.append(student)
    save_to_csv(student)

    return redirect(url_for('view_students'))

@app.route('/students')
def view_students():
    result_data = []
    for s in students:
        result_data.append({
            'name': s.name,
            'roll': s.roll,
            'marks': s.marks,
            'average': round(s.average(), 2),
            'grade': s.grade(),
            'status': 'Bonus Pass' if isinstance(s, SpecialStudent) and any(m < 33 for m in s.marks) and s.grade() != 'Fail' else 'OK' if s.grade() != 'Fail' else 'Fail'
        })
    return render_template('students.html', students=result_data)

@app.route('/download')
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True)
    else:
        return "❌ No CSV file available yet.", 404


# --- Initialize on startup ---
if __name__ == '__main__':
    load_from_csv()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
