from .database_utils import get_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value
    
    @classmethod
    def new_from_db(cls, row):
        """Create a Magazine instance from a database tuple/row."""
        return cls(row[0], row[1], row[2])
    
    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls.new_from_db(row)
        return None
    
    def save(self):
        """Save (INSERT or UPDATE) the magazine to the database."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self._id is None:
            # INSERT new magazine
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self._name, self._category)
            )
            self._id = cursor.lastrowid
        else:
            # UPDATE existing magazine
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self._name, self._category, self._id)
            )
        
        conn.commit()
        conn.close()
        return self
    
    def articles(self):
        """Return a list of Article objects for this magazine."""
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM articles 
            WHERE magazine_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Article.new_from_db(row) for row in rows]
    
    def contributors(self):
        """Return a list of Author objects who have written for this magazine."""
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Author.new_from_db(row) for row in rows]
    
    def article_titles(self):
        """Return a list of article titles for this magazine."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles WHERE magazine_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows] if rows else None
    
    def contributing_authors(self):
        """Return authors who have written more than 2 articles for this magazine."""
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Author.new_from_db(row) for row in rows] if rows else None
    
    def top_publisher(self):
        """BONUS: Return the magazine with the most articles."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Magazine.new_from_db(row[:3])
        return None