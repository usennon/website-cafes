import smtplib


def send_email(name, map_url, location, cafe_site=None):
    email_from = 'progmvl@gmail.com'
    password = "N)SC#1rMLnKb8(Z"
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=email_from, password=password)
        connection.sendmail(from_addr=email_from,
                            to_addrs='usennon@mail.ru',
                            msg=f'New Cafe Suggestion\n\nCafe name:'
                                f'{name}\nCafe map:{map_url}\nLocation: {location}'
                                f'\nSite: {cafe_site}')
