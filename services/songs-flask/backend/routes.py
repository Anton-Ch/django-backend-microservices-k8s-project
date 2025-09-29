from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys
from urllib.parse import urlparse


# Load .env from the service root (services/songs-flask/.env)
# Use os.path on purpose (explicit and consistent across the codebase).
try:
    from dotenv import load_dotenv
    SERVICE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
    load_dotenv(os.path.join(SERVICE_ROOT, ".env"))
except Exception:
    # If python-dotenv is not installed, the app can still read real env vars
    pass


# Build the MongoDB URI from MONGO_URI or (as a fallback) from component vars.
def build_mongo_uri() -> str:
    """
    Resolve the final Mongo connection string:
    1) If MONGO_URI is set in .env vars, use it as-is.
    2) Otherwise build it from .env var components:
       MONGO_APP_USERNAME, MONGO_APP_PASSWORD, MONGODB_HOST, MONGODB_PORT,
       MONGO_DB, MONGO_AUTH_SOURCE.
    """
    uri = os.getenv("MONGO_URI")
    if uri:
        return uri

    # fallback part
    host = os.getenv("MONGODB_HOST", "localhost")
    port = int(os.getenv("MONGODB_PORT", "27017"))
    dbn = os.getenv("MONGO_DB", "app_db")

    user = os.getenv("MONGO_APP_USERNAME")
    pwd = os.getenv("MONGO_APP_PASSWORD")

    # Default authSource: app_db (where the app user lives).
    # If you intend to use root instead, set MONGO_AUTH_SOURCE=admin in .env.
    auth_source = os.getenv("MONGO_AUTH_SOURCE", dbn)

    if user and pwd:
        return f"mongodb://{user}:{pwd}@{host}:{port}/{dbn}?authSource={auth_source}"
    # Fallback without auth (useful for dev-only scenarios with disabled auth)
    return f"mongodb://{host}:{port}/{dbn}"


# Resolve the final Mongo URI and connect
MONGO_URL = build_mongo_uri()
app.logger.info(f"Connecting to Mongo: {MONGO_URL}")

try:
    client = MongoClient(MONGO_URL)
except OperationFailure as e:
    app.logger.error(f"Mongo authentication error: {str(e)}")
    raise

# Pick DB name from URI path (or default to 'app_db')
try:
    parsed = urlparse(MONGO_URL)
    DB_NAME = (parsed.path.lstrip("/") or "app_db").split("?")[0]
except Exception:
    DB_NAME = "app_db"


db = client[DB_NAME]


# Bootstrap data from JSON (lab-style): drop and seed the 'songs' collection.
# NOTE: This is for the learning lab to ensure deterministic tests.
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
try:
    with open(json_url, "r", encoding="utf-8") as fh:
        songs_list = json.load(fh)
    # For reproducible tests we reset the collection:
    db.songs.drop()
    if songs_list:
        db.songs.insert_many(songs_list)
except FileNotFoundError:
    app.logger.warning("songs.json not found; skipping bootstrap seeding.")

def parse_json(data):
    """Serialize Mongo objects (ObjectId, datetime) into JSON-safe structures."""
    return json.loads(json_util.dumps(data))

######################################################################
# SYSTEM ENDPOINTS
######################################################################

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify(status="OK"), 200

@app.route("/count", methods=["GET"])
def count():
    """Return number of documents in the 'songs' collection."""
    total = db.songs.count_documents({})
    return jsonify(count=total), 200

######################################################################
# CRUD ENDPOINTS
######################################################################
@app.route("/song", methods=["GET"])
def songs():
    songs = list(db.songs.find({}))
    return {"songs": parse_json(songs)}, 200


@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = db.songs.find_one({"id":id})
    if song:
        return parse_json(song), 200
    return jsonify({"Message": f"song with id {id} not found"}), 404


# def get_song_by_id(id): ...
# def create_song(): ...
# def update_song(id): ...
# def delete_song(id): ...
