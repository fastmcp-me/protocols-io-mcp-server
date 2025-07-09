from typing import Optional, Annotated
from pydantic import BaseModel, Field

class ProtocolStep(BaseModel):
    guid: Annotated[str, Field(description="Unique identifier for this protocol step. Please use 'generate_guids' to create the new GUIDs.")]
    step: str
    previous_guid: Annotated[Optional[str], Field(description="Only the previous_guid of the first step can be null.")] = None
    section: Optional[str] = None
    section_color: Optional[str] = None
    is_substep: bool = False

    def dict(self, **kwargs):
        return self.model_dump(exclude_none=True, **kwargs)
