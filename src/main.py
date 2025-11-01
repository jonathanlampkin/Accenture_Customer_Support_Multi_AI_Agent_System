from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from enum import Enum
from datetime import datetime
import re

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class RunState(BaseModel):
    # Required fields with enhanced validation
    ticket_id: int = Field(
        gt=0,  # Must be greater than 0
        description="Auto-incrementing ticket identifier"
    )
    
    user_id: int = Field(
        gt=0,  # Must be greater than 0
        description="Auto-incrementing user identifier"
    )
    
    content: str = Field(
        ...,  # Required
        min_length=10,  # Ensure meaningful content
        max_length=2000,  # Limit tokens/cost
        regex="^(?!.*(?:SELECT|INSERT|UPDATE|DELETE|DROP|UNION|--)).*$",  # Basic SQL injection prevention
        description="The support request content, with security validations"
    )
    
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description="Automatically set to current timestamp"
    )
    
    # Optional fields with strong typing and validation
    category: Optional[str] = Field(
        None,
        max_length=50,
        regex="^[a-zA-Z0-9_-]+$",  # Alphanumeric with dash/underscore only
        description="Technical category of the ticket"
    )
    
    sentiment: Optional[str] = Field(
        None,
        regex="^(positive|negative|neutral)$",
        description="Analyzed sentiment of request"
    )
    
    priority: Optional[TicketPriority] = Field(
        None,
        description="Ticket priority level"
    )
    
    solution: Optional[str] = Field(
        None,
        max_length=5000,
        description="Proposed solution with length limit"
    )
    
    resolution_status: TicketStatus = Field(
        default=TicketStatus.PENDING,
        description="Current status of ticket"
    )
    
    resolved_at: Optional[int] = Field(
        None,
        description="Timestamp when resolved"
    )

    class Config:
        # Additional model configuration
        validate_assignment = True  # Validate when attributes are set
        extra = "forbid"  # Prevent additional fields
        
    @property
    def time_to_resolution(self) -> Optional[int]:
        """Calculate time taken to resolve ticket in seconds"""
        if self.resolved_at and self.created_at:
            return self.resolved_at - self.created_at
        return None
        
    def mark_as_resolved(self) -> None:
        """Helper method to mark ticket as resolved"""
        self.resolution_status = TicketStatus.RESOLVED
        self.resolved_at = int(datetime.now().timestamp())


class Router(BaseModel):




