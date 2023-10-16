# MODULES
import scp, re, datetime, os
import warnings
from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
    import paramiko

# MODELS
from ..models.main import AlphaFile

# LIBS
from .string_lib import universal_decode
from . import io_lib

WINDOWS_LINE_ENDING = "\r\n"
UNIX_LINE_ENDING = "\n"


def standardize_content(content: str) -> str:
    """
    Standardize the formatting of a string.

    Replaces occurrences of "\r\n", "\\r\\n", and "\\r\n" with "\n" and replaces occurrences of "\\t" with "\t".

    Args:
        content: A string to standardize.

    Returns:
        The standardized string.
    """
    if not isinstance(content, str):
        content = content.decode("utf-8")
    return content.replace("\\r\\n", "\n").replace("\\r\n", "\n").replace("\\t", "\t")


def process_content(content: str, parameters: dict[str, object] | None = None) -> str:
    """
    Process the content of a string.

    If the string starts with "file:", the rest of the string is interpreted as a file path and the contents of the file
    are read and returned. If `parameters` is not None, the function replaces occurrences of "{{key}}" in the content
    string with the corresponding value in `parameters`.

    Args:
        content: A string to process.
        parameters: A dictionary of key-value pairs to replace in the content string.

    Returns:
        The processed content string.
    """
    if content.startswith("file:"):
        path = content.replace("file:", "")
        if not os.path.exists(path):
            path = os.path.join(os.getcwd(), path)
        with open(path, "r") as f:
            content = f.read()
    if parameters is not None:
        for key, value in parameters.items():
            content = content.replace(f"{key}", str(value))
    return content


def split_lines(content: str):
    return content.split(
        "\r\r\n" if "\r\r\n" in content else ("\r\n" if "\r\n" in content else "\n")
    )


