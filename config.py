#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os,socketio

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "37a137cd-6495-44f6-885d-106cdde6afe6")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "}T1m:qf^dUH-jhD_JDZ]v}G2KXx23jJ")

