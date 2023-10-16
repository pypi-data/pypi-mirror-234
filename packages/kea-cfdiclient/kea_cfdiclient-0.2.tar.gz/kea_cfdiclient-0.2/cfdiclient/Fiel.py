import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_der_x509_certificate

class Fiel:
    def __init__(self, cer_der, key_der, passphrase):
        self.__importar_cer__(cer_der)
        self.__importar_key__(key_der, passphrase)

    def __importar_cer__(self, cer_der):
        # Load the DER certificate
        self.cer = load_der_x509_certificate(cer_der, default_backend())

    def __importar_key__(self, key_der, passphrase):
        try:
            # Import the private key using PKCS#8 format and the provided passphrase
            self.key = serialization.load_der_private_key(key_der, password=passphrase.encode(), backend=default_backend())
        except ValueError:
            raise ValueError('Wrong key password')

    def firmar_sha1(self, texto):
        # Sign with SHA1
        signature = self.key.sign(
            texto,
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        # Convert the signature to base64
        b64_firma = base64.b64encode(signature)
        return b64_firma

    def cer_to_base64(self):
        # Serialize the certificate to DER format
        cer_der = self.cer.public_bytes(encoding=serialization.Encoding.DER)
        # Convert DER to base64
        return base64.b64encode(cer_der)

    def cer_issuer(self):
        # Extract issuer components
        components = self.cer.issuer
        # Generate the issuer string
        return u','.join(['{key}={value}'.format(key=key, value=value) for key, value in components])

    def cer_serial_number(self):
        # Get the serial number of the certificate
        serial = self.cer.serial_number
        # Convert the serial number to a string
        return str(serial)
