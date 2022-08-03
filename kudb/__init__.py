"""
# kudb

Simple document database
"""

from .kudb import connect, close, get_key, get_by_id, set_key, get_keys, \
    kvs_json, delete_key, get_info, change_db, clear_keys, \
    get_all, recent, get, insert, find, update, delete, clear, clear_doc, \
    MEMORY_FILE, insert_many

__version__ = "0.1.7"
