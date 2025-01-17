from pydantic import BaseModel, Field

class InterpretationLimits(BaseModel):
    """Token limits for interpretation stages"""
    card_analysis: int = Field(default=1000, description="Tokens per card analysis")
    spread_analysis: int = Field(default=1500, description="Tokens for spread analysis") 
    context_synthesis: int = Field(default=1000, description="Tokens for context synthesis")
    final_interpretation: int = Field(default=2000, description="Tokens for final interpretation")
