# # cell phone variables
# carriers = {
#     "vzn": "vtext.com",
#     "att": "txt.att.net",
#     "spr": "sprintpaging.com",
#     "tmb": "tmomail.net",
#     "vgn": "vmobl.com"
# }


# def send_text(message, carrier , phone_number):
#
#     msg = MIMEMultipart()
#
#     msg['From'] = ""
#
#     body = "This is a Text Message."
#
#     msg.attach(MIMEText(body, 'plain'))
#
#     ts = smtplib.SMTP('smtp.gmail.com', 587)
#
#     ts.starttls()
#
#     ts.login(email_address, password)
#
#     text = msg.as_string()
#
#     ts.sendmail(email_address, phone_number, text)
#
#     ts.quit()

# send_text(stock_name + " has changed to " + stock_price, adam_address)

# phone = raw_input('Enter phone number or enter to continue without text alerts: ')

# "2. Enter a phone number (optional) for text alerts or press enter to continue without. \n"