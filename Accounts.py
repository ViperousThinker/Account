import json as j
import os
import warnings as w

w.simplefilter("always", Warning)
script = os.path.dirname(os.path.abspath(__file__))
acc = os.path.join(script, "Acc.json")
tempacc = os.path.join(script, "TempAcc.json")


class Handles:
    def __init__(self):
        self.warnconfig = self.Warn()
        self.errorconfig = self.Error()
        self.tipconfig = self.Tip()

    class Warn:
        def __init__(self):
            self.format = {
                "call": "\033[4;38;5;142m",
                "detail": "\033[0;38;5;144m",
                "normal": "\033[0m",
                "emphasis": "\033[1;38;5;150m",
            }

        def FileNotFoundWarn(self, Ifile, Idir):
            fmt = self.format
            msg = (
                f"{fmt['emphasis']}'{Ifile}' {fmt['call']}was not Found.\n"
                f"{fmt['detail']}Absolute Directory given: {Idir}\n"
                f"Redirecting to Fallback Temporary File: {fmt['emphasis']}'TempAcc.json'{fmt['normal']}"
            )
            w.warn(msg, ImportWarning, stacklevel=5)

    class Error:
        def __init__(self):
            self.format = {
                "call": "\033[4;16;1;160m",
                "detail": "\033[0;16;1;88m",
                "normal": "\033[0m",
                "emphasis": "\033[1;16;1;20m",
            }

    class Tip:
        def __init__(self):
            self.format = {
                "call": "\033[4;232;8;241m",
                "detail": "\033[0;232;8;245m",
                "normal": "\033[0m",
                "emphasis": "\033[1;232;8;250m",
            }


try:
    with open(acc, "r", encoding="utf-8") as file:
        data = j.load(file)
    filefound = True
except FileNotFoundError:
    Handles().warnconfig.FileNotFoundWarn(Ifile="Acc.json", Idir=acc)
    data = []
    filefound = False
except j.JSONDecodeError:
    data = []
    filefound = False


class Account:
    def __init__(self, choice, data):
        self.data = data
        choice = str(choice).strip()
        choice_lower = choice.lower()

        if choice_lower in {"sign", "sign up", "signup"}:
            self.Sign.Up(choice="UP", data=self.data)
        elif choice_lower in {"log", "log in", "login"}:
            self.Log.In()

    class Sign:
        class Up:
            def __init__(self, choice, data):
                self.data = data
                if str(choice).upper() == "UP":
                    self.username_check()
                    self.password_check()
                    self.data_setup()
                    self.data_add()

            def username_check(self):
                u_unique = False
                while not u_unique:
                    username = input("Enter a username: ")
                    for users in self.data:
                        if isinstance(users, dict) and username.lower() == str(users.get("USERNAME", "")).lower():
                            print(f"Username: '{username}' is already taken.\nPlease Try Again")
                            break
                    else:
                        self.username = username
                        u_unique = True

            def password_check(self):
                p_same = False
                while not p_same:
                    password1 = input("Enter a password: ")
                    password2 = input("Reenter your password: ")
                    if password1 == password2:
                        self.password = password1
                        p_same = True
                    else:
                        print("the password reentered was not the same as the set password.\nPlease Try Again.")

            def data_setup(self):
                add_data = {
                    "USERNAME": self.username,
                    "PASSWORD": self.password,
                }
                self.data.append(add_data)

            def data_add(self):
                global filefound
                if os.path.exists(acc):
                    filefound = True
                    with open(acc, "w", encoding="utf-8") as file:
                        j.dump(self.data, file)
                else:
                    filefound = False
                    with open(tempacc, "w", encoding="utf-8") as file:
                        j.dump(self.data, file)

        class In:
            def __init__(self):
                pass

            def username_check(self):
                pass

            def password_check(self):
                pass

        class Out:
            pass

    class Log:
        class Register:
            pass

        class In:
            pass

        class Out:
            pass

    def CurrentAccount(self):
        pass

    def __str__(self):
        return str(self.data)

    def RemoveAccount(self):
        pass

    def DeleteAccount(self):
        pass

    def __del__(self):
        pass


if __name__ == "__main__":
    Account(choice="sign up", data=data)
