import redis


r = redis.Redis(
    host='redis-19620.c250.eu-central-1-1.ec2.cloud.redislabs.com',
    port=19620,
    password='MFVkgjaJiqDkZHHcV9IShMTUDraHmYjg')


def check_for_team_existance(teams):
    t1, t2 = teams
    if not r.get(t1):
        r.set(t1, 0)
    if not r.get(t2):
        r.set(t2, 0)


def main():
    # solo per 2 squadre
    check_for_team_existance(('t1', 't2'))

    while True:
        print("""What action would you like to perform 
        1) add 1 point
        2) add 2 points
        3) add 3 points
        4) print specified team result
        5) print all teams result""")
        try:
            comando = input("What action would you like to do (1/2/3/4/q - t1/t2): ")
            comando = comando.split()
            if comando[0] == "1":
                r.incr(comando[1])
                print(f'{comando[0]} point was added')
            elif comando[0] == "2":
                r.incrby(comando[1], 2)
                print(f'{comando[0]} point was added')
            elif comando[0] == "3":
                r.incrby(comando[1], 3)
                print(f'{comando[0]} point was added')
            elif comando[0] == "4":
                print(f"\nTeam: {comando[1]} has {int(r.get(comando[1]))} points.\n")
            elif comando[0] == "5":
                print(f"\nTeam1: {int(r.get('t1'))}, Team2: {int(r.get('t2'))}\n")
            elif comando[0].lower() == "q":
                break
            else:
                print("Invalid input.")
        except:
                print("Invalid input.")


if __name__ == "__main__":
    main()
    