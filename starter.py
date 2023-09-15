import argparse
import os
import uuid


def generate_env(username, password):
    env = []
    compose_location = os.path.join(os.getcwd(), 'services/docker-compose.yml')

    env.append(f'ADMIN_USERNAME={username}')
    env.append(f'ADMIN_PASSWORD={password}')
    env.append(f'COMPOSE_LOCATION={compose_location}')

    credentials = [f'PASSWORD_{(i * 1000) + 10000}={uuid.uuid4().hex}' for i in range(20)]
    env.extend(credentials)
    return '\n'.join(env)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, default='admin')
    parser.add_argument('-p', '--password', type=str, default='admin')
    parser.add_argument('-c', '--challenges', type=str, default='', help='challenge names')
    args = parser.parse_args()

    cwd = os.getcwd()
    env = generate_env(args.username, args.password)
    receiver_env = os.path.join(cwd, 'receiver/.env')
    services_env = os.path.join(cwd, 'services/.env')

    with open(receiver_env, 'w') as f:
        f.write(env)
    
    with open(services_env, 'w') as f:
        f.write(env)

    os.chdir(os.path.join(cwd, 'services'))
    os.system(f'docker compose -f docker-compose.yml up --build -d {args.challenges}')
    
    os.chdir(os.path.join(cwd, 'receiver'))
    os.system('apt-get install -y gcc python3-dev libgmp3-dev libssl-dev libffi-dev build-essential')
    os.system('python3 -m pip install -r requirements.txt')
    os.system('uvicorn main:app --reload --host 0.0.0.0 --port 80')



if __name__ == '__main__':
    main()










