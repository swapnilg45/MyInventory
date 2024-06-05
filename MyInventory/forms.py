from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, IntegerField
from wtforms.validators import DataRequired,ValidationError
from models import Product, Location

class AddProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('qty', validators=[DataRequired()])
    submit = SubmitField('Add Product')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Add Location')



class MoveProductForm(FlaskForm):
    product_id = SelectField('Product', validators=[DataRequired()], coerce=str)
    from_location = SelectField('From Location', coerce=str, choices=[('', 'None')])
    to_location = SelectField('To Location', coerce=str, choices=[('', 'None')])
    qty = IntegerField('Quantity', validators=[DataRequired()])

    submit = SubmitField('Move Product')

    def validate_product_id(self, field):
        product = Product.query.get(field.data)
        if not product:
            raise ValidationError('Selected product does not exist.')

    def validate_from_location(self, field):
        if field.data:
            location = Location.query.get(field.data)
            if not location:
                raise ValidationError('Selected from location does not exist.')

    def validate_to_location(self, field):
        if field.data:
            location = Location.query.get(field.data)
            if not location:
                raise ValidationError('Selected to location does not exist.')

    def validate_qty(self, field):
        if field.data <= 0:
            raise ValidationError('Quantity must be a positive integer.')
