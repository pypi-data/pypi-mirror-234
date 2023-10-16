class FormatStrings:
    
    def format_date(self, fecha_inicial, fecha_final):

        date =  '<u:Timestamp ' \
                'xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" ' \
                'u:Id="_0">' \
                '<u:Created>{created}</u:Created>' \
                '<u:Expires>{expires}</u:Expires>' \
                '</u:Timestamp>'.format(created=fecha_inicial, expires=fecha_final)

        return date
    

    def signature_value(self, digest_value):

        dataToSign = '<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">' \
                     '<CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">' \
                     '</CanonicalizationMethod>' \
                     '<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1">' \
                     '</SignatureMethod><Reference URI="#_0">' \
                     '<Transforms><Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#">' \
                     '</Transform></Transforms>' \
                     '<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>' \
                     '<DigestValue>{digest_value}</DigestValue>' \
                     '</Reference></SignedInfo>'.format(digest_value=digest_value)
        
        return dataToSign
    
    def xml_authentication(self, fecha_inicial, fecha_final, uuid, b64certificate, digest_value, signature_value):
        xml_auth = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" ' \
                    'xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">' \
                    '<s:Header><o:Security s:mustUnderstand="1" ' \
                    'xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">' \
                    '<u:Timestamp u:Id="_0"><u:Created>{created}</u:Created>' \
                    '<u:Expires>{expires}</u:Expires></u:Timestamp>' \
                    '<o:BinarySecurityToken u:Id="{uuid}" ' \
                    'ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" ' \
                    'EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0' \
                    '#Base64Binary">{b64certificate}</o:BinarySecurityToken>' \
                    '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#"><SignedInfo>' \
                    '<CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>' \
                    '<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/><Reference URI="#_0">' \
                    '<Transforms><Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/></Transforms>' \
                    '<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>' \
                    '<DigestValue>{digest_value}</DigestValue></Reference></SignedInfo>' \
                    '<SignatureValue>{signature_value}</SignatureValue>' \
                    '<KeyInfo><o:SecurityTokenReference><o:Reference ' \
                    'ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" ' \
                    'URI="#{uuid}"/></o:SecurityTokenReference></KeyInfo></Signature></o:Security></s:Header>' \
                    '<s:Body><Autentica xmlns="http://DescargaMasivaTerceros.gob.mx"/></s:Body></s:Envelope>'.format(
                    created = fecha_inicial,
                    expires = fecha_final,
                    uuid = uuid,
                    b64certificate = b64certificate,
                    digest_value = digest_value,
                    signature_value = signature_value
                )
        return xml_auth
