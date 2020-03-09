import os
import re

from flask import Flask, jsonify, request
import requests, json
from datetime import datetime
from schema import Schema, And, Use, Optional

import logging 

# Files implemented
from models.categoria import categoria
from utils.requestUtils import requestUtils
from utils.exceptionHandler import exceptionHandler


from urllib import parse
import urllib3
import urllib3.exceptions as httpexception

from werkzeug.exceptions import HTTPException, NotFound
