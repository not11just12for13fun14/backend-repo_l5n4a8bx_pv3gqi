"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Example schemas (retain for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Fitness app schemas
class Exercise(BaseModel):
    """
    Exercises catalog
    Collection: "exercise"
    """
    name: str = Field(..., min_length=1, max_length=100, description="Exercise name")
    notes: Optional[str] = Field(None, max_length=300, description="Optional notes")

class WorkoutSet(BaseModel):
    reps: int = Field(..., ge=1, le=1000, description="Repetitions")
    weight: float = Field(0, ge=0, le=10000, description="Weight per set")

class WorkoutExercise(BaseModel):
    exercise_id: Optional[str] = Field(None, description="Reference to exercise _id as string")
    exercise_name: Optional[str] = Field(None, description="Custom exercise name if not in catalog")
    sets: List[WorkoutSet] = Field(default_factory=list)

class Workout(BaseModel):
    """
    Workouts with multiple exercises and sets
    Collection: "workout"
    """
    performed_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str] = Field(None, description="Workout title or focus")
    notes: Optional[str] = Field(None)
    exercises: List[WorkoutExercise] = Field(default_factory=list)
