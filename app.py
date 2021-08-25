from flask import Flask, request
from flask import jsonify, abort


app = Flask(__name__)


@app.errorhandler(403)
def return_forbidden_page(error):

    return jsonify(
        status=403, message="Forbidden Request"
    ), 403


@app.errorhandler(404)
def return_not_found_page(error):

    return jsonify(
        status=404, message="Not Found"
    ), 404


@app.route("/")
def return_index():
    # This is for debugging
    return jsonify(
        {
            "message": "Hello World!"
        }
    )


@app.route("/register", methods=["GET", "POST"])
@app.route("/register/<device_id>")
def check_device_register(device_id=None):

    if request.method == "POST" and request.is_json:

        #Add the device into postgresql database
        return jsonify(request.get_json())
    
    if device_id:
    
        #Add the postgresql database to check the device
        return jsonify(
            {
                "status_code": 200,
                "message": f"This is my device:{device_id}"
            }
        )
    
    abort(404)


@app.route("/collect", methods=["GET", "POST"])
def collect_event():

    if request.method == "POST":
        #Insert the data into monitor event
        return jsonify(
            {
                "status": 200,
                "message": "Event Received"
            }
        )

    abort(403)


if __name__ == "__main__":

    app.run("0.0.0.0", port=5000, debug=True, threaded=True)