import ssl
import poplib
from laboro.error import LaboroError
from laboro.module import Module
from laboro_mail.ciphers import DEFAULT_CIPHERS
from laboro_mail.files import save_email


class Client(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a basic POP3 client able to manage incoming email operations using the POP3 protocol.

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

  def __exit__(self, type_err, value, traceback):
    self._close()

  def connect(self):
    try:
      self._connect()
    except poplib.error_proto as err:
      err_msg = f"{err.__class__.__name__} {err}"
      if self.args.get("exit_on_error"):
        self.context.log.critical(err_msg)
        raise err
      self.context.log.warning(err_msg)

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
      self.client = poplib.POP3_SSL(host=self.args.get("host"),
                                    port=self.args.get("port"),
                                    timeout=self.args.get("timeout"),
                                    context=ctx)
    else:
      self.client = poplib.POP3(host=self.args.get("host"),
                                port=self.args.get("port"),
                                timeout=self.args.get("timeout"))
      if self.args.get("starttls"):
        self.context.log.info("Using STARTTLS")
        response = self.client.stls(context=ctx)
    if self.args.get("username") is not None:
      self.context.log.debug("Authentication...")
      try:
        try:
          self.client.utf8()
        except poplib.error_proto:
          pass
        self.client.user(self.args.get("username"))
        self.client.pass_(self.args.get("password"))
      except Exception as err:
        raise err
    self._connected = True

  def _close(self):
    if self.connected:
      self.client.quit()
    self._connected = False

  @Module.laboro_method
  def get_message_count(self):
    """Return the number of available emails.

    Returns:
      ``int``: Number of available emails on the remote server.
    """
    return len(self.get_messages_numbers())

  @Module.laboro_method
  def get_messages_numbers(self):
    """Return the number of each email available on the remote server.

    Returns:
      list: List of ``int``.
    """
    self.context.log.info("Getting available mails count...")
    try:
      if not self.connected:
        self.connect()
      return [int(mid.decode("utf-8").split()[0]) for mid in self.client.list()[1]]
    except Exception as err:
      err_msg = f"[PopListError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_message(self, number):
    """Return the message identified by the give number.

    Arguments:
      ``number``: Int. The email number.

    Returns:
      ``string``. The string representation of the email identified by the give number.
    """
    self.context.log.info("Retrieving email...")
    try:
      if not self.connected:
        self.connect()
      return "\n".join([line.decode("utf-8")
                        for line in self.client.retr(number)[1]])
    except poplib.error_proto as err:
      err_msg = f"[PopRetrError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def get_all_messages(self):
    """Return all emails available on the remote server.

    Returns:
      ``List``. List of strings representation of each email.
    """
    messages = list()
    mids = self.get_messages_numbers()
    for mid in mids:
      messages.append(self.get_message(number=mid))
    return messages

  @Module.laboro_method
  def delete_message(self, number):
    """Delete from the remote server the message identified by the give number.

    Arguments:
      ``number``: Int. The email number to be deleted.
    """
    self.context.log.info("Deleting email...")
    try:
      if not self.connected:
        self.connect()
      return self.client.dele(number)
    except poplib.error_proto as err:
      err_msg = f"[PopDeleteError] {err}"
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def delete_all_messages(self):
    """Delete all emails available ont the remote server.
    """
    count = self.get_message_count()
    while count > 0:
      self.delete_message(number=count)
      count = self.get_message_count()

  @Module.laboro_method
  def save_message(self, number, filename):
    """Save the message identified by the give number to the specified file,

    If the email contains attachments, a directory named after the specified file name and with the ".attachments" extension will be created and all attachments stored into it.

    Arguments:
      ``number``: Int. The number of the email to save.
      ``filename``: String. The complete path to the file where to save the email.

    Returns:
      ``dict``. A two keys dictionary containing the file name where the email has been saved and the list of attachments file names.

      ..  code-block:: python

        {"filename": "/path/to/file",
         "attachments": ["/path/to/file.attachments/attachements_1.txt",
                         "/path/to/file.attachments/attachements_2.txt]}
    """
    self.context.log.info(f"Saving email to file: {filename}")
    mail = self.get_message(number=number)
    try:
      return save_email(email_as_string=mail,
                        filename=filename)
    except Exception as err:
      err_msg = f"[PopFileError] {err.__class__.__name__}: {err}"
      raise LaboroError(err_msg) from err
