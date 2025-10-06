#!/usr/bin/env python3
"""Debug script for testing the magazine management system."""

from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

def reset_database():
    """Clear and recreate all tables."""
    import os
    if os.path.exists('magazine.db'):
        os.remove('magazine.db')
    create_tables()
    print("✓ Database reset complete\n")

def test_basic_crud():
    """Test basic Create, Read, Update operations."""
    print("=== Testing Basic CRUD Operations ===\n")
    
    # Create authors
    author1 = Author(None, "Jane Doe")
    author1.save()
    print(f"✓ Created author: {author1.name} (ID: {author1.id})")
    
    author2 = Author(None, "John Smith")
    author2.save()
    print(f"✓ Created author: {author2.name} (ID: {author2.id})")
    
    # Create magazines
    mag1 = Magazine(None, "Tech Weekly", "Technology")
    mag1.save()
    print(f"✓ Created magazine: {mag1.name} - {mag1.category} (ID: {mag1.id})")
    
    mag2 = Magazine(None, "Food Monthly", "Culinary")
    mag2.save()
    print(f"✓ Created magazine: {mag2.name} - {mag2.category} (ID: {mag2.id})")
    
    # Create articles
    article1 = Article(None, "Introduction to Python", author1.id, mag1.id)
    article1.save()
    print(f"✓ Created article: {article1.title}")
    
    article2 = Article(None, "Advanced SQL Queries", author1.id, mag1.id)
    article2.save()
    print(f"✓ Created article: {article2.title}")
    
    article3 = Article(None, "Perfect Pasta Recipe", author2.id, mag2.id)
    article3.save()
    print(f"✓ Created article: {article3.title}")
    
    print()

def test_relationships():
    """Test relationship methods."""
    print("=== Testing Relationships ===\n")
    
    # Get an author and their articles
    author = Author.find_by_id(1)
    print(f"Author: {author.name}")
    print(f"  Articles written: {[a.title for a in author.articles()]}")
    print(f"  Magazines contributed to: {[m.name for m in author.magazines()]}")
    print(f"  Topic areas: {author.topic_areas()}")
    print()
    
    # Get a magazine and its content
    magazine = Magazine.find_by_id(1)
    print(f"Magazine: {magazine.name}")
    print(f"  Article titles: {magazine.article_titles()}")
    print(f"  Contributors: {[a.name for a in magazine.contributors()]}")
    print()
    
    # Test article relationships
    article = Article.find_by_id(1)
    print(f"Article: {article.title}")
    print(f"  Author: {article.author.name}")
    print(f"  Magazine: {article.magazine.name}")
    print()

def test_aggregate_methods():
    """Test advanced aggregate methods."""
    print("=== Testing Aggregate Methods ===\n")
    
    # Add more articles for testing
    author1 = Author.find_by_id(1)
    mag1 = Magazine.find_by_id(1)
    
    author1.add_article(mag1, "Python Best Practices")
    author1.add_article(mag1, "Web Development Guide")
    print("✓ Added 2 more articles for author 1")
    
    # Test contributing_authors
    contributing = mag1.contributing_authors()
    if contributing:
        print(f"✓ Authors with 2+ articles in {mag1.name}:")
        for author in contributing:
            print(f"  - {author.name}")
    else:
        print("  No authors with more than 2 articles yet")
    
    print()

def test_validations():
    """Test property validations."""
    print("=== Testing Validations ===\n")
    
    try:
        # Test author name validation
        bad_author = Author(None, "")
        bad_author.save()
    except ValueError as e:
        print(f"✓ Author validation working: {e}")
    
    try:
        # Test magazine name validation
        bad_mag = Magazine(None, "A", "Category")
        bad_mag.save()
    except ValueError as e:
        print(f"✓ Magazine name validation working: {e}")
    
    try:
        # Test article title validation
        bad_article = Article(None, "Hi", 1, 1)
        bad_article.save()
    except ValueError as e:
        print(f"✓ Article title validation working: {e}")
    
    print()

def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("  Magazine Management System - Debug Tests")
    print("="*50 + "\n")
    
    reset_database()
    test_basic_crud()
    test_relationships()
    test_aggregate_methods()
    test_validations()
    
    print("="*50)
    print("  All tests completed!")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()