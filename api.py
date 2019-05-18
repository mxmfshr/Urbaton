from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import pandas as pd
import json

parser = reqparse.RequestParser()
parser.add_argument('lat', type=float)
parser.add_argument('lng', type=float)
parser.add_argument('filters', action='append')
parser.add_argument('count', type=int)

app = Flask(__name__)
api = Api(app)

df = pd.read_csv('df_final.csv')

def get_recommendations(lat, lng, filters, count, df):
    if filters:
        for filter in filters:
            df = df[df[filter] == 1]
    
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
        filters = args['filters']
        count = args['count']
        res = get_recommendations(lat, lng, filters, count, df)
        
        return res

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=False)
