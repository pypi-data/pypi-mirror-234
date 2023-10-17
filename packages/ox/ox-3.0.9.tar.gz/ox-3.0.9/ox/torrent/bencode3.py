##
#
# bencode.py python3 compatable bencode / bdecode
#
##

class Decoder(object):

    def _decode_int(self):
        """
        decode integer from bytearray
        return int
        """
        self.idx += 1
        start = self.idx
        end = self.data.index(b'e', self.idx)
        self.idx = end + 1
        return int(self.data[start:end])

    def _decode_str(self):
        """
        decode string from bytearray
        return string
        """
        start = self.data.index(b':', self.idx)
        l = int(self.data[self.idx:start].decode(), 10)
        if l < 0:
            raise Exception('invalid string size: %d' % l)
        start += 1
        ret = self.data[start:start+l]
        try:
            ret = ret.decode('utf-8')
        except:
            pass
        self.idx = start + l
        return ret

    def _decode_list(self):
        """
        decode list from bytearray
        return list
        """
        ls = []
        self.idx += 1
        while self.data[self.idx] != ord(b'e'):
            ls.append(self._decode())
        self.idx += 1
        return ls

    def _decode_dict(self):
        """
        decode dict from bytearray
        return dict
        """
        d = {}
        self.idx += 1
        while self.data[self.idx] != ord(b'e'):
            k = self._decode_str()
            v = self._decode()
            d[k] = v
        self.idx += 1
        return d

    def _decode(self):
        ch = chr(self.data[self.idx])
        if ch == 'l':
            return self._decode_list()
        elif ch == 'i':
            return self._decode_int()
        elif ch == 'd':
            return self._decode_dict()
        elif ch.isdigit():
            return self._decode_str()
        else:
            raise Exception('could not decode data: %s' % data)

    def decode(self, data):
        self.idx = 0
        self.data = data
        obj = self._decode()
        if len(data) != self.idx:
            raise Exception('failed to decode, extra data: %s' % data)
        return obj

def bdecode(data):
    """
    decode a bytearray
    return decoded object
    """
    return Decoder().decode(data)

def _encode_str(s, buff):
    """
    encode string to a buffer
    """
    s = bytearray(s)
    l = len(s)
    buff.append(bytearray(str(l)+':', 'utf-8'))
    buff.append(s)

def _encode_int(i, buff):
    """
    encode integer to a buffer
    """
    buff.append(b'i')
    buff.append(bytearray(str(i), 'ascii'))
    buff.append(b'e')

def _encode_list(l, buff):
    """
    encode list of elements to a buffer
    """
    buff.append(b'l')
    for i in l:
        _encode(i, buff)
    buff.append(b'e')

def _encode_dict(d, buff):
    """
    encode dict
    """
    buff.append(b'd')
    for k in sorted(d):
        if not isinstance(k, (bytes, str)):
            k = str(k)
        _encode(k, buff)
        _encode(d[k], buff)
    buff.append(b'e')

def _encode(obj, buff):
    """
    encode element obj to a buffer buff
    """
    if isinstance(obj, str):
        _encode_str(bytearray(obj, 'utf-8'), buff)
    elif isinstance(obj, bytes):
        _encode_str(bytearray(obj), buff)
    elif isinstance(obj, bytearray):
        _encode_str(obj, buff)
    elif str(obj).isdigit():
        _encode_int(obj, buff)
    elif isinstance(obj, int):
        _encode_int(obj, buff)
    elif isinstance(obj, list):
        _encode_list(obj, buff)
    elif hasattr(obj, 'keys') and hasattr(obj, 'values'):
        _encode_dict(obj, buff)
    elif str(obj) in ['True', 'False']:
        _encode_int(int(obj and '1' or '0'), buff)
    else:
        raise Exception('non serializable object: %s [%s]' % (obj, type(obj)))


def bencode(obj):
    """
    bencode element, return bytearray
    """
    buff = []
    _encode(obj, buff)
    ret = bytearray()
    for ba in buff:
        ret += ba
    return bytes(ret)
