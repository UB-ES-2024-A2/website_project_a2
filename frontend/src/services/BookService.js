import http from '../http-common'

class BookService {
  readBooks (skip = 0, limit = 100) {
    const config = {
      headers: {
        'accept': 'application/json'
      },
      params: {
        skip: skip,
        limit: limit
      }
    }

    const path = '/api/v1/books'

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  readTop5MatchedBooks (keyword) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = '/api/v1/books/' + keyword

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }

  readBookById (id) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }
    const path = '/api/v1/books/book/' + id

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  filterBooks (genres) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = '/api/v1/books/filter-by-genres'

    return http.post(path, genres, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  getCommentsRatings (bookId) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = `/api/v1/books/CommentRatingPerBook/${bookId}`

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  createCommentRating (bookId, userId, comment, rating) {
    const config = {
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json'
      },
      params: {
        user_id: userId,
        comment: comment,
        rating: rating
      }
    }
    const path = `/api/v1/books/books/${bookId}/comments`

    return http.post(path, {}, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  readMyBooks (idUser) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = `/api/v1/mybooks/${idUser}`

    return http.get(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
  deleteComment (commentId) {
    const config = {
      headers: {
        'accept': 'application/json'
      }
    }

    const path = `/api/v1/books/CommentRatingPerBook/${commentId}`

    return http.delete(path, config)
      .then((res) => {
        return res
      })
      .catch((error) => {
        return Promise.reject(error)
      })
  }
}

export default new BookService()
