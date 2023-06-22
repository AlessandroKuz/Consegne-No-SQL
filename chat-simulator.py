import redis
from getpass import getpass


r = redis.Redis(
  host='redis-19620.c250.eu-central-1-1.ec2.cloud.redislabs.com',
  port=19620,
  password='MFVkgjaJiqDkZHHcV9IShMTUDraHmYjg')


def users(users_hmap_name: str):
    username: str = input("Insert Username: ")
    if username.encode('utf-8') in r.hgetall(users_hmap_name):
        while True:
            password: str = getpass()
            if password.encode('utf-8') == r.hget(users_hmap_name, username):
                print(f"\nSuccessful login! Welcome back {username}.")
                break
            else:
                print("\nPassword incorrect, try again.")
    else:
        password1: str = getpass()
        while True:
            password2: str = getpass(prompt="Confirm Password: ")
            if password2 == password1:
                print(f"\nSuccessfully registered, Welcome {username}!")
                r.hset(users_hmap_name, username, password1)
                break
            if password2 == "q":
                exit()
            else:
                print("\nPassword don't match, try again.")
    return username


def send_messages(chat_messages: list, user: str):
    while True:
        message: str = input("Message: ")
        if message == 'q': break
        r.rpush(chat_messages, f"{user}: {message}")
    print("\nMessages sent successfully.")
        

def latest_messages(chat_messages: list):
    print()
    for message in r.lrange(chat_messages, -10, -1):
        message = message.decode("utf-8")
        print(message)
    input("\nPress enter to continue: ")


def main():
    actions = ((1, "Send message(s)"), (2, "Latest messages"), (3, "Exit"))
    if not r.exists("users"):
        r.hset("users", "chat", "admin1234")
    if not r.exists("chat_messages"):
        r.rpush("chat_messages", "Welcome to the chat!")
    user = users(users_hmap_name="users")
    chat_name = "chat_messages"
    try:
        while True:
            print(f"{actions[0][0]}. {actions[0][1]}\
                    \n{actions[1][0]}. {actions[1][1]}\
                    \n{actions[2][0]}. {actions[2][1]}")
            action: int = int(input("What would you like to do? "))
            if action == 1:
                send_messages(chat_name, user)
            if action == 2:
                latest_messages(chat_name)
            if action == 3:
                break
    except ValueError:
        print("\nYou should type in a valid number.")


if __name__ == "__main__":
    main()
