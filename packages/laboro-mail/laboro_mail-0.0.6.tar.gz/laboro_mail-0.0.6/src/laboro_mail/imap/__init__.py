import ssl
import imaplib
from laboro.error import LaboroError
from laboro.module import Module
from laboro_mail.ciphers import DEFAULT_CIPHERS
from laboro_mail.files import save_email


SEEN_FLAG = "\\Seen"
DELETE_FLAG = "\\Deleted"


class Client(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a basic IMAP client able to manage incoming email operations using the IMAP protocol.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.

    ``username``: String. Optional. The user name used for authentication on remote POP3 server if needed.
    ``password``: String. Optional, The password used for authentication on remote POP3 server if needed.
    ``host``: String. Optional. The remote POP3 server to connect to. Default to ``localhost``
    ``port``: Int. Optional. The TCP remote port to connect to. Default to ``110``.
    ``ssl``: Boolean. Optional. When set to ``True``, the connection will use a SSL encrypted socket. Default to ``False``.
    ``starttls``: Boolean. Optional. When set to ``True``, SSL negotiation will done using the ``STARTTLS`` command. Default to ``False``.
    ``ssl_verify``: Boolean. Optional. Whether the remote server SSL certificate must be verified when using ``ssl`` or ``starttls``. Default to ``True``.
    ``timeout``: Int. Optional. The connection timeout. Default to ``60``.
    ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will be logged as a warning. When set to ``True``, exit the workflow if any error is encountered. Default: ``True``.

    Note: The ``ssl`` and ``starttls`` arguments are mutually exclusive. You may user either one of them or none but not both at the same time.
  """
  @property
  def connected(self):
    return self.client is not None and self._connected

  def __init__(self, context, args=None):
    super().__init__(filepath=__file__, context=context, args=args)
    self.client = None
    self._connected = False
    self.exit_on_error = True

  def connect(self):
    try:
      self._connect()
    except imaplib.IMAP4.error as err:
      err_msg = f"{err.__class__.__name__} {err}"
      if self.args.get("exit_on_error"):
        self.context.log.critical(err_msg)
        raise err
      self.context.log.warning(err_msg)

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    if self.args.get("ssl") or self.args.get("starttls"):
      self.context.log.info("Creating secure connection...")
      ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
      ctx.options |= ssl.OP_NO_SSLv2
      ctx.options |= ssl.OP_NO_SSLv3
      ctx.set_ciphers(DEFAULT_CIPHERS)
      ctx.check_hostname = False
      ctx.verify_mode = ssl.CERT_NONE
      if self.args.get("ssl_verify"):
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = True
        ctx.set_default_verify_paths()
        ctx.load_default_certs()
    self.context.log.info(f"Connecting to {self.args.get('host')}:{self.args.get('port')}")
    if self.args.get("ssl"):
      self.client = imaplib.IMAP4_SSL(host=self.args.get("host"),
                                      port=self.args.get("port"),
                                      timeout=self.args.get("timeout"),
                                      ssl_context=ctx)
    else:
      self.client = imaplib.IMAP4(host=self.args.get("host"),
                                  port=self.args.get("port"),
                                  timeout=self.args.get("timeout"))
      if self.args.get("starttls"):
        self.context.log.info("Using STARTTLS")
        response = self.client.starttls(ssl_context=ctx)
    if self.args.get("username") is not None:
      self.context.log.debug("Authentication...")
      try:
        self.client.login(user=self.args.get("username"),
                          password=self.args.get("password"))
        self.client.enable("UTF8=ACCEPT")
      except Exception as err:
        raise err
    self.client.select()
    self._connected = True

  def _close(self):
    if self.connected:
      try:
        self.client.close()
      except imaplib.IMAP4.error:
        pass
      self.client.logout()
    self._connected = False

  @Module.laboro_method
  def list_mailbox(self, mailbox="INBOX"):
    """
    List all sub-mailboxes of the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox to browse. Default to ``INBOX``

    Returns:
      ``list``: List of strings. The list of sub-mailboxes (directories) found in the specified mailbox.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    if not self.connected:
      self.connect()
    self.client.select(mailbox=mailbox)
    try:
      self.context.log.info("Listing available mailboxes...")
      resp, dirs = self.client.lsub(directory=mailbox,
                                    pattern="*")
      return [d.decode('utf-8').split()[2] for d in dirs]
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapListsubError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_message_count(self, mailbox="INBOX"):
    """Return the number of available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``

    Returns:
      ``int``: Number of available emails on the remote server in the specified mailbox.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      self.context.log.info("Getting available emails count...")
      self.client.select(mailbox=mailbox)
      resp, data = self.client.search(None, 'ALL')
      return len(data[0].decode("utf-8").split())
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapCountError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_messages_numbers(self, mailbox="INBOX", tags=None, inverse=False):
    """Return the list of emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

      ..  code-block:: python

        client.get_messages_numbers(mailbox="INBOX",
                                    tags=["laboro", "rocks"],
                                    inverse=False):

      Will return the list of email numbers tagged ``laboro`` or ``rocks`` available in the ``INBOX`` mailbox directory.

      ..  code-block:: python

        client.get_messages_numbers(mailbox="INBOX",
                                    tags=["laboro", "rocks"],
                                    inverse=True):

      Will return the list of email numbers neither tagged ``laboro`` or ``rocks`` available in the ``INBOX`` mailbox directory.

      If ``tags`` is not specified, the method will return the list of all available emails numbers in the specified mailbox.

    Returns:
      ``list``: List of available emails numbers matching specified criteria and mailbox.

    Raises:
      ``laboro.error.LaboroError``: Notably when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      self.context.log.info("Getting available mails numbers...")
      self.client.select(mailbox=mailbox)
      resp, data = self.client.search(None, 'ALL')
      uids = [uid for uid in data[0].split()]
      if tags is not None:
        select = list()
        for uid in uids:
          resp, flags = self.client.fetch(uid, "(FLAGS)")
          flags = [flag.decode("utf-8")
                   for flag in imaplib.ParseFlags(flags[0])]
          if inverse:
            if set(tags).isdisjoint(flags):
              select.append(uid)
          else:
            if not set(tags).isdisjoint(flags):
              select.append(uid)
        return select
      return uids
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapListError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_unread_messages_numbers(self, mailbox="INBOX"):
    """Return the list of unread emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``list``: List of unread emails numbers matching specified mailbox.
    """
    return self.get_messages_numbers(mailbox=mailbox,
                                     tags=[SEEN_FLAG],
                                     inverse=True)

  @Module.laboro_method
  def get_read_messages_numbers(self, mailbox="INBOX"):
    """Return the list of read emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``list``: List of read emails numbers matching specified mailbox.
    """
    return self.get_messages_numbers(mailbox=mailbox,
                                     tags=[SEEN_FLAG],
                                     inverse=False)

  @Module.laboro_method
  def get_message(self, number, mailbox="INBOX"):
    """Get the email specified by its number from the specified mailbox.

    Arguments:
      ``number``: The email number to retrieve.
      ``mailbox``: Optional. Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``string``: The string representation of the email.

    Raises:
      ``laboro.error.LaboroError``: When the specified email number does not match any available email.
    """
    try:
      if not self.connected:
        self.connect()
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      typ, data = self.client.fetch(number, '(RFC822)')
      return data[0][1].decode("utf-8")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapFetchError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_messages(self, mailbox="INBOX", tags=None, inverse=False):
    """Return the list of available emails in the specified mailbox and matching the specified criteria.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

    Returns:
      ``list``: List of string representations of all emails matching specified criteria and mailbox.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    messages = list()
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=inverse)
    for uid in uids:
      messages.append(self.get_message(mailbox=mailbox,
                                       number=uid))
    return messages

  @Module.laboro_method
  def tag_message(self, number, tags, mailbox="INBOX"):
    """Add one or more tags to the specified email.

    Arguments:
      ``number``: The email number.
      ``tags``: A list of string that will be used as tags to be added to the email.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      self.context.log.info("Tagging email...")
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      for tag in tags:
        self.client.store(number, "+FLAGS", fr"({tag})")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapTagError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def untag_message(self, number, tags, mailbox):
    """Remove one or more tags to the specified email.

    Arguments:
      ``number``: The email number.
      ``tags``: A list of string that will be used as tags to be removed from the email.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      self.context.log.info("Untagging email...")
      if not self.connected:
        self.connect()
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      for tag in tags:
        self.client.store(number, "-FLAGS", fr"({tag})")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapTagError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def mark_message_as_read(self, number, mailbox="INBOX"):
    """Mark the specified email as 'read'.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    self.tag_message(mailbox=mailbox,
                     number=number,
                     tags=[SEEN_FLAG])

  @Module.laboro_method
  def mark_message_as_unread(self, number, mailbox="INBOX"):
    """Mark the specified email as 'unread'.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    self.untag_message(mailbox=mailbox,
                       number=number,
                       tags=[SEEN_FLAG])

  @Module.laboro_method
  def tag_messages(self, tags, mailbox="INBOX"):
    """Tag all emails in the specified mailbox with one or more tags.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: A list of string that will be used as tags to be added to each email.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=True)
    for uid in uids:
      self.tag_message(mailbox=mailbox,
                       number=uid,
                       tags=tags)

  @Module.laboro_method
  def untag_messages(self, mailbox, tags):
    """Remove one or more tags to all emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: A list of string that will be used as tags to be removed from each email.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags)
    for uid in uids:
      self.untag_message(mailbox=mailbox,
                         number=uid,
                         tags=tags)

  @Module.laboro_method
  def mark_messages_as_read(self, mailbox="INBOX"):
    """Mark all emails in the specified mailbox as 'read'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    self.tag_messages(mailbox=mailbox,
                      tags=[SEEN_FLAG])

  @Module.laboro_method
  def mark_messages_as_unread(self, mailbox="INBOX"):
    """Mark all emails in the specified mailbox as 'unread'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    self.untag_messages(mailbox=mailbox,
                        tags=[SEEN_FLAG])

  @Module.laboro_method
  def delete_message(self, number, mailbox="INBOX"):
    """Delete the specified email in the specified mailbox.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``laboro.error.LaboroError``: When no email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      self.context.log.info("Deleting email...")
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      self.client.store(number, "+FLAGS", DELETE_FLAG)
      self.client.expunge()
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapDeleteError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def delete_messages(self, mailbox="INBOX", tags=None, inverse=False):
    """Delete all emails matching the specified criteria'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

    Raises:
      ``laboro.error.LaboroError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=inverse)
    for uid in sorted(uids, reverse=True):
      self.delete_message(mailbox=mailbox,
                          number=uid)

  @Module.laboro_method
  def save_message(self, number, filename, mailbox="INBOX"):
    """Save the message identified by the give number to the specified file,

    If the email contains attachments, a directory named after the specified file name and with the ".attachments" extension will be created and all attachments stored into it.

    Arguments:
      ``number``: Int. The number of the email to save.
      ``filename``: String. The complete path to the file where to save the email.
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``

    Returns:
      ``dict``. A two keys dictionary containing the file name where the email has been saved and the list of attachments file names.

      ..  code-block:: python

        {"filename": "/path/to/file",
         "attachments": ["/path/to/file.attachments/attachements_1.txt",
                         "/path/to/file.attachments/attachements_2.txt]}
    """
    self.context.log.info(f"Saving email to file: {filename}")
    mail = self.get_message(mailbox=mailbox,
                            number=number)
    try:
      return save_email(email_as_string=mail,
                        filename=filename)
    except Exception as err:
      err_msg = f"[ImapFileError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err
