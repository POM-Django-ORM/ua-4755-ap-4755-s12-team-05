from django.db import models

class Book(models.Model):
    """
    This class represents a Book. 
    Attributes:
    -----------
    param name: Describes name of the book
    type name: str max_length=128
    param description: Describes description of the book
    type description: str
    param count: Describes count of the book
    type count: int default=10
    param authors: list of Authors
    type authors: list->Author
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    count = models.IntegerField(default=10)
    authors = models.ManyToManyField('author.Author', related_name='books')

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        author_ids = [author.id for author in self.authors.all()]
        return f"ID: {self.id}, Name: {self.name}, Description: {self.description}, Count: {self.count}, Authors: {author_ids}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f"{self.__class__.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        """
        :param book_id: SERIAL: the id of a Book to be found in the DB
        :return: book object or None if a book with such ID does not exist
        """
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(book_id):
        """
        :param book_id: an id of a book to be deleted
        :type book_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return True
        except Book.DoesNotExist:
            return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        param authors: list of Authors
        type authors: list->Author
        :return: a new book object which is also written into the DB
        """
        if name and len(name) <= 128:
            book = Book.objects.create(
                name=name, 
                description=description, 
                count=count
            )
            if authors:
                # Використовуємо .set() для додавання списку авторів після створення книги
                book.authors.set(authors)
            return book
        return None

    def to_dict(self):
        """
        :return: book id, book name, book description, book count, book authors
        :Example:
        | {
        |   'id': 8,
        |   'name': 'django book',
        |   'description': 'bla bla bla',
        |   'count': 10,
        |   'authors': []
        | }
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'authors': [author.id for author in self.authors.all()]
        }

    def update(self, name=None, description=None, count=None):
        """
        Updates book in the database with the specified parameters.
        param name: Describes name of the book
        type name: str max_length=128
        param description: Describes description of the book
        type description: str
        param count: Describes count of the book
        type count: int default=10
        :return: None
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        """
        Add authors to book in the database with the specified parameters.
        param authors: list authors
        :return: None
        """
        if authors:
            # Символ * розпаковує список, оскільки метод .add() приймає аргументи через кому
            self.authors.add(*authors)

    def remove_authors(self, authors):
        """
        Remove authors to book in the database with the specified parameters.
        param authors: list authors
        :return: None
        """
        if authors:
            self.authors.remove(*authors)

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all books
        """
        return list(Book.objects.all())