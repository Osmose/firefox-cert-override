import click

from firefox_cert_override.base import CertOverrideEntry, generate_cert_override


@click.command()
@click.argument('overrides', nargs=-1)
def generate(overrides):
    """
    Generates a cert_override.txt file with the given overrides.

    OVERRIDES should be a list of arguments of the form:

        \b
        domain:port=/path/to/certificate.pem[MUT]

    Each argument specifies a domain and port that you want to register
    an override for, and the path to the certificate file that you want
    to accept for that domain:port combination.

    You can optionally include an override mask surrounded by square
    brackets at the end of an entry to specify what types of checks you
    want to override:

        \b
        M meaning hostname-Mismatch-override
        U meaning Untrusted-override
        T meaning Time-error-override (expired/not yet valid)

    By default, all three checks are overridden.
    """
    entries = []
    for override in overrides:
        if '[' in override and override.endswith(']'):
            start = override.find('[')
            mask = override[start + 1:-1]
            override = override[:start]
        else:
            mask = 'MUT'

        try:
            domain, certificate_path = override.split('=')
        except ValueError as err:
            raise click.BadParameter(
                'Override parameters must contain a domain and certificate path separated by an =',
                param_hint='overrides',
            )

        entry = CertOverrideEntry.from_certificate_file(domain, certificate_path, mask=mask)
        entries.append(entry)

    click.echo(generate_cert_override(entries))
