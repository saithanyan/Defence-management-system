from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'defense_key'

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'  # Your MySQL password here
app.config['MYSQL_DB'] = 'defense_db'  # Database for defense system
mysql = MySQL(app)

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to display available defense assets (military vehicles, tanks, etc.)
@app.route('/assets')
def assets():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM assets")  # Query to fetch defense asset data
    asset_info = cur.fetchall()
    cur.close()
    return render_template('homepage.html', assets=asset_info)

# Route to search assets by ID
@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    search_term = ''
    if request.method == "POST":
        search_term = request.form['asset_id']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM assets WHERE id LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)
        cur.close()
        return render_template('homepage.html', assets=search_results)

# Route to insert a new defense asset (e.g., military vehicle)
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        asset_id = request.form['asset_id']
        name = request.form['name']
        type = request.form['type']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO assets (id, name, type, status) VALUES (%s, %s, %s, %s)", (asset_id, name, type, status))
        mysql.connection.commit()
        return redirect(url_for('assets'))

# Route to delete a defense asset
@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM assets WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('assets'))

# Route to edit asset details (Display the Edit Form)
@app.route('/edit/<string:id_data>', methods=['GET'])
def edit(id_data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM assets WHERE id=%s", (id_data,))
    asset = cur.fetchone()  # Fetch the asset details to edit
    cur.close()
    return render_template('edit_asset.html', asset=asset)

# Route to handle the update of asset details
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        asset_id = request.form['asset_id']
        name = request.form['name']
        type = request.form['type']
        status = request.form['status']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE assets SET name=%s, type=%s, status=%s WHERE id=%s", (name, type, status, asset_id))
        mysql.connection.commit()
        return redirect(url_for('assets'))  # Redirect back to the asset list page

if __name__ == "__main__":
    app.run(debug=True)
