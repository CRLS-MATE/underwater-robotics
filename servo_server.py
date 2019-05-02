#!/usr/bin/python3

# import only required components of flask library
from flask import Flask, jsonify, request, render_template
import serial

ser = serial.Serial('/dev/ttyACM0', write_timeout=.1)  # open serial port
print(ser.name)         # check which port was really used

# create a flask object
app = Flask(__name__)

# match "/" with url
# (ie. abc.com/ or abc.com/?hello=world, not abc.com/hi/hello)
@app.route("/")
def send(): # arbitrary function name
    # create dictionary of the query string (everything in url after '?')
    all_args = request.args.to_dict()

    # iterate through all keys in dictionary
    for arg in all_args:
        # get index of servo to set
        i = int(arg)
        val = int(float(all_args[arg]))
        # log for debugging
        print("servo %2.0d: %5.0d" % (i, val))
        # set the servo to the value at the key
        print("about to write")
        ser.flush()
        try:
            ser.write(bytes([180 + i, val]));
        except:
            print("------------------------ FLUSHING ------------------------")
            ser.reset_input_buffer()
            ser.reset_output_buffer()
        print("just wrote")
        
    print(type(all_args))
    # return the dictionary as json for debugging
    return render_template('index.html', servos = all_args)

# if this file is the executed file (not linked from another file)
if __name__ == "__main__":
    # run the flask server
    app.run(host='0.0.0.0', debug=True)
