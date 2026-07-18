import json


FILE = "db.json"


def load_data():
    with open(FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_history(user_id, city, temperature):

    data = load_data()

    if "history" not in data:
        data["history"] = []

    data["history"].append({
        "user_id": user_id,
        "city": city,
        "temperature": temperature
    })

    save_data(data)


def get_history():

    data = load_data()

    return data.get("history", [])


def clear_history():

    data = load_data()

    data["history"] = []

    save_data(data)



def save_favorite(user_id, city):

    data = load_data()

    data[str(user_id)] = {
        "favorite_city": city
    }

    save_data(data)



def get_favorite(user_id):

    data = load_data()

    user = data.get(str(user_id))

    if user:
        return user.get("favorite_city")

    return None



def get_stats():

    data = load_data()

    return len(data.get("history", []))