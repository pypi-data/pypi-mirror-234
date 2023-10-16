import getpass
import itertools
import qtc.env_config as ecfg
import qtc.utils.endpoint_utils as epu

_BASE_SALT = 'QuantTrading'


def intersperse(str1: str, str2: str) -> str:
    """Mixes together two strings.  If one string is longer, the shorter sting is cycled.
    >>> import qtc.utils.cipher_utils as cu
    >>> cu.intersperse('foo', 'bar')
    'fboaor'
    >>> cu.intersperse('steven', '_-')
    's_t-e_v-e_n-'
    """
    piece_len = max(len(str1), len(str2))
    combined = [None] * 2 * piece_len
    # Mypy doesn't understand that that strings behave as iterable things?  If
    # we let this type float to the 'intersperse' signature, the rest of the
    # file gets ugly.
    combined[0::2] = itertools.islice(itertools.cycle(str1), piece_len) # type: ignore
    combined[1::2] = itertools.islice(itertools.cycle(str2), piece_len) # type: ignore
    return ''.join(map(str, combined))


def scramble(secret: str, *, salt: str = 'AbCdEfG') -> bytes:
    """Apply a salt to a secret string using xor.
    >>> import qtc.utils.cipher_utils as cu
    >>> str(cu.scramble('ABC', salt='ABC'))
    "b'\\\\x00\\\\x00\\\\x00'"
    >>> str(cu.scramble('ABCABC', salt='ABC'))
    "b'\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00'"
    >>> str(cu.scramble('AAA', salt='ABC'))
    "b'\\\\x00\\\\x03\\\\x02'"
    >>> str(cu.scramble('AAAAAA', salt='ABC'))
    "b'\\\\x00\\\\x03\\\\x02\\\\x00\\\\x03\\\\x02'"
    """
    return bytes((ord(a) ^ ord(b)) for (a, b) in zip(secret, itertools.cycle(salt)))


def to_salted(text: str, user: str = None) -> str:
    """Encode a text string by salt
    >>> import qtc.utils.cipher_utils as cu
    >>> cu.to_salted(text='Hello World')
    '0a040d0403552e0e130417'
    """
    if user is None:
        user = getpass.getuser()
    salt = intersperse(_BASE_SALT, user)
    secret = scramble(text, salt=salt)
    secret_str = ''.join('{:02x}'.format(b) for b in secret)
    return secret_str


def from_salted(secret_str: str, user: str = None) -> str:
    """Decodes a salted string
    >>> import qtc.utils.cipher_utils as cu
    >>> cu.from_salted(secret_str='0a040d0403552e0e130417')
    'Hello World'
    """
    if user is None:
        user = getpass.getuser()
    salt = intersperse(_BASE_SALT, user)
    secret_chars = bytearray.fromhex(secret_str)
    secret = ''.join([chr(b) for b in secret_chars])
    return ''.join([chr(b) for b in scramble(secret, salt=salt)])


def get_token():
    url = ecfg.get_env_config().get('token_service.base_url')
    return epu.process_request(request_url=url, is_post=False,
                               data_transmission_protocol='TXT')
