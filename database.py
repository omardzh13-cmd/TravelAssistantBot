import json



def load_data():

    with open("db.json", "r", encoding="utf-8") as file:
        return json.load(file)



def save_data(data):

    with open("db.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def add_history(user_id, city, temperature):
    data = load_data()
    user_id = str(user_id)


    if user_id not in data["users"]:
        data["users"][user_id] = {
            "history": []
        }


    data["users"][user_id]["history"].append({
        "city": city,
        "temperature": temperature
    })

    save_data(data)


def get_history(user_id):

    data = load_data()
    user_id = str(user_id)
    if user_id in data["users"]:
        return data["users"][user_id]["history"]

    return []