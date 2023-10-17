import os
from laboro.error import LaboroError
from laboro_mail.imap import Client
from tests import init_context
from laboro.logic.processor import Processor
from tests import USERS, IMAP


GOOD_IMAP_ARGS = {"username": USERS[1].get("email"),
                  "password": USERS[1].get("password"),
                  "host": IMAP.get("host"),
                  "port": IMAP.get("port")}
GOOD_IMAP_SSL_ARGS = {"username": USERS[1].get("email"),
                      "password": USERS[1].get("password"),
                      "host": IMAP.get("host"),
                      "port": IMAP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}
GOOD_IMAP_STARTTLS_ARGS = {"username": USERS[1].get("email"),
                           "password": USERS[1].get("password"),
                           "host": IMAP.get("host"),
                           "port": IMAP.get("port"),
                           "starttls": True,
                           "ssl_verify": True}
BAD_AUTH_IMAP_ARGS = {"username": USERS[1].get("email"),
                      "password": "d34dp4rr0t",
                      "host": IMAP.get("host"),
                      "port": IMAP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}


def test_imap_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_ARGS) as client:
    mailbox = "INBOX"
    count = client.get_message_count(mailbox=mailbox)
    assert count == 8


def test_imap_ssl_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    count = client.get_message_count()
    assert count == 8


def test_imap_starttls_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_STARTTLS_ARGS) as client:
    count = client.get_message_count()
    assert count == 8


def test_imap_ssl_bad_auth():
  context = init_context()
  try:
    with Client(context=context,
                args=BAD_AUTH_IMAP_ARGS) as client:
      count = client.get_message_count()
      raise LaboroError("Failed test: test_imap_ssl_bad_auth")
  except LaboroError as err:
    assert str(err).startswith("[ImapCountError] error: b'[AUTHENTICATIONFAILED] Authentication failed.")


def test_get_message():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    number = 1
    message = client.get_message(number=number,
                                 mailbox=mailbox)
    expected_from = f"From: {USERS[0].get('email')}"
    expected_subject = "test_smtp_good 1"
    assert expected_from in message and expected_subject in message


def test_get_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    messages = client.get_messages(mailbox=mailbox)
    assert len(messages) == client.get_message_count(mailbox=mailbox)


def test_get_messages_numbers():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    numbers = client.get_messages_numbers(mailbox=mailbox)
    assert len(numbers) == client.get_message_count(mailbox=mailbox)


def test_tag_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    tags = ["laboro_all"]
    client.tag_messages(mailbox=mailbox,
                        tags=tags)
    numbers = client.get_messages_numbers(mailbox=mailbox,
                                          tags=tags)
    assert len(numbers) == client.get_message_count(mailbox=mailbox)


def test_tag_even_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    all_tags = ["laboro", "remove"]
    odd_tags = ["odd"]
    even_tags = ["even"]
    numbers = client.get_messages_numbers(mailbox=mailbox)
    evens = 0
    for number in numbers:
      if int(number) % 2:
        evens += 1
        client.tag_message(number=number,
                           mailbox=mailbox,
                           tags=even_tags)
      else:
        client.tag_message(number=number,
                           mailbox=mailbox,
                           tags=odd_tags)
      client.tag_message(number=number,
                         mailbox=mailbox,
                         tags=all_tags)
      client.mark_message_as_read(number=number,
                                  mailbox=mailbox)
    even_numbers = client.get_messages_numbers(mailbox=mailbox,
                                               tags=odd_tags,
                                               inverse=True)
    assert len(even_numbers) == evens
    odd_tags = ["odd"]
    odd_numbers = client.get_messages_numbers(mailbox=mailbox,
                                              tags=odd_tags)
    assert len(odd_numbers) == len(numbers) - evens
    all_tags = ["laboro"]
    all_numbers = client.get_messages_numbers(mailbox=mailbox,
                                              tags=all_tags)
    assert len(all_numbers) == len(numbers)


def test_untag_message():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    tags = ["remove"]
    messages = client.get_messages_numbers(mailbox=mailbox,
                                           tags=tags)
    assert len(messages) > 0
    client.untag_messages(mailbox=mailbox, tags=tags)
    assert len(client.get_messages_numbers(mailbox=mailbox,
                                           tags=tags)) == 0


