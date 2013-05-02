"""
Testing of SQLite functionality
"""

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from drinkz import db

import sqlite3

db._reset_db()

def test_add_bottles():
    # Tests the SQL database for adding bottles

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    m = db._check_bottle_type_exists('Johnnie Walker', 'Black Label')    
    
    db.save_db('test.sql')
    
    db._reset_db()
    
    db.load_db('test.sql')
    
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    
def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    
    db.save_db('test.sql')
    
    db._reset_db()
    
    db.load_db('test.sql')
    
    assert db.check_inventory('Johnnie Walker', 'Black Label')
