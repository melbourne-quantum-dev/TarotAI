try:
    from pydantic.v1 import BaseModel, Field
except ImportError:
    from pydantic import BaseModel, Field

class InterpretationLimits(BaseModel):
    """Limits for different types of tarot interpretations
    
    Attributes:
        single_card: Maximum length for single card interpretations
        three_card: Maximum length for three card spread interpretations
        celtic_cross: Maximum length for Celtic Cross spread interpretations
    """
    single_card: int = Field(default=500, gt=0, description="Maximum length for single card interpretations")
    three_card: int = Field(default=1000, gt=0, description="Maximum length for three card spread interpretations")
    celtic_cross: int = Field(default=2000, gt=0, description="Maximum length for Celtic Cross spread interpretations")
