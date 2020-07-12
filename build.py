import json


def get_data() -> dict:
    with open("data.json", "r") as f:
        return json.loads(f.read())


if __name__ == "__main__":
    data_list = [(timestamp, assets) for timestamp, assets in get_data().items()]

    first_row = data_list.pop(0)
    ft = int(first_row[0])
    firstA = first_row[1]["assetA"]
    firstB = first_row[1]["assetB"]

    output = list()

    for timestamp, assets in data_list:
        A = assets["assetA"]
        B = assets["assetB"]
        if ft + 30000 <= int(timestamp):
            ft = int(timestamp)
            template = {"time": ft, "actions": list()}
            if firstA['ask'] > A['ask']:
                print(A['ask'], "buyA ---")
                template["actions"].append("buyA")
            else:
                print(A['ask'], "sellA +++")
                template["actions"].append("sellA")
            if firstB['ask'] > B['ask']:
                # print(B['ask'], "buyB ---")
                template["actions"].append("buyB")
            else:
                # print(B['ask'], "sellB +++")
                template["actions"].append("sellB")
            output.append(template)
        firstA = A
        firstB = B

    print(json.dumps(output))
