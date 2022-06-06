from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from predict import predict_personality_
app = Flask(__name__)
api = Api(app)
CORS(app)
class fetch(Resource):
    def get(self,s):
        try:
            response=predict_personality_(s)
            return {'personality-type':response}
        except:
            return "error"
api.add_resource(fetch,'/getPersonality/<string:s>')
class status (Resource):
    def get(self):
        try:
            return {'data': 'Api is Running'}
        except:
            return {'data': 'An Error Occurred during fetching Api'}
api.add_resource(status,'/')
if __name__ == "__main__":
    app.run()
