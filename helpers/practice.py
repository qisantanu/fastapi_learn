from sqlmodel import SQLModel, Field, Relationship, select
from typing import List, Optional
from sqlalchemy.orm import selectinload

# 1. How would you handle a one-to-many relationship (e.g., User has many Posts) in FastAPI?

# Declare User model
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    
    # Relationship: One User can have many Posts
    posts: List["Post"] = Relationship(back_populates="user")

# Declare Post model
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    
    # Foreign Key pointing to the User table
    user_id: int = Field(foreign_key="users.id")
    
    # Relationship: Each Post belongs to one User
    user: User = Relationship(back_populates="posts")

# 2. How do you prevent the N+1 problem?
# The N+1 problem occurs when you fetch N items and then make N additional queries to fetch related data.
# In SQLModel/SQLAlchemy, you use "Eager Loading" to fetch everything in one (or fewer) optimized queries.

# Example of preventing N+1 using 'selectinload' for one-to-many relationships:
def get_users_with_posts(session):
    # This fetches all users and their associated posts in just TWO queries total, 
    # rather than 1 query for users + 1 query PER user for their posts.
    statement = select(User).options(selectinload(User.posts))
    results = session.exec(statement).all()
    return results

# Example of preventing N+1 using 'joinedload' (often used for many-to-one):
# statement = select(Post).options(joinedload(Post.user))