def test_read_unread_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    client.mark_messages_as_unread(mailbox=mailbox)
    assert client.get_unread_messages_numbers(mailbox=mailbox) == \
           client.get_messages_numbers(mailbox=mailbox)
    assert len(client.get_read_messages_numbers(mailbox=mailbox)) == 0
    client.mark_messages_as_read(mailbox=mailbox)
    assert len(client.get_unread_messages_numbers(mailbox=mailbox)) == 0
    assert len(client.get_read_messages_numbers(mailbox=mailbox)) == \
           len(client.get_messages_numbers(mailbox=mailbox))
    client.mark_message_as_unread(number=1, mailbox=mailbox)
    assert bytes(f"{1}", "utf-8") not in client.get_read_messages_numbers(mailbox=mailbox)


def test_untag_even_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    tags = ["even"]
    numbers = client.get_messages_numbers(mailbox=mailbox,
                                          tags=tags)
    for number in numbers:
      if int(number) % 2:
        client.untag_message(number=number,
                             mailbox=mailbox,
                             tags=tags)
      # Number can be bytes or int
      client.untag_message(number=2,
                           mailbox=mailbox,
                           tags=tags)
    numbers = client.get_messages_numbers(mailbox=mailbox,
                                          tags=tags)
    assert len(numbers) == 0


def test_delete_odd_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    tags = ["odd"]
    client.delete_messages(mailbox=mailbox,
                           tags=tags)
    numbers = client.get_messages_numbers(mailbox=mailbox,
                                          tags=tags)
    assert len(numbers) == 0
    count = client.get_message_count(mailbox=mailbox)
    client.delete_message(mailbox=mailbox,
                          number=1)
    assert count == client.get_message_count(mailbox=mailbox) + 1


def test_imap_save_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    filename = Processor.process_arg(context, "$file$test_email.txt")
    number = 2
    client.save_message(number=number,
                        filename=filename)
    message = client.get_message(number=number).replace("\r", "")
    assert os.path.isfile(filename)
    with open(filename, mode="r", encoding="utf-8") as msg:
      assert message == "".join(msg.readlines())


def test_imap_save_messages_to_bad_file():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    filename = "/nobody/expects/the/Spanish/Inquisition.txt"
    try:
      client.save_message(number=1,
                          filename=filename)
      raise LaboroError("Failed test: test_imap_save_messages_to_bad_file")
    except LaboroError as err:
      assert str(err).startswith("[ImapFileError]")


def test_bad_dir_ops():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INB0X"
    try:
      numbers = client.get_message_count(mailbox=mailbox)
      raise LaboroError("Failed test: test_bad_dir_ops 1")
    except LaboroError as err:
      assert str(err).startswith("[ImapCountError]")
    try:
      numbers = client.get_messages_numbers(mailbox=mailbox)
      raise LaboroError("Failed test: test_bad_dir_ops 2")
    except LaboroError as err:
      assert str(err).startswith("[ImapListError]")


def test_bad_message_ops():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    number = 42
    try:
      msg = client.get_message(mailbox=mailbox,
                               number=number)
      raise LaboroError("Failed test: test_bad_message_ops 1")
    except LaboroError as err:
      assert str(err).startswith("[ImapFetchError]")
    try:
      msg = client.delete_message(mailbox=mailbox,
                                  number=number)
      raise LaboroError("Failed test: test_bad_message_ops 2")
    except LaboroError as err:
      assert str(err).startswith("[ImapDeleteError]")


def test_bad_tag():
  context = init_context()
  with Client(context=context,
              args=GOOD_IMAP_SSL_ARGS) as client:
    mailbox = "INBOX"
    tags = [r"\D3l3t3"]
    try:
      msg = client.tag_message(mailbox=mailbox,
                               number=1,
                               tags=tags)
      raise LaboroError("Failed test: test_bad_tag 1")
    except LaboroError as err:
      assert str(err).startswith("[ImapTagError]")
    try:
      msg = client.untag_message(mailbox=mailbox,
                                 number=1,
                                 tags=tags)
      raise LaboroError("Failed test: test_bad_tag 1")
    except LaboroError as err:
      assert str(err).startswith("[ImapTagError]")
