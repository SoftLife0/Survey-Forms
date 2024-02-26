from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from forms import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate


app=Flask(__name__)
app.config["SECRET_KEY"] = (
    "e98148fdc372680af4ddb5cfba21aeae90afed81f6b745c3a33444a2deaa420e"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    fields = db.relationship('SurveyField', backref='survey', lazy=True)

    def __repr__(self):
        return f"Survey('{self.name}', '{self.description}')"
    
class SurveyField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)  # Type of form field (e.g., text, select, checkbox)
    answer_type = db.Column(db.String(50), nullable=False)  # Type of answer response (e.g., text, single_select, multiple_select)
    options = db.Column(db.Text, nullable=True)  # Options for select or checkbox fields (stored as JSON string)

    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    survey = db.relationship('Survey', backref=db.backref('fields', lazy=True))

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
            return redirect(url_for('add_question', formId=new_survey.id))
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
    return render_template('add_question.html', form=form, survey=survey)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5500,debug=True)