import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to create a connection to the MySQL database
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # e.g., 'localhost'
            user='root',  # e.g., 'root'
            password='99999??',
            database='source'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Create table if it doesn't exist
def create_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        age INT
    )'''
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

# Insert user data into the table
def insert_user(conn, name, email, age):
    query = '''
    INSERT INTO users (name, email, age) VALUES (%s, %s, %s)
    '''
    cursor = conn.cursor()
    cursor.execute(query, (name, email, age))
    conn.commit()

# Fetch all user data from the table
def fetch_users(conn):
    query = '''
    SELECT * FROM users
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Streamlit app
st.title('User Information Collection')

# Establish connection to the database
conn = create_connection()
if conn:
    create_table(conn)

    # Form to collect user information
    with st.form(key='user_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        age = st.number_input('Age', min_value=0, max_value=120)
        submit_button = st.form_submit_button(label='Submit')

    # Save data to the database
    if submit_button:
        if name and email and age:
            insert_user(conn, name, email, age)
            st.success('User information saved successfully!')
        else:
            st.error('Please fill in all fields')

    # Display saved data
    if st.checkbox('Show user data'):
        users = fetch_users(conn)
        st.write(users)

    # Close the database connection when the app is done
    conn.close()
else:
    st.error('Failed to connect to the database')

