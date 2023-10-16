import smtplib
import re
import dns.resolver
import socket


REGEXR_EMAIL = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'


def check_email(email_address:str, dns_checker=False, recipient_checker=False):
    try:
        addressToVerify = email_address
        match = re.match(REGEXR_EMAIL, addressToVerify)

        if match == None:
            print('Error invalid email ' + addressToVerify)
            raise ValueError('Bad Syntax')

        if not dns_checker and not recipient_checker:
            return True

        domain_name = email_address.split('@')[1]

        records = dns.resolver.resolve(domain_name, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        host = socket.gethostname()

        server = smtplib.SMTP()
        server.set_debuglevel(0)

        server.connect(mxRecord)
        server.helo(host)

        if dns_checker and not recipient_checker:
            server.quit()
            return True

        server.mail('info@domain.com')
        code, message = server.rcpt(str(addressToVerify))
        server.quit()

        return code == 250
    except:
        return False