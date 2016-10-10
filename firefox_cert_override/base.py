from base64 import b64encode

from OpenSSL.crypto import FILETYPE_PEM, load_certificate

from firefox_cert_override.utils import b64pad


SHA256_OID = 'OID.2.16.840.1.101.3.4.2.1'


def parse_cert_override(data):
    """
    Parse the contents of a cert_override.txt file and generate
    CertOverrideEntry objects for each entry in the file.
    """
    overrides = []
    for line in data.split('\n'):
        if not line.strip() or line.startswith('#'):
            continue

        try:
            domain, fingerprint_algorithm, fingerprint, mask_string, db_key = line.split('\t')
        except ValueError:
            continue

        entry = CertOverrideEntry(
            domain,
            fingerprint,
            db_key,
            mask=OverrideMask.from_string(mask_string),
            fingerprint_algorithm=fingerprint_algorithm,
        )
        overrides.append(entry)
    return overrides


def generate_cert_override(overrides):
    """
    Generate the contents for a cert_override.txt file with entries for
    the given CertOverrideEntry objects.
    """
    contents = (
        '# PSM Certificate Override Settings file\n'
        '# This is a generated file!  Do not edit.\n'
    )

    for override in overrides:
        contents += '\t'.join([
            override.host + ':' + override.port,
            override.fingerprint_algorithm,
            override.fingerprint,
            str(override.mask),
            override.db_key
        ]) + '\n'

    return contents


class OverrideMask(object):
    """
    Mask that stores what error types are overridden by a specific
    override.
    """
    __slots__ = ('hostname_mismatch', 'untrusted', 'time_error')

    def __init__(self, hostname_mismatch, untrusted, time_error):
        self.hostname_mismatch = hostname_mismatch
        self.untrusted = untrusted
        self.time_error = time_error

    @classmethod
    def from_string(cls, string):
        string = string.upper()
        return cls(
            hostname_mismatch='M' in string,
            untrusted='U' in string,
            time_error='T' in string,
        )

    def __str__(self):
        return ''.join([
            'M' if self.hostname_mismatch else '',
            'U' if self.untrusted else '',
            'T' if self.time_error else '',
        ])

    def __eq__(self, other):
        return str(self) == str(other)


class CertOverrideEntry(object):
    """
    A single entry overriding the certificate checks for a given
    domain/certificate pair.
    """
    def __init__(self, domain, fingerprint, db_key, mask=None, fingerprint_algorithm=SHA256_OID):
        try:
            self.host, self.port = domain.split(':')
        except ValueError as cause:
            error = ValueError('Domain must include both a hostname and a port: {}'.format(domain))
            raise error from cause

        self.fingerprint = fingerprint
        self.fingerprint_algorithm = fingerprint_algorithm
        self.db_key = db_key

        if isinstance(mask, str):
            self.mask = OverrideMask.from_string(mask)
        elif isinstance(mask, OverrideMask):
            self.mask = mask
        elif mask is None:
            self.mask = OverrideMask(False, False, False)
        else:
            raise ValueError('Mask must be a string, OverrideMask instance, or None')

    @classmethod
    def from_certificate(cls, domain, certificate, **kwargs):
        """
        Create a CertOverrideEntry from a domain and PyOpenSSL
        certificate object.
        """
        fingerprint = certificate.digest('sha256').decode('utf-8')

        serial_number = certificate.get_serial_number()
        serial_number = serial_number.to_bytes((serial_number.bit_length() // 8) + 1, 'big')
        issuer = certificate.get_issuer().der()
        db_key = b''.join([
            (0).to_bytes(4, 'big'),
            (0).to_bytes(4, 'big'),
            len(serial_number).to_bytes(4, 'big'),
            len(issuer).to_bytes(4, 'big'),
            serial_number,
            issuer
        ])

        # Encode and pad
        db_key = b64pad(b64encode(db_key)).decode('ascii')
        return cls(domain, fingerprint, db_key, **kwargs)

    @classmethod
    def from_certificate_file(cls, domain, certificate_path, **kwargs):
        """
        Create a CertOverrideEntry from a domain and the certificate
        located at the given path.

        This currently only works with PEM-encoded files.
        """
        with open(certificate_path) as f:
            certificate = load_certificate(FILETYPE_PEM, f.read())
        return cls.from_certificate(domain, certificate, **kwargs)
