from .database_utils import get_connection

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self._id = id
        self._title = title
        self._author_id = author_id
        self._magazine_id = magazine_id
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        # Title is immutable after initialization in the requirements
        if hasattr(self, '_title') and self._title is not None:
            raise AttributeError("Title cannot be changed after initialization")
        self._title = value
    
    @classmethod
    def new_from_db(cls, row):
        """Create an Article instance from a database tuple/row."""
        return cls(row[0], row[1], row[2], row[3])
    
    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls.new_from_db(row)
        return None
    
    def save(self):
        """Save (INSERT or UPDATE) the article to the database."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self._id is None:
            # INSERT new article
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (self._title, self._author_id, self._magazine_id)
            )
            self._id = cursor.lastrowid
        else:
            # UPDATE existing article
            cursor.execute(
                "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                (self._title, self._author_id, self._magazine_id, self._id)
            )
        
        conn.commit()
        conn.close()
        return self
    
    @property
    def author(self):
        """Return the Author object for this article."""
        from .author import Author
        return Author.find_by_id(self._author_id)
    
    @author.setter
    def author(self, author_obj):
        """Set the author using an Author object."""
        from .author import Author
        if not isinstance(author_obj, Author):
            raise ValueError("Must provide an Author object")
        self._author_id = author_obj.id
    
    @property
    def magazine(self):
        """Return the Magazine object for this article."""
        from .magazine import Magazine
        return Magazine.find_by_id(self._magazine_id)
    
    @magazine.setter
    def magazine(self, magazine_obj):
        """Set the magazine using a Magazine object."""
        from .magazine import Magazine
        if not isinstance(magazine_obj, Magazine):
            raise ValueError("Must provide a Magazine object")
        self._magazine_id = magazine_obj.id