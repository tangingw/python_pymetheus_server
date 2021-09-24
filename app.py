from flask import Flask, request
from flask import jsonify, abort
from handler.device import DeviceRegisterHandler
from handler.event import EventHandler
from db.connector import get_connection


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
@app.route("/register/<device_name>")
def check_device_register(device_name=None):

    db_conn = get_connection("config")
    register_handler = DeviceRegisterHandler(db_conn)

    if request.method == "POST" and request.is_json:

        #Add the device into postgresql database
        register_handler.add_register(request.get_json())
        db_conn.close()       
        return jsonify(request.get_json())
    
    if device_name:
        device_id = register_handler.get_device(device_name)

        return jsonify(
            {
                "status_code": 200,
                "message": {
                    "device_name": device_name,
                    "device_id": device_id
                }
            }
        )
    
    abort(404)


@app.route("/collect", methods=["GET", "POST"])
def collect_event():

    if request.method == "POST" and request.is_json:
        #Insert the data into monitor event
        db_conn = get_connection("config")

        event_handler = EventHandler(db_conn)
        received_event = request.get_json()

        event_handler.add_current_event(
            received_event["event_type"], received_event["monitor_type"], 
            received_event["monitor_type_name"], {
                "event_type": received_event["event_type"], 
                "event_status": received_event["event_status"],
                "event_message": received_event["event_message"],
                "event_value": received_event["event_value"]
            }
        )
        
        db_conn.close()
        return jsonify(
            {
                "status": 200,
                "message": "Event Received"
            }
        )

    abort(403)


if __name__ == "__main__":

    app.run("0.0.0.0", port=5000, debug=True, threaded=True)