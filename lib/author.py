from .database_utils import get_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @classmethod
    def new_from_db(cls, row):
        """Create an Author instance from a database tuple/row."""
        return cls(row[0], row[1])
    
    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls.new_from_db(row)
        return None
    
    def save(self):
        """Save (INSERT or UPDATE) the author to the database."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self._id is None:
            # INSERT new author
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
            self._id = cursor.lastrowid
        else:
            # UPDATE existing author
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self._id))
        
        conn.commit()
        conn.close()
        return self
    
    def articles(self):
        """Return a list of Article objects for this author."""
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles 
            WHERE author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Article.new_from_db(row) for row in rows]
    
    def magazines(self):
        """Return a list of Magazine objects this author has contributed to."""
        from .magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Magazine.new_from_db(row) for row in rows]
    
    def add_article(self, magazine, title):
        """Create and save a new Article associated with this author and magazine."""
        from .article import Article
        article = Article(None, title, self._id, magazine.id)
        return article.save()
    
    def topic_areas(self):
        """Return a list of unique categories from magazines this author has written for."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows] if rows else None