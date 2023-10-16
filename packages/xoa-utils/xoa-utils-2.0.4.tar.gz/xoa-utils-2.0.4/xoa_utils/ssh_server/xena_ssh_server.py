import asyncssh
import sys


class XenaSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn: "asyncssh.SSHServerConnection"):
        remote_host = conn.get_extra_info("peername")[0]
        print(f"{remote_host}: SSH connection received from {remote_host}.")

    def connection_lost(self, exc: Exception) -> None:
        if exc and str(exc) != "Connection lost":
            print("SSH connection error: " + str(exc), file=sys.stderr)
        else:
            print("SSH connection closed.")

    def begin_auth(self, username: str) -> bool:
        # If the user's password is the empty string, no auth is required
        return False

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        return True
