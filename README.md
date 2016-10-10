# firefox-cert-override
`firefox-cert-override` is a Python library and CLI utility for reading and writing `cert_override.txt` files.

`cert_override.txt` is located at the root of a Firefox profile directory and stores the per-domain certificate overrides for that profile. When you permanently add an exception for Firefox to trust a certificate for a specific domain, Firefox adds an entry to `cert_override.txt`, and will read it on startup in the future to load the override again.

## Installation

```sh
$ pip install firefox-cert-override
```

## API
There isn't any documentation for the API (yet), but `firefox_cert_override/base.py` is where the main functionality lives and is a quick skim.

## CLI
The package adds a `firefox-cert-override` command that takes a list of domain and certificate file path pairs and outputs the contents for a `cert_override.txt` file with overrides for the given domains. See `firefox-cert-override --help` for more details.

## License
Licensed under the MIT License. See `LICENSE` for details.
