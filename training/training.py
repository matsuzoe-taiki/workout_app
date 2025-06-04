from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
from sqlalchemy import Float
from datetime import datetime

db_uri = 'mysql+pymysql://root:@localhost:3306/workout_db?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise = db.Column(db.String(50), nullable=False)  # 種目名
    weight = db.Column(db.Float, nullable=False)          # 重量
    reps = db.Column(db.Integer, nullable=False)          # 回数
    date = db.Column(db.DateTime, default=datetime.utcnow)  # 日付

class Bench_press(db.Model):
    __tablename__ = 'bench_press'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise = db.Column(db.String(50), nullable=False)  # 種目名
    weight = db.Column(db.Float, nullable=False)          # 重量
    reps = db.Column(db.Integer, nullable=False)          # 回数
    date = db.Column(db.DateTime, default=datetime.utcnow)  # 日付

class Bench_press_Machine(db.Model):
    __tablename__ = 'bench_press_machine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise = db.Column(db.String(50), nullable=False)  # 種目名
    weight = db.Column(db.Float, nullable=False)          # 重量
    reps = db.Column(db.Integer, nullable=False)          # 回数
    date = db.Column(db.DateTime, default=datetime.utcnow)  # 日付

with app.app_context():
    db.create_all()

@app.route("/")
def training():
    workouts = Workout.query.order_by(Workout.date.desc()).limit(10).all()
    message = "筋トレLOG"
    return render_template("view.html", workouts = workouts, message=message)

@app.route("/add", methods=['POST'])
def add():
    exercise = request.form.get("exercise")
    weight = float(request.form.get("weight"))
    reps = int(request.form.get("reps"))
    new_workout = Workout(exercise = exercise, weight = weight, reps = reps)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for("training"))

@app.route("/benchpress", methods=["GET"])
def show_bench_press():
    workouts = Workout.query.all()
    for workout in workouts:
        if workout.exercise == "ベンチプレス":
            exists = Bench_press.query.filter_by(exercise=workout.exercise, weight=workout.weight, reps=workout.reps, date=workout.date).first() 
            if not exists:
                bp = Bench_press(exercise = workout.exercise, weight = workout.weight, reps = workout.reps, date = workout.date)
                db.session.add(bp)
    db.session.commit()
    bench_datas = Bench_press.query.order_by(Bench_press.date.desc()).all()
    return render_template("view_benchpress.html", bench_datas=bench_datas)

@app.route("/benchpress_machine", methods=["GET"])
def show_bench_press_machine():
    workouts = Workout.query.all()
    for workout in workouts:
        if workout.exercise == "マシンベンチプレス":
            exists = Bench_press_Machine.query.filter_by(exercise=workout.exercise, weight=workout.weight, reps=workout.reps, date=workout.date).first() 
            if not exists:
                bp = Bench_press_Machine(exercise = workout.exercise, weight = workout.weight, reps = workout.reps, date = workout.date)
                db.session.add(bp)
    db.session.commit()
    bench_machine_datas = Bench_press_Machine.query.order_by(Bench_press_Machine.date.desc()).all()
    return render_template("view_benchpress_machine.html", bench_machine_datas=bench_machine_datas)

@app.route("/benchpress/gragh", methods=["GET"])
def show_bench_press_gragh():
    datas = Bench_press.query.order_by(Bench_press.date)
    dates = []
    weights = []
    for data in datas:
        dates.append(data.date)
        total_weight = data.weight * data.reps
        weights.append(total_weight)
    if weights[-1] > weights[-2]:
        message = 'おめでとうございます。総重量が上がりました。'
    else:
        message = '引き続き頑張りましょう。'
    return render_template("view_gragh.html", labels=dates, data=weights, message = message)


if __name__ == "__main__":
    app.run(debug=True)