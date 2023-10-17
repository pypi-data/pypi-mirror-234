import os
from laboro.error import LaboroError
from laboro_mail.smtp import Client
from tests import init_context
from tests import USERS, ATTACHMENTS, SMTP


ATTACHMENTS_FILES = ATTACHMENTS.get("files")
GOOD_SMTP_ARGS = {"username": USERS[0].get("email"),
                  "password": USERS[0].get("password"),
                  "host": SMTP.get("host"),
                  "port": SMTP.get("port")}
GOOD_SMTP_SSL_ARGS = {"username": USERS[0].get("email"),
                      "password": USERS[0].get("password"),
                      "host": SMTP.get("host"),
                      "port": SMTP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}
GOOD_SMTP_STARTTLS_ARGS = {"username": USERS[0].get("email"),
                           "password": USERS[0].get("password"),
                           "host": SMTP.get("host"),
                           "port": SMTP.get("port"),
                           "starttls": True,
                           "ssl_verify": True}
BAD_AUTH_SMTP_ARGS = {"username": USERS[0].get("email"),
                      "password": "d34dp4rr0t",
                      "host": SMTP.get("host"),
                      "port": SMTP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}


def test_smtp_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_ARGS) as client:
    sender = USERS[0].get("email")
    recipients = [USERS[1].get("email")]
    subject = "test_smtp_good 1"
    body = "test_smtp_good 1"
    args = {"sender": sender,
            "subject": subject,
            "recipients": recipients,
            "body": body}
    client.send(**args)


def test_smtp_starttls_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_STARTTLS_ARGS) as client:
    sender = USERS[0].get("email")
    recipients = [USERS[1].get("email")]
    subject = "test_smtp_starttls_good 1"
    body = "test_smtp_starttls_good 1"
    args = {"sender": sender,
            "subject": subject,
            "recipients": recipients,
            "body": body}
    client.send(**args)


def test_smtp_ssl_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_SSL_ARGS) as client:
    sender = USERS[0].get("email")
    recipients = [USERS[1].get("email")]
    subject = "test_smtp_ssl_good 1"
    body = "test_smtp_ssl_good 1"
    args = {"sender": sender,
            "subject": subject,
            "recipients": recipients,
            "body": body}
    client.send(**args)


def test_smtp_ssl_good_with_attachment():
  context = init_context()
  wksp_dir = context.workspace.workspace_dir
  with Client(context=context,
              args=GOOD_SMTP_SSL_ARGS) as client:
    sender = USERS[0].get("email")
    recipients = [USERS[1].get("email")]
    subject = "test_smtp_ssl_good_with_attachment 1"
    body = "test_smtp_ssl_good_with_attachment 1"
    attachments = [os.path.join(wksp_dir, ATTACHMENTS.get("dir"), att)
                   for att in ATTACHMENTS_FILES]
    args = {"sender": sender,
            "subject": subject,
            "recipients": recipients,
            "body": body,
            "attachments": attachments}
    # We need 2 mails with attachments for POP/IMAP tests
    client.send(**args)
    client.send(**args)


def test_smtp_ssl_good_with_cc():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_SSL_ARGS) as client:
    sender = USERS[0].get("email")
    recipients = [USERS[1].get("email")]
    cc = [user.get("email") for user in USERS]
    subject = "test_smtp_ssl_good_with_cc 1"
    body = "test_smtp_ssl_good_with_cc 1"
    args = {"sender": sender,
            "subject": subject,
            "recipients": recipients,
            "body": body,
            "cc": cc}
    client.send(**args)


def test_smtp_ssl_good_with_bcc():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_SSL_ARGS) as client:
    sender = USERS[0].get("email")
    bcc = [user.get("email") for user in USERS]
    subject = "test_smtp_ssl_good_with_bcc 1"
    body = "test_smtp_ssl_good_with_bcc 1"
    args = {"sender": sender,
            "subject": subject,
            "body": body,
            "bcc": bcc}
    client.send(**args)


def test_smtp_ssl_bad_rcpt():
  context = init_context()
  with Client(context=context,
              args=GOOD_SMTP_SSL_ARGS) as client:
    try:
      sender = USERS[0].get("email")
      bcc = ["ken.shabby@flying.circus"]
      subject = "test_smtp_ssl_bad_rcpt 1"
      body = "test_smtp_ssl_bad_rcpt 1"
      args = {"sender": sender,
              "subject": subject,
              "body": body,
              "bcc": bcc}
      client.send(**args)
      raise LaboroError("Failed test: test_smtp_ssl_bad_rcpt 1")
    except LaboroError as err:
      assert str(err).startswith(f"[SmtpSendError] SMTPRecipientsRefused {bcc[0]}")
    try:
      sender = USERS[0].get("email")
      recipients = ["ken.shabby@flying.circus", USERS[1].get("email")]
      subject = "test_smtp_ssl_bad_rcpt 1"
      body = "test_smtp_ssl_bad_rcpt 1"
      args = {"sender": sender,
              "subject": subject,
              "body": body,
              "recipients": recipients}
      client.send(**args)
      raise LaboroError("Failed test: test_smtp_ssl_bad_rcpt 2")
    except LaboroError as err:
      assert str(err).startswith(f"[SmtpSendError] LaboroError Rejected: <{recipients[0]}>")


def test_smtp_ssl_bad_auth():
  context = init_context()
  try:
    with Client(context=context,
                args=BAD_AUTH_SMTP_ARGS) as client:
      sender = USERS[0].get("email")
      recipients = ["ken.shabby@flying.circus", USERS[1].get("email")]
      subject = "test_smtp_ssl_bad_rcpt 1"
      body = "test_smtp_ssl_bad_rcpt 1"
      args = {"sender": sender,
              "subject": subject,
              "body": body,
              "recipients": recipients}
      client.send(**args)
      raise LaboroError("Failed test: test_smtp_ssl_bad_auth")
  except LaboroError as err:
    assert str(err).startswith("[SmtpSendError] SMTPAuthenticationError")


def test_smtp_ssl_no_recpt():
  context = init_context()
  try:
    with Client(context=context,
                args=GOOD_SMTP_SSL_ARGS) as client:
      sender = USERS[0].get("email")
      subject = "test_smtp_ssl_no_recpt 1"
      body = "test_smtp_ssl_no_recpt 1"
      args = {"sender": sender,
              "subject": subject,
              "body": body}
      client.send(**args)
      raise LaboroError("Failed test: test_smtp_no_rcpt")
  except LaboroError as err:
    assert str(err).startswith("[SmtpEnvelopeError] One of recipients, cc or bcc must be filled")
