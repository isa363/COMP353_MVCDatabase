from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Database connection (adjust host/user/database as needed)
db_config = {
    'host': 'nuc353.encs.concordia.ca',
    'user': 'nuc353_1',
    'password': os.getenv("MYSQL_PASSWORD", "your-fallback-password"),
    'database': 'nuc353_1',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Members")
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('members.html', members=members)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        fields = ["mID", "NAS", "medicare", "phone", "address", "city", "province", "postalCode",
                  "type", "firstName", "lastName", "genre", "birth", "height", "weight", "age"]
        values = [request.form.get(f) for f in fields]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Members (mID, NAS, medicare, phone, address, city, province, postalCode,
                    type, firstName, lastName, genre, birth, height, weight, age)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/members')
        except mysql.connector.Error as err:
            return f"Error: {err}"
    return render_template('add_member.html')

# You can add other routes like /memberships, /personnel, etc.

if __name__ == '__main__':
    # Use the PORT Render provides or default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
