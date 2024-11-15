from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('comments.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT, timestamp TEXT, upvotes INTEGER)')
        db.commit()
        db.close()

init_db()

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments ORDER BY timestamp DESC').fetchall()
    conn.close()

    if request.method == 'POST':
        comment = request.form['comment']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        conn.execute('INSERT INTO comments (comment, timestamp, upvotes) VALUES (?, ?, 0)', (comment, timestamp))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('index.html', comments=comments)

@app.route('/upvote/<int:comment_id>', methods=['POST'])
def upvote(comment_id):
    conn = get_db_connection()

    # Update the upvote count in the database
    conn.execute('UPDATE comments SET upvotes = upvotes + 1 WHERE id = ?', (comment_id,))
    conn.commit()

    # Get the updated upvote count
    updated_count = conn.execute('SELECT upvotes FROM comments WHERE id = ?', (comment_id,)).fetchone()[0]
    conn.close()

    return jsonify({'upvote_count': updated_count})

if __name__ == '__main__':
    app.run(debug=True)