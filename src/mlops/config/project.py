from pydantic import BaseModel



class Project(BaseModel):
    """
    Project class to hold project information.
    """
    name: str
    description: str