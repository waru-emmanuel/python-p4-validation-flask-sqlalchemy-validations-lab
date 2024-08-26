from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators name,phone number, id
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError('Phone number must be exactly 10 digits.')
        if not phone_number.isdigit():
            raise ValueError('Phone number must contain only digits.')
        return phone_number
    
    @validates('id')
    def validate_id(self, key, id):
        if id <= 0:
            raise ValueError('ID must be a positive integer.')
        if id > 10000:
            raise ValueError('ID must be less than or equal to 10000.')
        return id

    @validates('name')
    def validate_name(self, key, name):
        if len(name) < 3 or len(name) > 50:
            raise ValueError('Name must be between 3 and 50 characters long.')
        if not all(char.isalpha() or char in [' ', '-'] for char in name):
            raise ValueError('Name must contain only alphabetic characters, spaces, or hyphens.')
        if db.session.query(Author).filter_by(name=name).first():
            raise ValueError('Name must be unique.')
        return name
        
        
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be a maximum of 250 characters long.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError(f'Title must contain one of the following phrases: {", ".join(clickbait_phrases)}.')
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
