Project Overview
================
This repository contains a Chrome Extension. The AWS Lambda backend exposes an endpoint that reverses a text string. The Chrome Extension provides a button to capture selected text, send it to AWS Lambda service for reversal, and then insert it back.

Directory Structure
-------------------
::

    Project Root
    │
    ├── backend
    │   ├── main.py
    │   ├── pyproject.toml
    │   └── poetry.lock
    ├── infra
    │   ├── app.py
    │   ├── cdk.json
    │   ├── infra_stack.py
    │   ├── pyproject.toml
    │   └── poetry.lock
    ├── tests
    │   └── test_reverse_text_work_correctly.py
    └── plugin
        ├── popup.html
        ├── popup.js
        └── manifest.json

Getting Started
===============

Prerequisites
-------------
1. Python 3.8 or higher
2. Google Chrome Browser
3. Node.js (Optional, for debugging)
4. Poetry (For Python dependency management)

Backend: FastAPI Service
========================

Installation
------------

1. Navigate to the ``backend`` directory.
2. Initialize and install dependencies using Poetry.

    cd backend

    poetry install

3. Navigate to the ``infra`` directory.
4. Initialize and install dependencies using Poetry.

    cd ../infra

    poetry install

5. Run tests (optional)

    cd tests

    pytest -v

Deployment
------------

Navigate to the ``infra`` directory.

    cd infra

Activate environment (optional):

    poetry shell


Export environment variables for AWS CDK:

    export AWS_ACCESS_KEY_ID=
    export AWS_SECRET_ACCESS_KEY=


To deploy on Mac OS:

    cdk deploy


Plugin: Chrome Extension
========================

Installation
------------

1. Open Google Chrome and go to ``chrome://extensions/``.
2. Turn on Developer Mode.
3. Click ``Load unpacked`` and select the ``plugin`` folder.

Usage
-----

1. Highlight text on any webpage.
2. Click the Chrome Extension icon.
3. Click the "Reverse Text" button.


Contribution and Support
========================

Feel free to contribute to the project or file issues for any questions or problems.