class AlphaSsh:
    host = None
    user = None
    password = None
    ssh = None

    def __init__(self, host, user, password=None, log=None, keys=True):
        self.host = host
        self.user = user
        self.password = password
        self.log = log
        self.keys = keys

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.history = {}

    def connect(self):
        if self.keys:
            self.ssh.connect(self.host, username=self.user, password=self.password)
        else:
            self.ssh.connect(
                self.host,
                username=self.user,
                password=self.password,
                look_for_keys=False,
            )
        connected = self.test()
        if connected:
            self.scp = scp.SCPClient(self.ssh.get_transport())
        return connected

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

        if exc_type:
            print(f"exc_type: {exc_type}")
            print(f"exc_value: {exc_value}")
            print(f"exc_traceback: {exc_traceback}")

    def disconnect(self):
        """Close ssh connection."""
        if self.test():
            self.ssh.close()
        self.scp.close()  # Coming later

    def test(self):
        return (
            self.ssh.get_transport() is not None
            and self.ssh.get_transport().is_active()
        )

    def wait(self):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("")
        while not ssh_stdout.channel.exit_status_ready():
            pass

    def list_files(self, directory: str) -> list[AlphaFile]:
        """[summary]

        Args:
            directory (str): [description]

        Returns:
            list[AlphaFile]: [description]
        """
        output = self.execute_cmd(f"ls -l {directory}")
        files = io_lib.get_list_file(output)
        return files

    def list_files_names(
        self, directory: str, pattern: str | None = None, hidden: bool = False
    ) -> list[str]:
        cmd = "ls -lt %s" % directory
        cmd = f"find {directory} -maxdepth 1 -type f"
        if pattern is not None:
            cmd += f' -iname "{pattern}"'

        output = self.execute_cmd(cmd)
        lines = split_lines(str(output))
        # if pattern is not None:
        """filtered = []
        for line in lines:
            matchs = re.findall(pattern,line)
            if matchs:
                filtered.append(line)
        lines = filtered"""
        # lines = [x for x in lines if len(re.findall(pattern, x)) != 0]

        files_names = []
        for line in lines:
            if line.strip() == "":
                continue
            elements = line.split()

            # Récupérer le dernier élément, qui est le chemin complet du fichier.
            full_file_path = elements[-1]

            # Utiliser les opérations de découpage de chemin pour obtenir le nom de fichier.
            file_name = full_file_path.split("/")[-1]
            files_names.append(file_name)

        if hidden:
            return [x for x in files_names if x.replace(".", "") != ""]
        else:
            return [
                x
                for x in files_names
                if x.replace(".", "") != "" and not x.startswith(".")
            ]

    def list_directories(self, directory: str) -> list[AlphaFile]:
        """[summary]

        Args:
            directory (str): [description]

        Returns:
            list[AlphaFile]: [description]
        """
        output = self.execute_cmd("ls -l %s" % directory)
        directories = io_lib.get_list_file(output)
        return directories

    def list_directories_names(self, directory: str, hidden: bool = False) -> list[str]:
        output = self.execute_cmd("ls -l -f %s" % directory)
        lines = str(output).split()
        if hidden:
            return [
                x
                for x in lines
                if x.replace(".", "") != "" and (not "." in x or x.startswith("."))
            ]
        else:
            return [x for x in lines if x.replace(".", "") != "" and not "." in x]

    def get_file_content(
        self, filepath: str, decode=False, escape_replace: bool = True
    ):
        output = self.execute_cmd(f"cat {filepath}", decode=decode)
        return standardize_content(output) if escape_replace else output

    def is_file(self, filename: str):
        output = self.execute_cmd("test -f %s && echo 'y'" % filename)
        return "y" in output

    def is_directory(
        self,
        path: str,
        group: str | None = None,
        user: str | None = None,
        mode=None,
    ):
        return self.is_dir(path=path, group=group, user=user, mode=mode)

    def is_dir(
        self,
        path: str,
        group: str | None = None,
        user: str | None = None,
        mode=None,
    ):
        output = self.execute_cmd("test -d %s && echo 'y'" % path)
        if group is not None and not self.is_group(group, path):
            return False
        if user is not None and not self.is_user(user, path):
            return False
        if mode is not None and not self.is_mode(mode, path):
            return False
        return "y" in output

    def make_directory(
        self,
        path: str,
        group: str | None = None,
        user: str | None = None,
        mode=None,
        ensure_path: bool = True,
    ):
        options = ""
        if ensure_path:
            options = "-p"
        if not self.is_dir(path):
            self.execute_cmd("mkdir %s %s" % (options, path))
            if not self.is_dir(path):
                return False
        if group is not None:
            self.change_group(group, path)
        if user is not None:
            self.change_user(user, path)
        if mode is not None:
            self.change_mode(mode, path)
        return True

    def get_mode(self, path: str):
        out = self.execute_cmd("stat -c %a " + path)
        mode = re.findall(r"[0-9]+", out)
        return mode[0] if len(mode) != 0 else None

    def is_mode(self, mode: str, path: str):
        mode = str(self.get_mode(path))
        return mode == str(mode)

    def change_mode(self, mode: int, path: str, recursively: bool = False):
        mode_c = ""
        if recursively:
            mode_c = "-R"
        self.execute_cmd("chmod %s %s %s" % (mode_c, mode, path))
        return str(mode) == self.get_mode(path)

    def change_group(self, group: int, path: str, recursively: bool = False):
        mode = ""
        if recursively:
            mode = "-R"
        self.execute_cmd("chgrp %s %s %s" % (mode, group, path))

    def get_group(self, path: str):
        return self.execute_cmd("stat -c %G " + path)

    def is_group(self, group: str, path: str):
        current_group = self.get_group(path)
        current_group = current_group.split()[0]
        return current_group == group

    def change_user(self, user: str, path: str, recursively: bool = False):
        mode = ""
        if recursively:
            mode = "-R"
        self.execute_cmd("chown %s %s %s" % (mode, user, path))

    def add_group_to_user(self, user: str, group: str):
        self.execute_cmd("usermod -a -G %s %s" % (group, user))

    def get_user(self, path: str):
        return self.execute_cmd("stat -c %U " + path).replace("\\r\\n", "")

    def is_user(self, user: str, path: str):
        current_user = self.get_user(path)
        return current_user == user

    def append_to_file(self, content: str, path: str):
        content = process_content(content)
        original_content = self.get_file_content(path, decode=True)
        self.execute_cmd("echo '%s' >> %s" % (content, path))
        new_content = self.get_file_content(path, decode=True)
        if not "No such file or directory" in original_content:
            return new_content == original_content + content + "\n"
        return new_content == content + "\n"

    def is_in_file(self, content: str, path: str):
        content = process_content(content)
        original_content = self.get_file_content(path, decode=True)
        return content in original_content

    def restart_service(self, service: str):
        self.execute_cmd("sudo systemctl restart %s" % service)

    def is_equal_to_file(self, content: str, path: str, mode: int | None = None):
        if not self.is_file(path):
            return False

        if mode is not None:
            self.change_mode(mode, path)

        content = process_content(content)
        double_backslash = "\\n" in content
        original_content = self.get_file_content(path, decode=True)

        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        original_content = original_content.replace(
            WINDOWS_LINE_ENDING, UNIX_LINE_ENDING
        )
        original_content_u = "\\n" in original_content
        """if double_backslash and not original_content_u:
            original_content = original_content.replace('\\','\\\\')"""
        original_content = original_content.replace("\\'", "'").replace("\\\\", "\\")

        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
        original_content = original_content.replace(
            WINDOWS_LINE_ENDING, UNIX_LINE_ENDING
        )

        equal = content == original_content or (
            content == original_content[:-1] and original_content[-1:] == "\n"
        )

        """if not equal:
            lines1, lines2 = content.split('\n'), original_content.split('\n')
            for i, e in enumerate(lines1):
                if lines1[i] != lines2[i]:
                    a, b = lines1[i],lines2[i]
                    c, d = a, b.replace('\\\'','\'')
                    print(lines1[i],'\n',lines2[i])"""

        return equal

    def create_file(self, path: str):
        self.execute_cmd(f"touch {path}")
        return self.is_file(path)

    def write_to_file(
        self,
        content: str,
        path: str,
        ensure_path: bool = True,
        parameters: dict[str, object] = None,
    ) -> bool:
        if ensure_path:
            self.make_directory(os.path.dirname(path))

        if content.startswith("file:"):  # TODO: remove
            content_path = content.replace("file:", "")
            self.scp.put(content_path, path)
            return True
        else:
            if not self.is_file(path):
                self.create_file(path)
            content = process_content(content, parameters)

            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
            self.execute_cmd(f"echo -e '{content}' > {path}")
            new_content = self.get_file_content(path, decode=True).replace(
                WINDOWS_LINE_ENDING, UNIX_LINE_ENDING
            )
            return new_content == content + "\n"

    def is_sudoers(self, user: str, cmd: str):
        sudo_line = "%s ALL = (ALL) NOPASSWD: %s" % (user, cmd)
        sudoers_content = self.get_file_content("/etc/sudoers", decode=True)
        return sudo_line in sudoers_content

    def is_user_exist(self, user: str):
        users_content = self.get_file_content("/etc/passwd", decode=True)
        return user + ":" in users_content

    def check_python_version(self, version: str):
        output = self.execute_cmd("python --version")
        current_version = re.findall(r"\s([0-9]+.[0-9]+.?[0-9]*)\b", output)[0]
        version_nb = re.findall(r"([0-9\.]+)", version)
        version = version.replace(version_nb[0], "'%s'" % version_nb[0])

        cmd = "'%s' %s" % (str(current_version), str(version))
        valid_version = eval(cmd)
        return valid_version

    def is_output(self, cmd: str):
        output = self.execute_cmd(cmd)
        return len(output.replace("\\n", "").replace("\\r", "").strip()) != 0

    def is_found(self, cmd: str, greps: list[str] = []):
        if type(greps) == str:
            greps = [greps]
        cmd = cmd + " | " + " | ".join(['grep "%s"' % x for x in greps])
        output = self.execute_cmd(cmd, lines=True)
        if "illegal" in output[0]:
            return False
        if len(output) == 1 and output[0].strip() == "":
            return False
        return len(output) != 0

    def get_pid(self, greps: list[str] = []):
        if type(greps) == str:
            greps = [greps]
        cmd = "ps aux -P | " + " | ".join(['grep "%s"' % x for x in greps])
        output = self.execute_cmd(cmd, lines=True)
        if len(output) == 0:
            return None
        if len(output) == 1:
            return re.findall(r"[0-9]+", output)[0]
        return [
            re.findall(r"[0-9]+", x)[0]
            for x in output
            if len(re.findall(r"[0-9]+", x)) != 0
        ]

    def is_pid(self, greps=[]):
        return self.get_pid(greps=greps) is not None

    def service_restart(self, service: str):
        cmd = f"sudo systemctl restart {service}"
        return self.execute_cmd(cmd)

    def service_start(self, service: str, start: bool = True):
        action = "restart" if start else "stop"
        cmd = f"sudo systemctl {action} {service}"
        return self.execute_cmd(cmd)

    def service_enable(self, service: str, enable=True):
        action = "enable" if enable else "disable"
        cmd = f"sudo systemctl {action} {service}"
        return self.execute_cmd(cmd)

    def reload_systemctl(self):
        cmd = "systemctl daemon-reload"
        return self.execute_cmd(cmd)

    def package_installed(self, package: str):
        cmd = "sudo yum list installed | grep " + package
        output = self.execute_cmd(cmd)
        return output.startswith(package)

    def install_package(self, package: str):
        cmd = "yum install -y " + package
        output = self.execute_cmd(cmd)
        return output.startswith(package)

    def is_python_module(self, module: str):
        cmd = "which python"
        output = self.execute_cmd(cmd)
        cmd = "python -c 'import %s'" % module
        output = self.execute_cmd(cmd)
        valid = not ("No module named " in output and module in output)
        return valid

    def install_python_module(self, module: str, version: str | None = None):
        cmd = "which pip"
        output = self.execute_cmd(cmd)
        cmd = f"yes | pip install {module}{version}"
        output = self.execute_cmd(cmd)
        return not "error" in output

    def add_user(
        self,
        user: str,
        description: str | None = None,
        group: str | None = None,
        password: str | None = None,
    ):
        options = ""
        if description is not None:
            options += ' -c "%s"' % description
        cmd = "sudo useradd %s %s" % (options, user)
        self.execute_cmd(cmd)

        if group is not None:
            self.add_group_to_user(user, group)

        if password is not None:
            cmd = 'echo "%s" | sudo passwd --stdin %s' % (password, user)
            self.execute_cmd(cmd)

    def execute_cmd(self, cmd, decode=True, lines=False, timeout: int = 600):
        inputs, output, err = "", "", ""
        if self.log:
            self.log.info(f"EXEC: {cmd}")
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(
            cmd, get_pty=True, timeout=timeout
        )
        output = ssh_stdout.read()
        if lines:
            decode = True
        if decode:
            try:
                output = output.decode("utf-8")
                if self.log:
                    self.log.info(f"OUTPUT: {output[:100]} ...")
                # output = output.decode('utf-8').encode('ascii')
            except Exception as ex:
                if self.log:
                    self.log.error(f"", ex=ex)
                pass
            output = str(output)
            if output[:2] == "b'":
                output = output[2:-1]

        output = standardize_content(output)
        if lines:
            output = output.split("\n")

        self.history[datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")] = [
            cmd,
            output,
        ]
        return output

    def execute_cmd_interactive(self, cmd, decode=True):
        inputs, output, err = "", "", ""
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)

        i, limit = 0, 100
        while not ssh_stdout.channel.exit_status_ready() and i < limit:
            # Print data whena available
            if ssh_stdout.channel.recv_ready():
                alldata = ssh_stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = ssh_stdout.channel.recv(1024)
                    alldata += prevdata
                output += str(alldata)
            i += 1

        if decode:
            inputs, output, err = (
                universal_decode(inputs),
                universal_decode(output),
                universal_decode(err),
            )
            if inputs != "" and self.log:
                self.log.info("inputs:", inputs)
            if err != "" and self.log:
                self.log.error("err:", err)
        return output
