#!/usr/bin/env python3
import logging
from celery_app import app

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app.start()
