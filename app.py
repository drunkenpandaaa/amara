from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amara.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Status(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	price = db.Column(db.Integer, nullable = False)

class Place(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Booking(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	date = db.Column(db.DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(hours=3))
	name = db.Column(db.String(100), nullable = False)
	surname = db.Column(db.String(100), nullable = False)
	phone = db.Column(db.String(100), nullable = False)
	place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

@app.route('/')
def main():
	return render_template('mainPage.html')

@app.route('/tents', methods=['GET', 'POST'])
def tents():
	if request.method == 'POST':
		dateFromMain = request.form['date-in']
		return render_template('tentsPage.html', dateIn=dateFromMain)
	return render_template('tentsPage.html', dateIn=date.today().strftime("%d-%m-%Y"))

@app.route('/about')
def about():
	return render_template('aboutPage.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == 'POST':
		surnameBooking = request.form['surnameBooking']
		nameBooking = request.form['nameBooking']
		phoneBooking = request.form['phoneBooking']
		#dateFromMain = request.form['dateIn']
		booking = Booking(name=nameBooking, surname=surnameBooking, phone=phoneBooking, date=date.today(), place_id=1)
		try:
			db.session.add(booking)
			db.session.commit()
			return render_template('adminService.html', dateIn=date.today().strftime("%d-%m-%Y"))
		except SQLAlchemyError as e:
			  error = str(e.__dict__['orig'])
			  return error
	else:
		return render_template('adminService.html', dateIn=date.today().strftime("%d-%m-%Y"))
	
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')