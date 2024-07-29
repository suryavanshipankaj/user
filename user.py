

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

st.title('User Information Form')

# Form inputs
with st.form(key='user_form'):
    username = st.text_input('Username')
    email = st.text_input('Email')
    age = st.number_input('Age', min_value=0)
    submit_button = st.form_submit_button(label='Submit')

# Save form data to CSV
if submit_button:
    # Create a DataFrame from the input data
    user_data = pd.DataFrame({
        'Username': [username],
        'Email': [email],
        'Age': [age]
    })
    
    # Save the DataFrame to a CSV file
    user_data.to_csv('user_data.csv', index=False)
    st.success('Form data saved to CSV file.')

# Upload CSV data to the database
if st.button('Upload to Database'):
    # Create a SQLAlchemy engine
    engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    # Read the CSV file
    user_data = pd.read_csv('user_data.csv')
    
    # Upload the data to the database
    user_data.to_sql('users', engine, if_exists='append', index=False)
    st.success('CSV data uploaded to the database.')

# Run the Streamlit app
if __name__ == '__main__':
    st.write('Fill in the form and submit, then click "Upload to Database" to save the data.')
