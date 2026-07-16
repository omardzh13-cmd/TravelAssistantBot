import json


FILE = "db.json"


def save_history(user_id, city, temperature):

    with open(FILE, "r", encoding="utf-8") as file:
        data = json.load(file)


    data["history"].append({
        "user_id": user_id,
        "city": city,
        "temperature": temperature
    })


    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_history():

    with open(FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["history"]


def clear_history():

    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"history": []},
            file,
            indent=4,
            ensure_ascii=False
        )

def save_favorite(user_id, city):

    with open(FILE, "r", encoding="utf-8") as file:
        data = json.load(file)


    data[str(user_id)] = {
        "favorite_city": city
    }


    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_favorite(user_id):

    with open(FILE, "r", encoding="utf-8") as file:
        data = json.load(file)


    user = data.get(str(user_id))

    if user:
        return user["favorite_city"]

    return None