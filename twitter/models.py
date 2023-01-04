class Proxy(object):
    def __init__(self, user: str, pswd: str, host: str, port: str):
        self.user = user
        self.pswd = pswd
        self.host = host
        self.port = port

    def __repr__(self):
        return f"<Proxy user={self.user} pswd={self.pswd} host={self.host} port={self.port}>"

    def __str__(self):
        return f"http://{self.user}:{self.pswd}@{self.host}:{self.port}"