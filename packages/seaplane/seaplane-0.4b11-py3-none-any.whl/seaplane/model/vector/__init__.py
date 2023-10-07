from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class Vector:
    def __init__(
        self,
        vector: List[float],
        id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.vector = vector
        self.metadata = metadata
        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id

    def __repr__(self) -> str:
        return f"Vector(vector={self.vector}, id={self.id}, metadata={self.metadata})"


Vectors = List[Vector]


class Distance(Enum):
    COSINE = "cosine"
    DOT = "dot"
    EUCLID = "euclid"

    def __str__(self) -> str:
        return str(self.value)
