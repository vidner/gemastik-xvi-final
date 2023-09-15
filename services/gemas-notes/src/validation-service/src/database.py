import MySQLdb

# Database configuration
db_config = {
    'host': 'database',
    'user': 'root',
    'passwd': 'why_my_random_string_password_doesnot_working',
    'db': 'gemasnotes',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)