from flask import Flask, request, jsonify
import sqlite3
import logging
import threading

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Function to create SQLite connection and cursor in the context of each thread
def get_db():
    db = getattr(threading.current_thread, 'db', None)
    if db is None:
        db = threading.current_thread.db = sqlite3.connect('notes.db')
    return db, db.cursor()

# Close database connection at the end of each request
@app.teardown_appcontext
def close_db(exception):
    db = getattr(threading.current_thread, 'db', None)
    if db is not None:
        db.close()

@app.route('/create_note', methods=['POST'])
def create_note():
    try:
        db, c = get_db()
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if title and content:
            # Insert the note into the 'notes' table
            c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            db.commit()  # Commit the transaction
            print("Note created: ", title)
            return jsonify({'message': 'Note created successfully'}), 201
        else:
            return jsonify({'error': 'Title and content are required'}), 400
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Replace 5001 with the desired port number
