#!/usr/bin/env python3

"""
Simple application to check Todoist inbox
and send mail if sth is inside it
"""

import todoist
import config
import smtplib


api = todoist.TodoistAPI(config.todoist_token)
api.sync()

inbox_items = filter(lambda item: item["project_id"] == config.inbox_project_id ,api.items.all())
inbox_item_contents = list(map( lambda item: item["content"], inbox_items))


if len(inbox_item_contents) > 0:
    subject = "TODOIST REMINDER - You have %s tasks in your inbox to organize" % str(len(inbox_item_contents))
    content = "Hello\n\n\nYou have a few tasks to review: \n\n-" + ("\n-".join(inbox_item_contents))
    message = 'Subject: {}\n\n{}'.format(subject, content)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(config.gmail_user, config.gmail_password)
    server.sendmail(config.gmail_user + "@gmail.com", config.mail_to_send_reminder, message.encode("utf8"))
    server.close()
