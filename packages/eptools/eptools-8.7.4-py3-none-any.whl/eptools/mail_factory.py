from eptools.configuration import *

from O365 import Account

# Utils
# ---

def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        after_func_new_globals = getglobals()
        # keep own globals rather than getglobals after func
        after_func_new_globals.update(globals())
        globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

loadconfigwithfile = reloadconfig(loadconfigwithfile)
loadconfigwithjson = reloadconfig(loadconfigwithjson)


# Mail Factory
# ---
# This Python module can be used to send emails using the no-reply mailaddress.

class MailFactory:
    @reloadconfig
    def __init__(self, config_path=None) -> None:
        loadconfigwithfile(config_path)

        self.credentials = (globals()['C_O365_CLIENT_ID'], globals()['C_O365_CLIENT_SECRET'],)
        self.account = Account(self.credentials, auth_flow_type='credentials', tenant_id=globals()['C_O365_TENANT_ID'], main_resource='noreply@easypost.eu')
       
        if not self.account.is_authenticated:
            self.account.authenticate()
       
    def send_mail(self, receivers, subject, body) -> None:
        msg = self.account.new_message()
        
        for receiver in receivers:
            msg.to.add(receiver)
            
        msg.subject = subject
        msg.body = body
        msg.send()


# Testing
# ---
       
if __name__ == "__main__":
    mail_factory = MailFactory()
    
    receivers = ['kirsten.vermeulen@easypost.eu']
    subject = "no-reply: New eptools feature launched!"
    body = """
        <html>
            <head>
                <style>
                p {margin: 0;}
                </style>
            </head>
            <body>
                <p>Hi!</p>
                <br/>
                <p>*beep boop*</p>
                <br/>
                <p>Just wanted to let you know that you can now send mails using this new eptools feature (MailFactory).</p>
                <br/>
                <p>See you later *beep boop*</p>
                <p>🤖 Easybot</p>
            </body>
        </html>
    """
    
    mail_factory.send_mail(receivers, subject, body)