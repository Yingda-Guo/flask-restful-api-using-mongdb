import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        pass

server = CustomSMTPServer(('0.0.0.0', 1025), None)

asyncore.loop()