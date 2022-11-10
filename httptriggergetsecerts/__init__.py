import logging
import os
import json

import azure.functions as func


def main(req: func.HttpRequest) -> str:
    logging.info('Python HTTP trigger function processed a request.')
    apim_key = os.getenv("apim_key")

    return func.HttpResponse(
        json.dumps(apim_key),
        mimetype="application/json",
    )
