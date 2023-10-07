from eptools import SalesForceApiIntegration as sf, slacker
try:
    sf.loadGlobals()
    print(sf.getParentAccountEmail(7255))
    print(sf.getEmailFromDB(7255))
except Exception as e:
    print(e)

try:
    s = slacker.Slacker()
    s.send_Custom_Message("CMV74FWRZ","Final test")
except Exception as ex:
    print(ex)