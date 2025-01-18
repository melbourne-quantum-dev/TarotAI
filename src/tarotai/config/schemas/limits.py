from pydantic import BaseModel, Field, ConfigDict

class InterpretationLimits(BaseModel):
    """Limits for different types of tarot interpretations"""
    
    model_config = ConfigDict(
        validate_default=True,
        extra="forbid"
    )

    single_card: int = Field(
        default=500, 
        gt=0, 
        description="Maximum length for single card interpretations"
    )
    three_card: int = Field(
        default=1000, 
        gt=0, 
        description="Maximum length for three card spread interpretations"
    )
    celtic_cross: int = Field(
        default=2000, 
        gt=0, 
        description="Maximum length for Celtic Cross spread interpretations"
    )

    @classmethod
    def create_default(cls) -> "InterpretationLimits":
        return cls.model_validate({})