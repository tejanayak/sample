import unittest
import requests
import time

class TestBookAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    def setUp(self):
        # Ensure the API is up (optional, since Jenkins starts it)
        time.sleep(2)  # Wait for the server to start

    def test_create_and_get_book(self):
        # Create a book
        create_response = requests.post(
            f"{self.BASE_URL}/books",
            json={"title": "Test Book", "author": "Test Author", "publication_year": 2023}
        )
        self.assertEqual(create_response.status_code, 201)
        book_id = create_response.json().get("id")

        # Get the created book
        get_response = requests.get(f"{self.BASE_URL}/books/{book_id}")
        self.assertEqual(get_response.status_code, 200)
        book = get_response.json()
        self.assertEqual(book["title"], "Test Book")
        self.assertEqual(book["author"], "Test Author")
        self.assertEqual(book["publication_year"], 2023)

    def test_get_nonexistent_book(self):
        # Try to get a book with an invalid ID
        response = requests.get(f"{self.BASE_URL}/books/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get("error"), "Book not found")

    def test_update_book(self):
        # Create a book
        create_response = requests.post(
            f"{self.BASE_URL}/books",
            json={"title": "Original Book", "author": "Original Author", "publication_year": 2020}
        )
        book_id = create_response.json().get("id")

        # Update the book
        update_response = requests.put(
            f"{self.BASE_URL}/books/{book_id}",
            json={"title": "Updated Book", "author": "Updated Author", "publication_year": 2021}
        )
        self.assertEqual(update_response.status_code, 200)

        # Verify the update
        get_response = requests.get(f"{self.BASE_URL}/books/{book_id}")
        book = get_response.json()
        self.assertEqual(book["title"], "Updated Book")
        self.assertEqual(book["author"], "Updated Author")
        self.assertEqual(book["publication_year"], 2021)

    def test_delete_book(self):
        # Create a book
        create_response = requests.post(
            f"{self.BASE_URL}/books",
            json={"title": "Delete Book", "author": "Delete Author", "publication_year": 2022}
        )
        book_id = create_response.json().get("id")

        # Delete the book
        delete_response = requests.delete(f"{self.BASE_URL}/books/{book_id}")
        self.assertEqual(delete_response.status_code, 200)

        # Verify deletion
        get_response = requests.get(f"{self.BASE_URL}/books/{book_id}")
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()