from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    consumer = db.Column(db.String(50), nullable=True)
    fields = db.relationship('SurveyField', backref='survey_parent', lazy=True)

    def __repr__(self):
        return f"Survey('{self.name}', '{self.description}')"
    
class SurveyField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)
    answer_type = db.Column(db.String(50), nullable=False)
    options = db.Column(db.Text, nullable=True)

    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    survey = db.relationship('Survey', backref=db.backref('survey_fields', lazy=True))

    def __repr__(self):
        return f"SurveyField('{self.label}', '{self.field_type}', '{self.answer_type}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    response_type = db.Column(db.String(50), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

    def __repr__(self):
        return f"Question(id={self.id}, text={self.text}, response_type={self.response_type})"




@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')


@app.route('/newForm', methods=['GET', 'POST'])
def newForm():
    form = NewForm()
    consumers = ["None", "Students", "Alumni", "Staff", "All"]
    if request.method == 'POST':
        if form.validate_on_submit():
            new_survey = Survey(
                name=form.name.data,
                description=form.description.data,
                consumer=request.form.get("answer"),
            )
            db.session.add(new_survey)
            db.session.commit()
            return redirect(url_for('add_question', surveyId=new_survey.id))
    return render_template('newform.html', form=form, consumers=consumers)

@app.route('/add_question/<int:surveyId>', methods=['GET', 'POST'])
def add_question(surveyId):
    survey = Survey.query.get_or_404(surveyId)
    form = NewQuestionForm()
    if form.validate_on_submit():
        new_question = Question(
            text=form.text.data,
            response_type=form.response_type.data,
            survey_id=surveyId
        )
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('add_question', surveyId=surveyId))
    return render_template('addQuestion.html', form=form, survey=survey)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5500,debug=True)