#Flask
from flask import Flask, request, jsonify

#sql alchemy basic
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

#enum
from enum import Enum

#Flask_migrate
from flask_migrate import migrate

#JWT
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#Marshmallow
from flask_marshmallow import Marshmallow

#.env
import os
from dotenv import load_dotenv