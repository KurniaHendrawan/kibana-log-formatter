#!/usr/bin/env python

# This script parses the logs of the "rasa run" command to JSON.
# OPS1 is monitoring stdout of all containers. OPS1 automatically adds a Kibana index for the JSON "context" key.
# Every line written to stdout needs to have the correct JSON structure or the OPS1 pipeline breaks. Inside "message" you can add keys at will.
# Original: 2020-12-22 15:46:47 INFO     root  - Rasa server is up and running.
# Parsed: {"context":"<$1>","logdate":"2021-01-14T17:42:03.000Z", "message": { "loglevel":"INFO","origin":"root","msg":"Rasa server is up and running."}}

# How to start Rasa: rasa run --enable-api --debug |& python log.py my-context
# |& pipes stdout and stderr to this script (Rasa echos everythin to stderr by default for some reason)


import dateparser
import datetime
import json
import Levenshtein as lev
import sys
import unicodedata

BASE = "vXgnfUuqD88JS8vxtTU4wro4cY6tYxMMLafMSVbQftOPubSAKaHBSM1st4qV6SssC9akWYMH5v3If8YwENczT3KjtTYd1mzIUCjC7fCotu4fLGChqlIgy12qWC1l9w8n4airmuymImozZZMeUlj7o5nlGqLFnhwLZOn6klJeturkAcQhCKOqTbOnN9LNeoEtOrUH1mHvLyubWiI7EwqRP3r8OvGDfpWkf8rHVfB6ZeySfiQWeHtNvziqQkQuyxIoLJn3yJE67jvt0m7zUGxshacft5p6IRK60JJM6vUwiGnm74FaJXpMJJAxQ5fXh70XHLxc8gyc4whLIwpsz00y82SE5QEY4N0nGsApgWXVpAKnWu7s1XPLeqP4qXPwFOXEGkQtJ3Q892umMtk3CKU3LB8tDzYzeOu0KyfEVSjsDIkykh4dh3djc6nWlUnEsaX3HUkex2CbzLkxCN98fDVFzU4dJPB6vSNAbhJaR5qX44v7SX2dxPLpSzZfsICFFpihhrHeYkj56lIARWwOcWHgG3rDWu7ZZj1nZBDkxjhXEvv19Gpe1gKKPqCc4TcafByft5g7vAI3HVqZUwg0lbzD78rBb3TnWbRhd6eHsfOSvcAMNnj5D7EAPPbopXUEPiEudPvCU1Ux2z9zjsD3iQSYvzakqUNFs9PaGKw0NlaT5aMpj9o2OsqV1HJohPIQJnLReCnsX1PNp6FFpDPI85TK2BLtYuFMh2Eu3Q42e1b1mh78C50CHKKx5ynDDRruA9ByidufLkFmTTqZV3gzpndzZjvhcjxF9RLrZ0yYugEPSpQaaToo0jLs0Qpq2P6oEmbyo82sZ1g31Lw1vxpM8FmVaXmWIBYlVBlr0SGZ1kfd5WaX923YejPYc5AomX7mfCg719sP8xk64bogxFy83oaNONNb2tD1Efobo1ZxPcmMkaHHc5HiA9BOBeGPnQUOBMOedb4qpj3ecplNG4JecrIHI7upxJTUQJYd63Y5LMZc" # base string


def transform_log(context, log):
    # 1) A developer logs in the correct format e.g. print('{"context":"chabot-rasa-gs","logdate":"2021-01-
    if log.startswith('{"context":'):
        return log
    splited_log = log.split(None, 4)
    unicodedata.normalize('NFKD', log).encode('ascii', 'ignore')
    log_date = dateparser.parse(" ".join(splited_log[:2]))

    # 2) Correct unknown format e.g. the developer logs with incorrect format or rasa run might potentially log a different format in rare cases.
    if not log_date:
        log_date = datetime.datetime.now()
        splited_log = ["", "", log]

    # 3) Default log format of rasa run
    msg = splited_log[-1]
    if msg.startswith('-'):
        msg = msg.replace('-', '', 1)
    final_log = {
        "context": context,
        "logdate": log_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "message": {
            "loglevel": splited_log[-3],
            "origin": splited_log[-2],
            "msg": msg.strip(),
            "levenshtein": str(round(lev.ratio(BASE, log), 3))
        }
    }
    return json.dumps(final_log)

if __name__ == '__main__':
    context = sys.argv[1]
    for log in sys.stdin:
        print(transform_log(context, log))
