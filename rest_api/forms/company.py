from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

# from flask_login import current_user
from rest_api.models.company import CompanyModel







class RegistrationForm (FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])
    submit = SubmitField("Register!")

    def check_company_name(self, company_name):

        if CompanyModel.find_by_name(company_name):
            raise ValidationError("Sorry, that company name already exists.")


    def check_email(self, email):
        if CompanyModel.find_by_email(email):
            raise ValidationError("Sorry, that email already exists.")