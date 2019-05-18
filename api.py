from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import pandas as pd
import json

parser = reqparse.RequestParser()
parser.add_argument('lat', type=float)
parser.add_argument('lng', type=float)
parser.add_argument('cost', type=str)
parser.add_argument('place', type=str)
parser.add_argument('count', type=int)

app = Flask(__name__)
api = Api(app)

df = pd.read_csv('df_final.csv')

def get_recommendations(lat, lng, cost, place, count, df):
    if cost:
        df = df[df[cost] == 1]
    if place:
        df = df[df[place] == 1]
    
    df['lat'] = df['location_lat'].apply(lambda x: abs(x - lat))
    df['lng'] = df['location_lng'].apply(lambda x: abs(x - lng))
    df = df.sort_values(by=['lat','lng'])
    df = df.head(count)
    df = df[['name', 'location_lat', 'location_lng', 'rating', 'address']]
    
    return df.to_json(orient='records', force_ascii=False).strip()

class HelloWorld(Resource):
    def post(self):
        args = parser.parse_args()
        lat = args['lat']
        lng = args['lng']
        cost = args['cost']
        place = args['place']
        count = args['count']
        res = get_recommendations(lat, lng, cost, place, count, df)
        
        return res

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
