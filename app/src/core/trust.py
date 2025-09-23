from OpenSSL import crypto

def parse_certificate(cert_file_path: str) -> dict:
    with open(cert_file_path, "rb") as f:
        pem_data = f.read()
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem_data)
    subject = cert.get_subject()
    issuer = cert.get_issuer()

    def name_to_dict(name):
        return {type_bytes.decode(): value_bytes.decode() for type_bytes, value_bytes in name.get_components()}

    return {
        "subject": name_to_dict(subject),
        "issuer": name_to_dict(issuer),
        "serial_number": str(cert.get_serial_number()),
        "not_valid_before": cert.get_notBefore().decode('ascii'),
        "not_valid_after": cert.get_notAfter().decode('ascii'),
        "version": cert.get_version(),
    }