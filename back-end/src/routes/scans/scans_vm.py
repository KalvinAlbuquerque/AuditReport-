from flask import Blueprint, request
from flask_cors import cross_origin

from utils.config import Config
from api.tenable_api import TenableApi
import os

tenable_api = TenableApi()
config = Config("config.json")

scans_vm_bp = Blueprint('scansvm', __name__, url_prefix='/scansvm')

@scans_vm_bp.route('/getScanByName/', methods=['POST'])
@cross_origin(origins=["http://localhost:5173", "127.0.0.1"])
def get_vm_scans() -> dict:

    data = request.get_json()

    if not data:
        return "No data provided", 400
    
    name = data.get("name")

    if not name:
        return "Name not provided", 400

    scan = tenable_api.get_vmscans_from_name(name)

    if not scan:
        return "Scan não encontrado.", 404

    return scan, 200