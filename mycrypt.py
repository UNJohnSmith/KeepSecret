from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class MyCrypt():
    def __init__(self, key):

        if len(key.encode('utf8'))>16:
            raise RuntimeError('Must Under 16 Digits')
        self.key = key.encode('utf8').zfill(16)
        self.mode = AES.MODE_CBC


    def encrypt(self, text):

        cryptor = AES.new(self.key, self.mode, self.key)

        text = text.encode('utf8')
        add = -(len(text) % -16)
        text = text + (b' ' * add)

        return cryptor.encrypt(text)

    def decrypt(self, text):

        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(text)
        plain_text = plain_text.rstrip(b' ').decode('utf8')
        return plain_text


if __name__ == '__main__':
    pass
