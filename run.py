import json
import app


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
    for timestamp in data.keys():
        # Each 30 secs fetch saved "predicted" trade
        if int(timestamp) - 30000 >= int(saved_timestamp):
            output.append(app.stream.get_trade())
            saved_timestamp = timestamp
        # Calculate new "prediction"
        if app.stream.set(timestamp, data[timestamp]):
            app.stream.calculate()
    output = [out for out in output if out is not None]
    save_to_output(json.dumps(output, indent=4))
