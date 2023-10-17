import os
from laboro.error import LaboroError
from laboro_mail.pop import Client
from tests import init_context
from laboro.logic.processor import Processor
from tests import USERS, POP


GOOD_POP3_ARGS = {"username": USERS[0].get("email"),
                  "password": USERS[0].get("password"),
                  "host": POP.get("host"),
                  "port": POP.get("port")}
GOOD_POP3_SSL_ARGS = {"username": USERS[0].get("email"),
                      "password": USERS[0].get("password"),
                      "host": POP.get("host"),
                      "port": POP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}
GOOD_POP3_SSL_ARGS2 = {"username": USERS[1].get("email"),
                       "password": USERS[1].get("password"),
                       "host": POP.get("host"),
                       "port": POP.get("ssl").get("port"),
                       "ssl": True,
                       "ssl_verify": True}
GOOD_POP3_STARTTLS_ARGS = {"username": USERS[0].get("email"),
                           "password": USERS[0].get("password"),
                           "host": POP.get("host"),
                           "port": POP.get("port"),
                           "starttls": True,
                           "ssl_verify": True}
BAD_AUTH_POP3_ARGS = {"username": USERS[0].get("email"),
                      "password": "d34dp4rr0t",
                      "host": POP.get("host"),
                      "port": POP.get("ssl").get("port"),
                      "ssl": True,
                      "ssl_verify": True}


def test_pop_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_ARGS) as client:
    count = client.get_message_count()
    assert isinstance(count, int)


def test_pop_ssl_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    count = client.get_message_count()
    assert isinstance(count, int)


def test_pop_starttls_good():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_STARTTLS_ARGS) as client:
    count = client.get_message_count()
    assert isinstance(count, int)


def test_pop_ssl_bad_auth():
  context = init_context()
  try:
    with Client(context=context,
                args=BAD_AUTH_POP3_ARGS) as client:
      count = client.get_message_count()
      raise LaboroError("Failed test: test_pop_ssl_bad_auth")
  except LaboroError as err:
    assert str(err).startswith("[PopListError] error_proto: b'-ERR [AUTH] Authentication failed.")


def test_pop_get_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    count = client.get_message_count()
    messages = client.get_all_messages()
    assert isinstance(messages, list)
    assert len(messages) == count


def test_pop_save_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS2) as client:
    filename = Processor.process_arg(context, "$file$test_email.txt")
    number = 5
    client.save_message(number=number,
                        filename=filename)
    message = client.get_message(number=number)
    assert os.path.isfile(filename)
    with open(filename, mode="r", encoding="utf-8") as msg:
      assert message == "".join(msg.readlines())


def test_pop_save_messages_to_bad_file():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS2) as client:
    filename = "/nobody/expects/the/Spanish/Inquisition.txt"
    try:
      client.save_message(number=1,
                          filename=filename)
      raise LaboroError("Failed test: test_pop_save_messages_to_bad_file")
    except LaboroError as err:
      assert str(err).startswith("[PopFileError] FileNotFoundError")


def test_pop_delete_messages():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    client.delete_all_messages()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    assert client.get_message_count() == 0


def test_get_bad_message():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    try:
      client.get_message(number=42)
      raise LaboroError("Failed test: test_get_bad_message")
    except LaboroError as err:
      assert str(err).startswith("[PopRetrError]")


def test_delete_bad_message():
  context = init_context()
  with Client(context=context,
              args=GOOD_POP3_SSL_ARGS) as client:
    try:
      client.delete_message(number=42)
      raise LaboroError("Failed test: test_delete_bad_message")
    except LaboroError as err:
      assert str(err).startswith("[PopDeleteError]")
