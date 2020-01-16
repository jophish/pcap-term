from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
import curses
from curses import wrapper
import json

_COOKIES_FILE = 'cookies.json'

pc = PersonalCapital()

email, password = "email", "password"
try:
    with open('cookies.json') as fd:
        cookies = json.load(fd)
        pc.set_session(cookies)
        pc.login(email, password)
except FileNotFoundError:
    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, input('code: '))
        pc.authenticate_password(password)
        cookies = pc.get_session()
        with open('cookies.json', 'w') as fd:
            json.dump(cookies, fd)

accounts_response = pc.fetch('/newaccount/getAccounts')
accounts = accounts_response.json()['spData']

print('Networth: {0}'.format(accounts['networth']))

curses.noecho()
curses.cbreak()

stdscr = curses.initscr()
stdscr.keypad(True)


curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
