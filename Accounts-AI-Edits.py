import json as j
import os
import warnings as w
import getpass

w.simplefilter("always", Warning)

script = os.path.dirname(os.path.abspath(__file__))
acc = os.path.join(script, "Acc.json")
tempacc = os.path.join(script, "TempAcc.json")

DebugMode = False


def debug_toggle():
    global DebugMode
    choice = input("Enable debug mode? (y/n): ").strip().lower()
    if choice in {"y", "yes", "true", "1"}:
        password = getpass.getpass("Enter debug password: ")
        if password == "0000":
            DebugMode = True
            print("\033[38;5;156mDebug mode enabled.\033[0m")
            return True
        print("\033[38;5;160mIncorrect debug password.\033[0m")
        DebugMode = False
        return False
    DebugMode = False
    return False


DebugMode = debug_toggle()


class Handles:
    def __init__(self):
        self.warnconfig = self.Warn()
        self.errorconfig = self.Error()
        self.tipconfig = self.Tip()
        self.debugconfig = self.Debug()

    class Warn:
        def __init__(self):
            self.format = {
                "call": "\033[4;38;5;142m",
                "detail": "\033[0;38;5;144m",
                "normal": "\033[0m",
                "emphasis": "\033[1;38;5;150m",
                "warning": "\033[1;38;5;214m",
            }

        def FileNotFoundWarn(self, Ifile, Idir):
            fmt = self.format
            msg = (
                f"{fmt['emphasis']}'{Ifile}' {fmt['call']}was not found.\n"
                f"{fmt['detail']}Absolute directory given: {Idir}\n"
                f"Redirecting to fallback temporary file: {fmt['emphasis']}'TempAcc.json'{fmt['normal']}"
            )
            w.warn(msg, ImportWarning, stacklevel=5)

        def JSONDecodeWarn(self, file_path):
            fmt = self.format
            msg = (
                f"{fmt['warning']}The file {fmt['emphasis']}'{file_path}'{fmt['warning']} "
                f"contains invalid JSON and cannot be loaded safely.{fmt['normal']}"
            )
            w.warn(msg, ValueError, stacklevel=5)

        def WeakPasswordWarn(self, username):
            fmt = self.format
            msg = (
                f"{fmt['warning']}Password policy warning for user {fmt['emphasis']}'{username}'{fmt['warning']}. "
                f"Use a stronger password for better protection.{fmt['normal']}"
            )
            w.warn(msg, UserWarning, stacklevel=5)

        def DuplicateUserWarn(self, username):
            fmt = self.format
            msg = (
                f"{fmt['warning']}The username {fmt['emphasis']}'{username}'{fmt['warning']} "
                f"is already in use. Please choose another one.{fmt['normal']}"
            )
            w.warn(msg, UserWarning, stacklevel=5)

        def PasswordMismatchWarn(self):
            fmt = self.format
            msg = (
                f"{fmt['warning']}Password confirmation did not match the original password. "
                f"Please try again.{fmt['normal']}"
            )
            w.warn(msg, UserWarning, stacklevel=5)

        def FileWriteWarn(self, path):
            fmt = self.format
            msg = (
                f"{fmt['warning']}Unable to write data to {fmt['emphasis']}'{path}'{fmt['warning']} "
                f"due to an unexpected filesystem issue.{fmt['normal']}"
            )
            w.warn(msg, OSError, stacklevel=5)

        def EmptyInputWarn(self, field_name):
            fmt = self.format
            msg = (
                f"{fmt['warning']}The field {fmt['emphasis']}'{field_name}'{fmt['warning']} "
                f"received an empty value and should not be blank.{fmt['normal']}"
            )
            w.warn(msg, UserWarning, stacklevel=5)

    class Error:
        def __init__(self):
            self.format = {
                "call": "\033[4;16;1;160m",
                "detail": "\033[0;16;1;88m",
                "normal": "\033[0m",
                "emphasis": "\033[1;16;1;20m",
                "danger": "\033[1;38;5;160m",
            }

        def InputError(self, field_name, detail=""):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Input error in {fmt['emphasis']}'{field_name}'{fmt['danger']}. "
                f"{detail}{fmt['normal']}"
            )
            raise ValueError(msg)

        def AccountNotFoundError(self, username):
            fmt = self.format
            msg = (
                f"{fmt['danger']}No account exists for username {fmt['emphasis']}'{username}'{fmt['danger']}.{fmt['normal']}"
            )
            raise LookupError(msg)

        def InvalidChoiceError(self, choice):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Invalid action choice: {fmt['emphasis']}'{choice}'{fmt['danger']}. "
                f"Accepted values may include sign up or login.{fmt['normal']}"
            )
            raise ValueError(msg)

        def FileWriteError(self, path):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Unable to save account data to {fmt['emphasis']}'{path}'{fmt['danger']}.{fmt['normal']}"
            )
            raise OSError(msg)

        def EmptyUsernameError(self):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Username cannot be empty or whitespace only.{fmt['normal']}"
            )
            raise ValueError(msg)

        def EmptyPasswordError(self):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Password cannot be empty or whitespace only.{fmt['normal']}"
            )
            raise ValueError(msg)

        def DuplicateUsernameError(self, username):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Username {fmt['emphasis']}'{username}'{fmt['danger']} already exists.{fmt['normal']}"
            )
            raise ValueError(msg)

        def LoginFailedError(self, username):
            fmt = self.format
            msg = (
                f"{fmt['danger']}Login failed for username {fmt['emphasis']}'{username}'{fmt['danger']}.{fmt['normal']}"
            )
            raise PermissionError(msg)

        def PasswordMismatchError(self):
            fmt = self.format
            msg = (
                f"{fmt['danger']}The re-entered password does not match the original password.{fmt['normal']}"
            )
            raise ValueError(msg)

    class Tip:
        def __init__(self):
            self.format = {
                "call": "\033[4;232;8;241m",
                "detail": "\033[0;232;8;245m",
                "normal": "\033[0m",
                "emphasis": "\033[1;232;8;250m",
                "tip": "\033[38;5;117m",
            }

        def StrongPasswordTip(self):
            fmt = self.format
            print(
                f"{fmt['tip']}Tip: Use a long password with letters, numbers, and symbols for stronger security.{fmt['normal']}"
            )

        def KeepBackupTip(self):
            fmt = self.format
            print(
                f"{fmt['tip']}Tip: Keep a backup of your account file in case the system resets or the file is damaged.{fmt['normal']}"
            )

        def UsernameHintTip(self):
            fmt = self.format
            print(
                f"{fmt['tip']}Tip: Use a unique username that is easy to remember but hard for others to guess.{fmt['normal']}"
            )

        def RecoveryTip(self):
            fmt = self.format
            print(
                f"{fmt['tip']}Tip: If a login fails, check whether the user account exists or if the password was typed incorrectly.{fmt['normal']}"
            )

        def DebugTip(self):
            fmt = self.format
            print(
                f"{fmt['tip']}Tip: Debug mode checks all code paths and confirms whether required functions ran successfully.{fmt['normal']}"
            )

    class Debug:
        def __init__(self):
            self.enabled = bool(DebugMode)
            self.format = {
                "debug": "\033[38;5;156m",
                "miss": "\033[38;5;88m",
                "normal": "\033[0m",
                "emphasis": "\033[1;38;5;150m",
                "soft": "\033[38;5;150m",
            }
            self.ran = []
            self.missed = []
            self.events = 0
            self.expected = []

        def enable(self):
            self.enabled = True
            self.format = {
                "debug": "\033[38;5;156m",
                "miss": "\033[38;5;88m",
                "normal": "\033[0m",
                "emphasis": "\033[1;38;5;150m",
                "soft": "\033[38;5;150m",
            }

        def register_expected(self, name):
            if name not in self.expected:
                self.expected.append(name)

        def mark(self, name, condition=True, detail=""):
            self.events += 1
            if condition:
                if name not in self.ran:
                    self.ran.append(name)
                if detail:
                    msg = f"{self.format['debug']}DEBUG {self.events}: {name} -> {detail}{self.format['normal']}"
                else:
                    msg = f"{self.format['debug']}DEBUG {self.events}: {name}{self.format['normal']}"
                print(msg)
                return True
            self.missed.append(name)
            if detail:
                msg = f"{self.format['miss']}DEBUG MISS {self.events}: {name} -> {detail}{self.format['normal']}"
            else:
                msg = f"{self.format['miss']}DEBUG MISS {self.events}: {name}{self.format['normal']}"
            print(msg)
            return False

        def check_file(self, label, path):
            if not self.enabled:
                return False
            exists = os.path.exists(path)
            self.mark(label, exists, f"path exists: {exists}")
            return exists

        def check_input(self, label, value):
            if not self.enabled:
                return False
            valid = value is not None and str(value).strip() != ""
            self.mark(label, valid, f"value={value!r}")
            return valid

        def check_sequence(self, label, sequence):
            if not self.enabled:
                return False
            present = bool(sequence)
            self.mark(label, present, f"sequence length={len(sequence)}")
            return present

        def summary(self):
            print(f"{self.format['miss']}DEBUG SUMMARY - MISSED PATHS{self.format['normal']}")
            if self.missed:
                for item in self.missed:
                    print(f"{self.format['miss']}{item}{self.format['normal']}")
            else:
                print(f"{self.format['emphasis']}No missed debug paths.{self.format['normal']}")
            print(f"{self.format['debug']}DEBUG SUMMARY - RAN PATHS{self.format['normal']}")
            if self.ran:
                for item in self.ran:
                    print(f"{self.format['debug']}{item}{self.format['normal']}")
            else:
                print(f"{self.format['emphasis']}No debug runs recorded.{self.format['normal']}")



