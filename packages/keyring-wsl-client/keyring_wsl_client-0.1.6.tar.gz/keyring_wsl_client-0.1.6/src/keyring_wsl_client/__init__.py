__author__ = "Kalle M. Aagaard <git@k-moeller.dk>"
__version__ = "0.1.3"

import json
import subprocess

from typing import TypedDict


import keyring.backend
import keyring.credentials

class CredResult(TypedDict):
    username: str
    password: str


class WSLProxyBackend(keyring.backend.KeyringBackend):

    priority = 9.9 # type: ignore


    def __init__(self):
        self._cache: dict[tuple[str, str], str] = {}

    def _run(self, *args: str):
        with open("/tmp/keylog", "a") as fp:
            fp.write("==================================\n")
            fp.write(f"STDIN: {args!r}\n")
            r = subprocess.run(["keyring-host.exe", *args], capture_output=True)
            fp.write(f"STDOUT: {r.stdout!r}\n")
            fp.write(f"STDERR: {r.stderr!r}\n")
        return json.loads(r.stdout.decode().strip())["result"]

    def get_credential(self, service: str, username: str | None):
        try:
            args = [service]
            if username is not None:
                args.append(username)
            cred: CredResult | None  = self._run("cred", *args)
            
            if cred is None:
                print("NO CRED")
                with open("/tmp/keylog.log", "a") as fp:
                    fp.write("NO CRED")
                return None

            self._cache[service, cred["username"]] = cred["password"]
            return keyring.credentials.SimpleCredential(cred["username"], cred["password"])
        except Exception as e:
            print(e)
            with open("/tmp/keylog.log", "a") as fp:
                fp.write(str(e))


    def get_password(self, service: str, username: str):
        try:
            password = self._cache.get((service, username), None)
            if password is not None:
                print("CACHE")
                with open("/tmp/keylog.log", "a") as fp:
                    fp.write("CACHE")
                return password

            creds = self.get_credential(service, None)
            if creds and username == creds.username:
                return creds.password

            print("NO PASS")
            with open("/tmp/keylog.log", "a") as fp:
                fp.write("NO PASS")
            return None
        except Exception as e:
            print(e)
            with open("/tmp/keylog.log", "a") as fp:
                fp.write(str(e))


    def set_password(self, service: str, username: str, password: str):
        self._run("set", service, username, password)

    def delete_password(self, service: str, username: str):
        self._run("del", service, username)
