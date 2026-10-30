#Marshmallow
from marshmallow import Schema, fields, validate


# =================== auth checkout schemas =================== #

class ListOfItemsForCheckout(Schema):
    products_id = fields.Int(required=True, validate=validate.Range(min=1, error="Product ID must be greater than 0"))
    quantity = fields.Int(required=True, validate=validate.Range(min=1, error="minimum purchase amount must be more than 1"))

class CheckoutSchema(Schema):
    items = fields.List(
        fields.Nested(ListOfItemsForCheckout),
        required=True
    )

# =================== register schemas =================== #

class RegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(
            min=3, max=30,
            error= "The username must be between three and thirty characters long"
        )
    )

    email = fields.Email(required=True)

    password_hash = fields.Str(
        required=True,
        validate=validate.Length(
            min=8, max=72,error="The password must be between 8 and 72 characters long"
        ),
        load_only=True
    )

    phone_number = fields.Str(
        required=True,
        validate=[
            validate.Regexp(r"^[0-9]+$", error="The number may only contain digits"),
            validate.Length(min=10, max=20, error="The mobile phone number must be between 10 and 20 digits long")
        ]
    )

# =================== login schemas =================== #

class LoginSchema(Schema):
    username = fields.Str(
        required=True
    )

    password = fields.Str(
        required=True
    )