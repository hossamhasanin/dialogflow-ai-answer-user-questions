from whitenoise import WhiteNoise

from flask_heroku_example import app

application = WhiteNoise(app)
