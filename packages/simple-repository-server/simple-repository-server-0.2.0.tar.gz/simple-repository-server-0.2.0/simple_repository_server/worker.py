# Copyright (C) 2023, CERN
# This software is distributed under the terms of the MIT
# licence, copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.

from uvicorn.workers import UvicornWorker


class ProxyHeadersWorker(UvicornWorker):
    """Custom configuration of the uvicorn worker usable with gunicorn.
    By setting "proxy_headers" the source address is replaced with the
    value in the X-Forwarded-For if it's set.
    """
    CONFIG_KWARGS = {**UvicornWorker.CONFIG_KWARGS, "proxy_headers": True}
