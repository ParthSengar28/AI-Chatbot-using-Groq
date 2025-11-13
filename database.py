# database.py

from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize SQLite database (creates chat_history.db file)
engine = create_engine("sqlite:///chat_history.db", echo=False)
Base = declarative_base()

# Define table schema
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    role = Column(Text)  # 'user' or 'assistant' or 'system'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create table
Base.metadata.create_all(engine)

# Setup session
Session = sessionmaker(bind=engine)
session = Session()

# Function to save chat message
def save_message(role, content):
    msg = ChatMessage(role=role, content=content)
    session.add(msg)
    session.commit()

# Function to get all chat messages
def get_all_messages():
    return session.query(ChatMessage).order_by(ChatMessage.timestamp).all()

# Function to clear chat history (optional)
def clear_messages():
    session.query(ChatMessage).delete()
    session.commit()
