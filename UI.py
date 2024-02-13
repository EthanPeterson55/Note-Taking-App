import requests
import logging

CREATE_NOTE_URL = 'http://localhost:5002'
RETRIEVE_NOTE_URL = 'http://localhost:5001'
DELETE_NOTE_URL = 'http://localhost:5003'

def display_menu():
    print("Note Taking Application")
    print("Enter a value 1-4:")
    print("(1) Create New Note")
    print("(2) View Existing Note")
    print("(3) Delete Note")
    print("(4) Quit")

def retrieve_note(title):
    response = requests.get(f'{RETRIEVE_NOTE_URL}/retrieve_note/{title}')
    if response.status_code == 200:
        note_data = response.json()
        title = note_data['title']
        content = note_data['content']
        print(f"Note Retrieved: {title}\n{content}")
    else:
        print("Note not found")

def create_note():
    note_data = input("Enter your Note title followed by a comma and your note contents: ")
    title, content = note_data.split(',', 1)
    response = requests.post(f'{CREATE_NOTE_URL}/create_note', json={'title': title, 'content': content})
    if response.status_code == 201:
        print("Note Created:", title)
    else:
        print("Failed to create note")

def delete_note(title):
    response = requests.delete(f'{DELETE_NOTE_URL}/delete_note/{title}')
    if response.status_code == 200:
        print("Note Deleted:", title)
    else:
        print("Failed to delete note")

def main():
    try:
        display_menu()

        while True:
            # Wait for user input
            choice = input("Enter your choice: ")

            # Perform action based on user input
            if choice == '1':
                create_note()
            elif choice == '2':
                note_title = input("Enter the Note title you wish to access: ")
                retrieve_note(note_title)
            elif choice == '3':
                note_title = input("Enter the Note title you wish to delete: ")
                delete_note(note_title)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    except Exception as e:
        print("An error occurred within main():", e)

if __name__ == "__main__":
    main()