import sys
from conf import config
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import Flask, redirect, request, jsonify, make_response,send_file, send_from_directory
from flask_cors import cross_origin
from oryza import OryzaAPI
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Aclimate Oryza Web API"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# Decorator which validates request to API should be logged
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        headers = [h for h in request.headers if h[0].lower() == 'x-access-token']
        if len(headers) > 0:
            token = headers[0][1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, config["SECRET_KEY"],algorithms=["HS256"])
            print(data)
            #current_user = User.objects.get(public_id=data['public_id'])
            current_user = config['CURRENT_USER']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'})
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token. Please log in again.'})
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator

@app.route('/')
def home():
    return redirect("/swagger")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

@app.route('/api/v1/login', methods=['POST'])
@cross_origin()
def login_user():
    auth = request.get_json()
    if not auth or not auth.get("user") or not auth.get("password"):
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = config['CURRENT_USER'] if config['CURRENT_USER'] == auth.get("user") else None

    if not user:
        # returns 401 if user does not exist
        return make_response('Could not verify',401,{'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'})

    #if check_password_hash(config['CURRENT_PWD'], auth.get("password")):
    if config['CURRENT_PWD'] == auth.get("password"):
        token = jwt.encode({'user': user, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=5)}, config['SECRET_KEY'],algorithm="HS256")
        return jsonify({'token' : token})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/api/v1/run', methods=['POST'])
@cross_origin()
@token_required
def run(current_user):
    response = None
    try:
        print(request.files)
        file = request.files['inputs']
        file_like_object = file.stream._file
        oryza_cli = OryzaAPI(config["ROOT_PATH"],config['R_COMMAND'])
        file = oryza_cli.generate_forecast(file_like_object)
        print("Output file",file)
        if file:
            response = send_file(file, mimetype='text/csv', as_attachment=True, download_name="output")
        else:
            response = make_response(jsonify({"message": "Inputs are not correct", "error": "unknown"}), 401)
    except Exception as e:
        print(e)
        response = make_response(jsonify({"message": "Error during execution", "error": str(e)}), 500)
    return response

if __name__ == "__main__":
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'], debug=config['DEBUG'])