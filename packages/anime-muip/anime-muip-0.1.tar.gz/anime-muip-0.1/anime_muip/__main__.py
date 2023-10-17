import requests
import hashlib

class AnimeMUIP():
    def __init__(self, secret: str, ssl: bool = False, ip: str = '127.0.0.1', port: int = 21051, ticket: str = 'GM', region: str = 'dev_docker', cmd_id: int = 1116):
        """
        Creates a client to process MUIP server commands

        Parameters
        -----------
        secret: str
            Authentication token on MUIP server.
        ssl: bool
            Whether to use SSL.
        ip: str
            Server IP.
        port: int
            Server port.
        ticket: str
            Server ticket.
        region: str
            Server region.
        cmd_id: int
            Server cmd_id.
        """

        self.secret = secret

        self.url = f'{"https" if ssl == True else "http"}://{ip}:{str(port)}/api'
        self.ticket = ticket
        self.region = region
        self.cmd_id = cmd_id

    def sha256_sign(self, secret: str, message: str):
        sha256 = hashlib.sha256()
        sha256.update(f"{message}{secret}".encode())
        return sha256.hexdigest()

    def muip_client(self, uid: int, command: str):
        """
        Sends a request to the MUIP server

        Parameters
        -----------
        uid: str
            UID of the user in game.
        command: str
            Your command.
        """

        payload = {
            "region": self.region,
            "ticket": self.ticket,
            "cmd": self.cmd_id,
            "uid": str(uid),
            "msg": command
        }

        kvs = []

        for key, value in payload.items():
            kvs.append(f"{key}={str(value)}")
            
        kvs.sort()

        qstr = "&".join(kvs)
        sign = self.sha256_sign(self.secret, qstr)
        payload['sign'] = sign

        response = requests.get(self.url, params=payload)
        return response.content.decode()