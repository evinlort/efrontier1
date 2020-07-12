import json
import app
import sys


def get_data() -> dict:
    with open("data.json", "r") as f:
        return json.loads(f.read())


def save_to_output(json_list):
    with open("output.json", "w") as f:
        f.write(json_list)


if __name__ == "__main__":
    data = get_data()
    output = list()
    saved_timestamp = list(data.keys())[0]
    try:
        coefficient = int(sys.argv[1])
    except:
        coefficient = 28  # Max profit for given data set
    stream = app.stream.set_coefficient(coefficient)
    for timestamp in data.keys():
        # Each 30 secs fetch saved "predicted" trade
        if int(timestamp) - 30000 >= int(saved_timestamp):
            output.append(stream.get_trade())
            saved_timestamp = timestamp
        # Calculate new "prediction"
        if stream.set(timestamp, data[timestamp]):
            stream.calculate()
    output = [out for out in output if out is not None]
    save_to_output(json.dumps(output, indent=4))
