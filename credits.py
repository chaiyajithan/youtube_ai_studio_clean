import json
USER_DB = "users.json"

def load_users():
    try:
        with open(USER_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_credit(username):
    users = load_users()
    return users.get(username, {}).get("credits", 0)

def add_credit(username, amount):
    users = load_users()
    users.setdefault(username, {"password": "", "credits": 0})
    users[username]["credits"] += amount
    save_users(users)

def use_credit(username, amount=1):
    users = load_users()
    if users.get(username, {}).get("credits", 0) >= amount:
        users[username]["credits"] -= amount
        save_users(users)
        return True
    return False