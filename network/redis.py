from redis import Redis


def redis_connection():
    return Redis(unix_socket_path='/var/run/redis/redis-server.sock')

