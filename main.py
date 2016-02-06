#!/usr/bin/env python
# -*- coding: utf-8 -*-

from imgurpython import ImgurClient
from email.mime.text import MIMEText
from email.header import Header
from random import randrange
from smtplib import SMTP_SSL
import config, os

save_file = config.PATH
last_img = None
subject = u'Hallo meine süBe freundin'
body = u""

client = ImgurClient(config.CLIENT_ID,
                     config.CLIENT_SECRET_KEY,
                     config.ACCESS_TOKEN,
                     config.REFRESH_TOKEN)
all_pictures = client.get_gallery_favorites(config.USERNAME)

with open(save_file) as f:
    last_img = f.readlines()
    if last_img:
        last_img = last_img[0]

recent_items = list(reversed(all_pictures[:10]))
if recent_items and last_img != all_pictures[0].link:
    for item in recent_items:
        link = item.link
        if not last_img:
            if link and link[-3:] == 'gif' and link[-5] == 'h':
                link = link[:-5] + '.gif'
            body += link + "\r\n"
        if link == last_img:
            last_img = None
    if recent_items[-1]:
        with open(save_file, "w") as f:
            f.write(recent_items[-1].link)
if body:
    body = u"All the pictures! Tell your amazing Boyfriend if something is broken!\r\n\r\n" + body
else:
    body = u"Oooo Noooies. There aren't any new pictures today. That's a really sad story. :(("

if len(all_pictures) > 200:
    old_item = all_pictures[randrange(0, len(all_pictures) - 150)].link
    if old_item and old_item[-3:] == 'gif' and old_item[-5] == 'h':
        old_item = old_item[:-5] + '.gif'
    body += u"\r\n\r\nHere's a random old image: " + old_item + "\r\n"

body += u"\r\n\r\nLove you!"

message = MIMEText(body, _charset="UTF-8")
message['Subject'] = Header(subject, "utf-8")

server = SMTP_SSL(u'smtp.gmail.com:465')
server.ehlo()
server.login(config.FROM_EMAIL, config.EMAIL_PASSWORD)
server.sendmail(config.FROM_EMAIL, config.TO_EMAILS, message.as_string())
server.quit()