class Account:
    def __init__(self, choice, data):
        self.data = data
        self.current_user = None
        self.warn = Handles().warnconfig
        self.error = Handles().errorconfig
        self.tip = Handles().tipconfig
        self.debug = Handles().debugconfig

        choice = str(choice).strip()
        choice_lower = choice.lower()

        if DebugMode:
            self.debug.enable()
            self.debug.mark("account_init", True, "account object created in debug mode")
            self.debug.mark("account_choice", True, f"choice={choice!r}")
            self.debug.check_file("account_data_file", acc)
            self.debug.check_input("account_choice_input", choice)
            self.debug.check_sequence("account_data_list", self.data)
            if choice_lower in {"sign", "sign up", "signup"}:
                self.debug.mark("signup_path", True, "signup branch selected")
                return
            if choice_lower in {"log", "log in", "login"}:
                self.debug.mark("login_path", True, "login branch selected")
                return
            self.debug.mark("invalid_choice_path", False, f"choice={choice_lower!r}")
            return

        if choice_lower in {"sign", "sign up", "signup"}:
            self.Sign.Up(choice="UP", data=self.data)
        elif choice_lower in {"log", "log in", "login"}:
            self.Log.In()
        elif choice_lower in {"log out", "logout", "sign out", "signout"}:
            self.Log.Out()
        else:
            raise self.error.InvalidChoiceError(choice)

    class Sign:
        class Up:
            def __init__(self, choice, data):
                self.data = data
                self.warn = Handles().warnconfig
                self.error = Handles().errorconfig
                self.tip = Handles().tipconfig
                self.debug = Handles().debugconfig
                self.username = ""
                self.password = ""
                if str(choice).upper() == "UP":
                    if DebugMode:
                        self.debug.enable()
                        self.debug.mark("signup_debug_init", True, "signup process checked")
                        return
                    self.username_check()
                    self.password_check()
                    self.data_setup()
                    self.data_add()

            def username_check(self):
                u_unique = False
                while not u_unique:
                    username = input("Enter a username: ")
                    self.debug.mark("username_check", True, f"username_input={username!r}")
                    if not str(username).strip():
                        self.error.EmptyUsernameError()
                    for users in self.data:
                        if isinstance(users, dict) and str(username).lower() == str(users.get("USERNAME", "")).lower():
                            self.warn.DuplicateUserWarn(username)
                            self.tip.UsernameHintTip()
                            break
                    else:
                        self.username = username
                        u_unique = True

            def password_check(self):
                p_same = False
                while not p_same:
                    password1 = input("Enter a password: ")
                    password2 = input("Reenter your password: ")
                    self.debug.mark("password_check", True, f"password_entry={password1!r}")
                    if not str(password1).strip():
                        self.error.EmptyPasswordError()
                    if password1 == password2:
                        self.password = password1
                        if len(self.password) < 8:
                            self.warn.WeakPasswordWarn(self.username)
                            self.tip.StrongPasswordTip()
                        p_same = True
                    else:
                        self.warn.PasswordMismatchWarn()
                        self.tip.StrongPasswordTip()

            def data_setup(self):
                add_data = {
                    "USERNAME": self.username,
                    "PASSWORD": self.password,
                }
                self.data.append(add_data)
                self.debug.mark("data_setup", True, f"added user={self.username!r}")

            def data_add(self):
                global filefound
                if os.path.exists(acc):
                    filefound = True
                    try:
                        with open(acc, "w", encoding="utf-8") as file:
                            j.dump(self.data, file)
                        self.debug.mark("data_add_file_write", True, f"saved to {acc}")
                    except OSError:
                        filefound = False
                        self.warn.FileWriteWarn(acc)
                        raise self.error.FileWriteError(acc)
                else:
                    filefound = False
                    try:
                        with open(tempacc, "w", encoding="utf-8") as file:
                            j.dump(self.data, file)
                        self.debug.mark("data_add_temp_write", True, f"saved to {tempacc}")
                    except OSError:
                        self.warn.FileWriteWarn(tempacc)
                        raise self.error.FileWriteError(tempacc)

        class In:
            def __init__(self):
                self.warn = Handles().warnconfig
                self.error = Handles().errorconfig
                self.tip = Handles().tipconfig
                self.debug = Handles().debugconfig
                if DebugMode:
                    self.debug.enable()
                    self.debug.mark("login_debug_init", True, "login path checked")
                    return
                self.username_check()
                self.password_check()

            def username_check(self):
                username = input("Enter your username: ")
                self.debug.mark("login_username_check", True, f"username={username!r}")
                if not str(username).strip():
                    self.error.EmptyUsernameError()
                for users in data:
                    if isinstance(users, dict) and str(username).lower() == str(users.get("USERNAME", "")).lower():
                        self.username = username
                        return
                self.error.AccountNotFoundError(username)

            def password_check(self):
                username = self.username
                password = input("Enter your password: ")
                self.debug.mark("login_password_check", True, f"password_checked_for={username!r}")
                if not str(password).strip():
                    self.error.EmptyPasswordError()
                for users in data:
                    if isinstance(users, dict) and str(username).lower() == str(users.get("USERNAME", "")).lower():
                        saved_password = str(users.get("PASSWORD", ""))
                        if password == saved_password:
                            print(f"\033[38;5;150mLogin successful for {username}.\033[0m")
                            return
                        self.error.LoginFailedError(username)
                self.error.LoginFailedError(username)

        class Out:
            def __init__(self):
                self.debug = Handles().debugconfig
                self.debug.mark("logout_process", True, "user attempted logout")
                print("\033[38;5;150mLogged out successfully.\033[0m")

    class Log:
        class Register:
            def __init__(self):
                self.debug = Handles().debugconfig
                self.debug.mark("register_path", True, "Register path reached")
                print("\033[38;5;150mRegistration route ready.\033[0m")

        class In:
            def __init__(self):
                self.debug = Handles().debugconfig
                self.debug.mark("login_class_path", True, "Login class path reached")
                print("\033[38;5;150mLogin route ready.\033[0m")

        class Out:
            def __init__(self):
                self.debug = Handles().debugconfig
                self.debug.mark("logout_class_path", True, "Logout class path reached")
                print("\033[38;5;150mLogout route ready.\033[0m")

    def CurrentAccount(self):
        self.debug = Handles().debugconfig
        if DebugMode:
            self.debug.mark("current_account_check", True, "CurrentAccount path validated")
            return self.current_user
        if self.current_user is None:
            return None
        return self.current_user

    def __str__(self):
        self.debug = Handles().debugconfig
        if DebugMode:
            self.debug.mark("__str__", True, "string conversion path validated")
        return str(self.data)

    def RemoveAccount(self, username):
        self.debug = Handles().debugconfig
        if DebugMode:
            self.debug.mark("remove_account_debug", True, f"username={username!r}")
            return True
        for index, users in enumerate(self.data):
            if isinstance(users, dict) and str(users.get("USERNAME", "")).lower() == str(username).lower():
                del self.data[index]
                with open(acc, "w", encoding="utf-8") as file:
                    j.dump(self.data, file)
                self.debug.mark("remove_account_success", True, f"removed {username!r}")
                return True
        self.error.AccountNotFoundError(username)
        return False

    def DeleteAccount(self, username):
        self.debug = Handles().debugconfig
        if DebugMode:
            self.debug.mark("delete_account_debug", True, f"username={username!r}")
            return True
        return self.RemoveAccount(username)

    def __del__(self):
        self.debug = Handles().debugconfig
        if DebugMode:
            self.debug.mark("__del__", True, "object cleanup path validated")
        self.data = []


