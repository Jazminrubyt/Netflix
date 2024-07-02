from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "af3dba35869fecea8ac6309dcb34c4a93034112f76febd4a0264f38975170dd6"
bcrypt = Bcrypt(app)
