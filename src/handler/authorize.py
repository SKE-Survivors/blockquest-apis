from handler import DatabaseHandler, SessionHandler
from utils import build_response


def handle_authorize(remote, _token, user_info):
    # if _token:
    #     save_token(remote.name, token)

    if not user_info:
        body = {"STATUS": "FAILED", "MESSAGE": f"Authorization failed"}
        return build_response(status_code=400, err=err)

    dbh = DatabaseHandler()
    sh = SessionHandler()

    try:
        # check if user exist
        user = dbh.find_user(user_info["username"])
        # (if not) create user, add to database
        if not user:
            user = dbh.add_user(
                mail=user_info["email"],
                username=user_info["username"],
                password=b"",  # or None
            )
    except Exception as err:
        body = {"STATUS": "FAILED", "MESSAGE": f"Authorization failed: {err}"}
        return build_response(status_code=400, body=body)

    # gen token and add to redis
    token = sh.set_session(user.email)
    body = {
        "STATUS": "SUCCESS",
        "MESSAGE": {
            "email": user.email,
            "token": token
        }
    }
    return build_response(status_code=201, body=body)
