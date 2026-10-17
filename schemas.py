#Marshmallow
from marshmallow import Schema, fields, validate


class ListOfItemsForCheckout(Schema):
    products_id = fields.Int(required=True, validate=validate.Range(min=1, error="Product ID must be greater than 0"))
    quantity = fields.Int(required=True, validate=validate.Range(min=1, error="minimum purchase amount must be more than 1"))

class CheckoutSchema(Schema):
    items = fields.List(
        fields.Nested(ListOfItemsForCheckout),
        required=True
    )