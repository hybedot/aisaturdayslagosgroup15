from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
import numpy as np
import pickle as p


app = Flask(__name__)
app.config['SECRET_KEY'] = 'blocking 4'

CORS(app)

api = Api(app)

modelfile = 'models/final_prediction.pickle'
model = p.load(open(modelfile, 'rb'))

class Predict(Resource):
    def post(self):
        json_data = request.get_json()
        
        try:
            age = json_data['age']
            position_category = json_data['positionCategory'] 
            signing_category = json_data['signingCategory']
            page_views = json_data['pageViews']
            fpl_value = json_data['fplValue']
            fpl_sell = json_data['fplSell']
            fpl_points = json_data['fplPoints']
            big_club_category = json_data['bigClubCategory']

            prediction_data = [age, position_category, signing_category, page_views, fpl_value, fpl_sell, fpl_points, big_club_category]

            prediction = np.array2string(model.predict([prediction_data]))

            prediction = prediction.strip('[]')


            return {
                    'status code':'200',
                    'message':prediction
                    }, 200
        except:
            return {
                    'status code':'500',
                    'message':'Invalid Values'
                    }, 500



#connect class with endpoint
api.add_resource(Predict, '/api/predict')

if __name__ == '__main__':
    app.run(debug=True)