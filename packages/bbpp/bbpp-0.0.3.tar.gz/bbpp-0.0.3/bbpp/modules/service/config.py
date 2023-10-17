import json
import os.path

from typing import Optional, Dict


class Config:
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        workspace: Optional[str] = None,
        sound: str = 'ping.wav',
    ):

        self.config_file = os.path.join(
            os.path.expanduser('~'), '.bbpp/bbpp.conf'
        )

        if username and password and workspace:
            self._write_config_file(
                username=username,
                password=password,
                workspace=workspace,
                sound=sound,
            )

        else:
            self.check_config_file_exists()
            self.config = self._read_config_file()
            self.username = self.config['username']
            self.password = self.config['password']
            self.workspace = self.config['workspace']
            self.sound = self.config['sound']
            self.auth = (self.username, self.password)

    def check_config_file_exists(self) -> None:
        if not os.path.exists(self.config_file):
            raise ValueError(
                'Cannot find config file, please configure your credentials `bbpp config -h`'
            )

    def _write_config_file(
        self, username: str, password: str, workspace: str, sound: str
    ) -> None:
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            config = {
                'username': username,
                'password': password,
                'workspace': workspace,
                'sound': sound,
            }
            f.write(json.dumps(config))

    def _read_config_file(self) -> Dict[str, str]:
        with open(self.config_file, 'r') as f:
            config = json.loads(f.read())
            return config
