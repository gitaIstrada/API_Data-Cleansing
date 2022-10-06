#Importing Library
import pandas as pd #memanggil library pandas alias pd untuk mengatur tata letak data
import re #memanggil library regex pendukung data cleansing (mendefinisikan sebuah pola pencarian dan membantu melakukan matching dan manipulasi teks)

#memanggil package flask untuk pembuatan api dan swagger untuk doc
from flask import request, Flask, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

from for_cleaning import * #fungsi add on

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Gita Istrada Putra')
        }, host = LazyString(lambda: request.host)
    )

swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }

swagger = Swagger(app, template=swagger_template, config=swagger_config)
@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = { 
        'status_code':200, 
        'description':'Menyapa hello binar gold challange', 
        'data': "Hello binar gold challange"
        }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')

    json_response = { 
        'status_code':200, 
        'description':'teks yang sudah diproses', 
        'data': preprocess(text),
        }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text_processing_file', methods=['POST'])
def text_processing_file():
    text = request.files.getlist('file')[0]

    #abusive_dict = pd.read_csv('docs/abusive.csv')
    alay_dict = pd.read_csv('docs/new_kamusalay.csv', encoding='iso-8859-1', header=None)
    alay_dict = alay_dict.rename(columns={0: 'original', 1: 'replacement'})

    #merubah bentuk df menjadi dict sehingga mudah untuk dipanggil
    alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))
    
    #merubah kata alay menjadi kata baku
    def normalize_alay(text):
        return ''.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])
   
    #memanggil semua fungsi cleaning
    def preprocess(text):
        text = lowercase(text)
        text = remove_nonaplhanumeric(text)
        text = remove_unnecessary_char(text)
        text = normalize_alay(text)
        return text

    #original data
    df_new = pd.DataFrame()
    df_data = pd.read_csv(text, encoding='iso-8859-1')
    df_new['old_tweet'] = df_data['Tweet']

    #mengaplikasikan fungsi preprocess ke output databaru
    df_data['Tweet'] = df_data['Tweet'].apply(preprocess)
    df_new['new_tweet'] = df_data['Tweet']

    df_new.to_csv('output_filename.csv', sep=',')

    json_response = { 
        'status_code':200, 
        'description':'teks yang sudah diproses', 
        'data': 'success'
        }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()

