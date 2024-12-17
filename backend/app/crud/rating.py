""" User related CRUD methods """
from typing import Any

def create_rating(*, cursor, id: int, user_id: int, comment: str, rating: int) -> None:
    """
    Inserts a new comment and rating for a specific book into the database and updates the book's average rating.

    Args:
        cursor (cursor): The database cursor for executing the SQL queries.
        id (int): The ID of the book being rated.
        user_id (int): The ID of the user providing the rating.
        comment (str): The comment provided by the user.
        rating (int): The rating given by the user.

    Returns:
        None
    """
    # Insertar comentario y calificación
    query_insert = """
                    INSERT INTO CommentRatingPerBook (IdUser, IdBook, Comment, Rating)
                    VALUES (%s, %s, %s, %s)
                """
    cursor.execute(query_insert, (user_id, id, comment, rating))

    query_avg_rating = "SELECT AVG(Rating) FROM CommentRatingPerBook WHERE IdBook = %s"
    cursor.execute(query_avg_rating, (id,))
    avg_rating = cursor.fetchone()[0]

    query_update_book = "UPDATE Books SET Rating = %s WHERE IdBook = %s"
    cursor.execute(query_update_book, (avg_rating, id))

def get_ratings(*, cursor, book_id: int) -> Any:
    """
    Retrieves all comments and ratings for a specific book.

    Args:
        cursor (cursor): The database cursor for executing the SQL query.
        book_id (int): The ID of the book whose ratings are to be retrieved.

    Returns:
        Any: A list of tuples containing the comment ID, user ID, comment text, rating, and username of the user.
    """
    query_get_comments = """
                SELECT crp.IdCommentRating, crp.IdUser, crp.Comment, crp.Rating, u.username
                FROM CommentRatingPerBook crp
                JOIN users u ON crp.IdUser = u.id_user
                WHERE crp.IdBook = %s
            """
    cursor.execute(query_get_comments, (book_id,))
    rows = cursor.fetchall()

    return rows

def get_rating_by_id(*, cursor, comment_id: int) -> Any:
    """
    Retrieves the book ID associated with a specific comment ID.

    Args:
        cursor (cursor): The database cursor for executing the SQL query.
        comment_id (int): The ID of the comment to be checked.

    Returns:
        Any: The ID of the book related to the comment, or None if the comment does not exist.
    """
    # Verificar que el comentario existe
    query_check_comment = "SELECT * FROM CommentRatingPerBook WHERE IdCommentRating = %s"
    cursor.execute(query_check_comment, (comment_id,))
    result = cursor.fetchone()

    return result

def delete_rating(*, cursor, comment_id: int) -> None:
    """
    Deletes a specific comment and rating from the database.

    Args:
        cursor (cursor): The database cursor for executing the SQL query.
        comment_id (int): The ID of the comment to be deleted.

    Returns:
        None
    """
    query_delete = "DELETE FROM CommentRatingPerBook WHERE IdCommentRating = %s"
    cursor.execute(query_delete, (comment_id,))

def calculate_rating(*, cursor, book_id: int):
    """
    Calculates the average rating for a specific book.

    Args:
        cursor (cursor): The database cursor for executing the SQL query.
        book_id (int): The ID of the book for which the average rating needs to be calculated.

    Returns:
        None
    """
    query_avg_rating = "SELECT AVG(Rating) FROM CommentRatingPerBook WHERE IdBook = %s"
    cursor.execute(query_avg_rating, (book_id,))

def get_books_with_ratings_by_user(*, cursor, user_id: int, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieves all books rated by a specific user, including their ratings, with pagination support.

    Args:
        cursor: The database cursor used for executing queries.
        user_id (int): The ID of the user whose ratings are to be retrieved.
        skip (int, optional): The number of books to skip for pagination (default is 0).
        limit (int, optional): The maximum number of books to retrieve (default is 100).

    Returns:
        Any: An object containing the list of books with their ratings and the total count of rated books.
    """

    # Consulta para obtener los libros puntuados por el usuario
    query_books = """
        SELECT 
            b.IdBook as id_book, 
            b.Title as title, 
            b.Authors as authors, 
            b.Synopsis as synopsis, 
            b.BuyLink as buy_link, 
            b.Genres as genres, 
            b.Rating as book_rating, 
            b.Editorial as editorial, 
            b.Comments as comments, 
            b.PublicationDate as publication_date, 
            b.Image as image,
            r.Rating as user_rating
        FROM 
            Books b
        INNER JOIN 
            CommentRatingPerBook r ON b.IdBook = r.IdBook
        WHERE 
            r.IdUser = %s
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query_books, (user_id, limit, skip))
    rows = cursor.fetchall()

    # Contar el total de libros puntuados por el usuario
    query_count = """
        SELECT COUNT(1)
        FROM CommentRatingPerBook r
        WHERE r.IdUser = %s
    """
    cursor.execute(query_count, (user_id,))
    count = cursor.fetchone()[0]

    # Transformar las filas obtenidas en una lista de objetos con libros y puntuaciones
    books_with_ratings = [
        {
            "book": {
                "id_book": row[0],
                "title": row[1],
                "authors": row[2],
                "synopsis": row[3],
                "buy_link": row[4],
                "genres": row[5],
                "rating": row[6],
                "editorial": row[7],
                "comments": row[8],
                "publication_date": row[9].isoformat() if row[9] else None,  # Convertir a cadena
                "image": row[10]
            },
            "user_rating": row[11]  # Rating given by the user
        } for row in rows
    ]

    return {"data": books_with_ratings, "count": count}
