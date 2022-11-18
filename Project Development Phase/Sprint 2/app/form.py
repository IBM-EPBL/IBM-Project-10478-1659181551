from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User

class RegistrationForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class JobForm(FlaskForm):
    title = StringField('Job Title',
                        validators=[DataRequired(), Length(min=2, max=20)])
    industry = SelectField('Industry', choices=[('Construction', 'Construction'),
                                                ('Education', 'Education'),
                                                ('Food And Beverage', 'Food and Beverage'),
                                                ('Pharmaceutical', 'Pharmaceutical'),
                                                ('Entertainment', 'Entertainment'),
                                                ('Manufacturing', 'Manufacturing'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Agriculture', 'Agriculture'),
                                                ('Transportation', 'Transportation'),
                                                ('Computer And Technology', 'Computer and Technology'),
                                                ('Healthcare', 'Healthcare'),
                                                ('Media And News', 'Media and News'),
                                                ('Hospitality', 'Hospitality'),
                                                ('Energy', 'Energy'),
                                                ('Fashion', 'Fashion'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Finance And Economic', 'Finance and Economic'),
                                                ('Advertising And Marketing', 'Advertising and Marketing'),
                                                ('Mining', 'Mining'),
                                                ('Aerospace', 'Aerospace')],
                           validators=[DataRequired()])
    description = TextAreaField('Job Description',
                                validators=[DataRequired()])
    required_skill=SelectField("Required skill",choices=[('Data-Science','Data-science'),
                                                        ('Cyber-Security','Cyber-Security'),
                                                        ('App Development','App Development'),
                                                        ('Game Development','Game Development'),
                                                        ('Web Development','Web Development'),
                                                        ('Machine Learning','Machine Learning'),
                                                        ("SQL","SQL"),
                                                        ("Artificial Intelligence","Artificial Intelligence"),
                                                        ("Cloud Computing","Cloud Computing"),
                                                        ],
                                            validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProfileUpdateForm(FlaskForm):
    skill1=SelectField("skill-1",choices=[('Data-Science','Data-science'),
                                                        ('Cyber-Security','Cyber-Security'),
                                                        ('App Development','App Development'),
                                                        ('Game Development','Game Development'),
                                                        ('Web Development','Web Development'),
                                                        ('Machine Learning','Machine Learning'),
                                                        ("SQL","SQL"),
                                                        ("Artificial Intelligence","Artificial Intelligence"),
                                                        ("Cloud Computing","Cloud Computing"),
                                                        ],
                                            validators=[DataRequired()])
    skill2=SelectField("skill-2",choices=[('Data-Science','Data-science'),
                                                        ('Cyber-Security','Cyber-Security'),
                                                        ('App Development','App Development'),
                                                        ('Game Development','Game Development'),
                                                        ('Web Development','Web Development'),
                                                        ('Machine Learning','Machine Learning'),
                                                        ("SQL","SQL"),
                                                        ("Artificial Intelligence","Artificial Intelligence"),
                                                        ("Cloud Computing","Cloud Computing"),
                                                        ],
                                            validators=[DataRequired()])
    skill3=SelectField("skill-3",choices=[('Data-Science','Data-science'),
                                                        ('Cyber-Security','Cyber-Security'),
                                                        ('App Development','App Development'),
                                                        ('Game Development','Game Development'),
                                                        ('Web Development','Web Development'),
                                                        ('Machine Learning','Machine Learning'),
                                                        ("SQL","SQL"),
                                                        ("Artificial Intelligence","Artificial Intelligence"),
                                                        ("Cloud Computing","Cloud Computing"),
                                                        ],
                                            validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Others', 'Other')],
                         default='male',
                         validators=[DataRequired()])
    degree = SelectField('Degree',
                         default='eSchool',
                         choices=[('eSchool', 'School'),
                                  ('dHighSchool', 'HighSchool'),
                                  ('cBachelor', 'Bachelor'),
                                  ('bMaster', 'Master'),
                                  ('aPHD', 'PHD')],
                         validators=[DataRequired()])
    experience = IntegerField('Professional Experience in years',
                              validators=[DataRequired()])
    submit = SubmitField('Login')

