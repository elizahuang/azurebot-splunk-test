#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "7481bb21-7632-4dbf-b7d8-4f7c3efcc9e4")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "ElizaHuangTaigidian2021")
