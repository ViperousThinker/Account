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
                    "emphasis": "\033[1;38;5;150m"
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
                    "emphasis": "\033[1;16;1;20m"
                }

        class Tip:
            def __init__(self):
                self.format = {
                    "call": "\033[4;232;8;241m",
                    "detail": "\033[0;232;8;245m",
                    "normal": "\033[0m",
                    "emphasis": "\033[1;232;8;250m"
                }

class Account:
    def __init__(self, choice, data):
        self.data = data
        self.sign_config = self.Signs()
        self.log_config = self.Log()
        if choice.upper == "SIGN":
                self.sign_config
        elif choice.upper == "LOG":
                self.log_config

    class Signs:
        class Up:
             def __init__(self, choice):
                if choice.upper() == "UP"
                     self.username_check()
                     self.password_check()

             def username_check(self):
                     u_unique = False
                     while u_unique == False:
                        username = input("Enter a username: ")
                        for users in self.data:
                            if username.lower() == users['USERNAME'].lower():
                                u_unique = False
                                print(f"Username: '{username}' is already taken.\nPlease Try Again")
                                break
                        else:
                            u_unique = True
                            break
                        self.username = username

             def password_check(self):
                p_same = False
                while p_same == False:
                    password1 = input("Enter a password: ")
                    password2 = input("Reenter your password: ")
                    if password1 == password2:
                        p_same = True
                        break
                    else:
                        p_same = False
                        print(f"the password reentered was not the same as the set password.\nPlease Try Again.")
                self.password = password1

             def data_setup(self)
                add_data = {
                    "USERNAME": self.username,
                    "PASSWORD": self.password
                }
                self.data.append(add_data)
        
             def data_add():
                    if filefound:
                        with open(acc, 'w') as file:
                            j.dump(self.data, file)
                   else:
                        with open(tempacc, 'w') as file:
                            j.dump(self.data, file)
                                
    def get_registers(self):
        pass

    class Log:
        def __init__(self):
            pass

    def get_logins(self):
        pass

    def CurrentAccount(self):
        pass

    def __str__(self):
        pass

    def signout(self):
        pass

    def get_logouts(self):
        pass

    def RemoveAccount(self):
        pass

    def DeleteAccount(self):
        pass

    def __del__(self):
        pass

try:
    with open(acc, 'r') as file:
        data = j.load(file)
        filefound = True
except FileNotFoundError:
    Handles().warnconfig.FileNotFoundWarn(Ifile="Acc.json", Idir=acc)
    data = []
    filefound = False

Account(data=data).signup()
