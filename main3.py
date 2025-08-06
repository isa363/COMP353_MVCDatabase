from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_key'

MYSQL_PASSWORD = "7h3ldn8P"

db_config = {
    'host': 'nuc353.encs.concordia.ca',
    'user': 'nuc353_1',
    'password': MYSQL_PASSWORD,
    'database': 'nuc353_1',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/members')
def show_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mID, firstName, lastName FROM Members")
    members = cursor.fetchall()
    conn.close()
    return render_template('members.html', members=members)

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            mID = request.form['mID']
            NAS = request.form['NAS']
            medicare = request.form['medicare']
            phone = request.form['phone']
            address = request.form['address']
            city = request.form['city']
            province = request.form['province']
            postalCode = request.form['postalCode']
            type_ = request.form['type']
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            genre = request.form['genre']
            birth = request.form['birth']
            height = request.form['height']
            weight = request.form['weight']
            age = request.form['age']

            query = """
                INSERT INTO Members (mID, NAS, medicare, phone, address, city, province, postalCode,
                    type, firstName, lastName, genre, birth, height, weight, age)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (mID, NAS, medicare, phone, address, city, province, postalCode,
                      type_, firstName, lastName, genre, birth, height, weight, age)
            cursor.execute(query, values)
            conn.commit()
            flash('Member successfully added!', 'success')
            return redirect(url_for('show_members'))
        except mysql.connector.Error as e:
            conn.rollback()
            flash(f"Error adding member: {str(e)}", 'error')
            return redirect(url_for('add_member'))
        finally:
            conn.close()

    return render_template('add_member.html')

@app.route('/employees')
def show_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pID, firstName, lastName FROM Personnel")
    employees = cursor.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/families')
def show_families():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fID, firstName, lastName FROM FamilyMembers")
    families = cursor.fetchall()
    conn.close()
    return render_template('families.html', families=families)

@app.route('/clubs')
def show_clubs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, city, website, phone FROM ClubLocations")
    clubs = cursor.fetchall()
    conn.close()
    return render_template('clubs.html', clubs=clubs)

@app.route('/teams')
def show_teams():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Teams.teamID, Teams.teamName, Teams.teamGenre, TeamLocations.clubName
        FROM Teams
        JOIN TeamLocations ON Teams.teamID = TeamLocations.teamID
    """)
    teams = cursor.fetchall()
    conn.close()
    return render_template('teams.html', teams=teams)

@app.route('/memberships')
def show_memberships():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mID, clubName, active FROM Memberships")
    memberships = cursor.fetchall()
    conn.close()
    return render_template('memberships.html', memberships=memberships)

if __name__ == '__main__':
    app.run(debug=True)
