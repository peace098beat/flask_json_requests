#! coding:utf-8
"""
"""
import json, os
from functools import wraps
from flask import Flask, Response, jsonify, request, abort, url_for
from fifitools import StatusCodes, ContentType

app = Flask(__name__)

""" config """
app.config["JSON_DIR"] = "db_json"

""" Content Type Checker"""

def consumes(content_type):
    def _consumes(function):
        @wraps(function)
        def __consumes(*argv, **keywords):
            if request.headers['Content-Type'] != content_type:
                abort(StatusCodes.BadRequest400)
            return function(*argv, **keywords)

        return __consumes

    return _consumes

""" Init """
def init():
    json_dir = app.config["JSON_DIR"]
    if(os.path.exists(json_dir) == False):
        os.mkdir(json_dir)
init()

""" Helth Check """


@app.route('/helth', methods=['GET', 'POST'])
def helth():
    """ Helth CHeck API"""

    response = jsonify({'results': 'succes'})
    response.status_code = StatusCodes.OK200
    return response


""" REST API """


@app.route('/api/<key>', methods=["GET"])
def get(key):
    content_body_dict = model_get(key)
    assert type(content_body_dict) == dict

    if(content_body_dict == {}):
        response = jsonify({"response":"Model Nothing"})
        response.status_code = StatusCodes.BadRequest400
        return response
    else:
        response = jsonify(content_body_dict)
        response.status_code = StatusCodes.OK200
        return response


@app.route('/api/<key>', methods=["POST"])
@consumes('application/json')
def post(key):
    content_body_dict = json.loads(request.data.decode("utf-8"))
    assert type(content_body_dict) == dict

    model_set(key, content_body_dict)

    # Create Resopnse Objects
    response = jsonify(content_body_dict)
    response.status_code = StatusCodes.created
    response.headers['Location'] = url_for('get', key=key)
    return response

@app.route('/api/<key>', methods=['DELETE'])
def delete(key):

    result = model_delete(key)

    response = Response()

    if(result):
        response.status_code = StatusCodes.NoContent
    else:
        response.status_code = StatusCodes.BadRequest400

    return response

""" Model Accesseres"""

def model_set(key: str, value: dict):
    filename = get_json_file_path(key)
    with open(filename, "w") as fp:
        json.dump(value, fp)


def model_get(key: str)-> dict:
    """ Load Model
    if not model : return None
    if exists json : return dict
    """

    filename = get_json_file_path(key)

    if(os.path.exists(filename) is False):
        return {}

    with open(filename, "r") as fp:
        result = json.loads(fp.read())
        assert type(result) == dict

    return result

def model_delete(key: str)->bool:
    """ Model Delete"""
    filepath = get_json_file_path(key)
    try:
        if (os.path.exists(filepath)):
            os.remove(filepath)
    except Exception as e:
        app.logger.error(e)
        return False

    return True

def get_json_file_path(key):
    filename = key+'.json'
    return os.path.join(app.config["JSON_DIR"], filename)


if __name__ == '__main__':
    app.init()
    app.run(debug=True)
