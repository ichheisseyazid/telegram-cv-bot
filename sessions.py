# sessions.py

# In-memory store: { telegram_id: { "step": 0, "data": {} } }
user_sessions = {}

def create_session(user_id: int):
    user_sessions[user_id] = {
        "step": 0,
        "data": {}
    }

def get_session(user_id: int):
    return user_sessions.get(user_id)

def update_session_data(user_id: int, key: str, value: str):
    user_sessions[user_id]["data"][key] = value

def advance_step(user_id: int):
    user_sessions[user_id]["step"] += 1

def get_step(user_id: int):
    return user_sessions[user_id]["step"]

def delete_session(user_id: int):
    if user_id in user_sessions:
        del user_sessions[user_id]