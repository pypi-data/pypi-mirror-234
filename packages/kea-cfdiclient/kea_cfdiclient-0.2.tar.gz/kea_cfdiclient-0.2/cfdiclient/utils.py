import xml.etree.ElementTree as ET
from base64 import b64encode
import hashlib
import random

class Utils():

    def b64_sha1_digest(self, data):
        digest_value = b64encode(hashlib.sha1(data.encode()).digest()).decode('ascii')
        return digest_value
        
    def xml_etree(self, xml):
    # Define una función para eliminar los prefijos de los nombres de espacio XML

        """def strip_namespace(element):
            if '}' in element.tag:
                element.tag = element.tag.split('}', 1)[1]

            # Recursivamente, procesa los elementos hijos
            for child in element:
                strip_namespace(child)"""

        # Parsea el XML de entrada
        root = ET.fromstring(xml)

        # Elimina los prefijos de los nombres de espacio
        #strip_namespace(root)

        # Convierte el elemento root en un árbol ElementTree
        tree = ET.ElementTree(root)

        return tree
    
    def headers(self, xml, soapAction, token=None):
        dictHeaders = {
            'Content-type': 'text/xml;charset="utf-8"',
            'Accept': 'text/xml',
            'cache-control': 'no-cache',
            'SOAPAction': soapAction,
            #'Content-length': str(sys.getsizeof(xml)),
        }
        
        if token is not None:
            dictHeaders.update({'Authorization': 'WRAP access_token="{token}"'.format(token=token)})
        
        return dictHeaders
    
    def generateUUID(self):
        uuid = '{normal:04x}{normal:04x}-{normal:04x}-{0:04x}-{1:04x}-{normal:04x}{normal:04x}{normal:04x}'.format(
            random.randint(0, 0x0fff) | 0x4000,
            random.randint(0, 0x3fff) | 0x8000,
            normal=random.randint(0, 0xffff),
        )

        uuid = 'uuid-' + uuid + '-1'

        return uuid
