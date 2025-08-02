# Secure Chat Verifier
A verifier tool for Secure Chat WhatsApp extension. Verifies the hashchain's files generated.

# How to use

## Requirements
The following software must be installed
- python 3.11.X or higher
- uv (a python environment manager) 0.7.4 or higher

## Procedure

1. Clone this repo.
2. Run ```source .venv/bin/activate```.
3. Put the hashchain you want to verify in a folder inside ./tests/sucess_cases. This directory must contain the public and private logs (jsons) and only these files must be present. Also, the public log filename must start with "public" and the private one with "private". Unwanted exposed messages of the private file can be deleted.
4. Run ```python3 test_suite.py```. This test all files inside ./tests/sucess_cases.

