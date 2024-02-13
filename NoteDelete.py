from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Function to open a new database connection
def get_db():
    return sqlite3.connect('notes.db')

@app.route('/delete_note/<title>', methods=['DELETE'])
def delete_note(title):
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM notes WHERE title=?", (title,))
            conn.commit()  # Commit the transaction

            if c.rowcount > 0:
                return jsonify({'message': 'Note deleted successfully'}), 200
            else:
                return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)  # Replace 5001 with the desired port number