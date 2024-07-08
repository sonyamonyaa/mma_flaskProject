from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, IntegerField, SelectField
from wtforms.fields.list import FieldList
from wtforms.validators import DataRequired,NumberRange

# Form to handle the lists of participants and items
class InputForm(FlaskForm):
    algo_name = SelectField(label=u'Algorithm Name',
                            choices=[('', 'Select Algorithm Name'), ('div', 'Divide and Choose'),
                                     ('alloc', 'Allocation by Matching')])
    participants = StringField(label='Participants (comma-separated)', validators=[DataRequired()])
    items = StringField(label='Items (comma-separated)', validators=[DataRequired()])
    submit = SubmitField('Update')
