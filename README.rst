Project Overview
================
This repository contains a FastAPI backend service and a Chrome Extension. The FastAPI backend exposes an endpoint that reverses a text string. The Chrome Extension provides a button to capture selected text, send it to the FastAPI service for reversal, and then insert it back.

Directory Structure
-------------------
::

    Project Root
    │
    ├── backend
    │   ├── main.py
    │   ├── pyproject.toml
    │   └── poetry.lock
    │
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

Running the Server
------------------

To run the FastAPI server, execute the following command:


    poetry run uvicorn main:app --reload

The server will start at http://127.0.0.1:8000.


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