try:
    with open(acc, "r", encoding="utf-8") as file:
        data = j.load(file)
    filefound = True
    if DebugMode:
        Handles().debugconfig.enable()
        Handles().debugconfig.mark("file_load", True, f"loaded {acc}")
except FileNotFoundError:
    Handles().warnconfig.FileNotFoundWarn(Ifile="Acc.json", Idir=acc)
    data = []
    filefound = False
    if DebugMode:
        Handles().debugconfig.enable()
        Handles().debugconfig.mark("file_load", False, f"missing file: {acc}")
except j.JSONDecodeError:
    Handles().warnconfig.JSONDecodeWarn(acc)
    data = []
    filefound = False
    if DebugMode:
        Handles().debugconfig.enable()
        Handles().debugconfig.mark("file_load", False, f"invalid JSON in {acc}")


if __name__ == "__main__":
    if DebugMode:
        debug = Handles().debugconfig
        debug.enable()
        debug.register_expected("script_main")
        debug.register_expected("file_load")
        debug.register_expected("account_choice")
        debug.register_expected("signup_debug_init")
        debug.register_expected("login_debug_init")
        debug.register_expected("account_init")
        debug.mark("script_main", True, "debug mode execution path reached")
        debug.check_file("account_file", acc)
        debug.check_file("temporary_account_file", tempacc)
        debug.summary()
    else:
        Account(choice="sign up", data=data)
        debug = Handles().debugconfig
        debug.summary()
