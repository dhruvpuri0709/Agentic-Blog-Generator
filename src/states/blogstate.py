from typing import TypedDict, List, Annotated
from pydantic import BaseModel, Field
import operator

# Blog Section
class Section(BaseModel):
    title: str = Field(description = "Title of the blog section")
    description: str = Field(description = "Brief description of the blog section")

# Blog state used to get a structured output from an llm
class Sections(BaseModel):
    title: str
    sections: List[Section] = Field(description = "The sections of the blog")
    
# Graph state    
class Blog(TypedDict):
    topic : str
    title: str 
    sections: List[Section]
    completed_sections: Annotated[list,operator.add]
    final_blog: str
    
# Worker State
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list,operator.add]
    
    
    
    