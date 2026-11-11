
from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    ConfigDict
)


class SummarizeRequest(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "text": (
                        "Artificial intelligence is transforming "
                        "healthcare, education, and business. "
                        "It helps organizations automate tasks, "
                        "analyze information, and improve decisions."
                    ),
                    "max_length": 100,
                    "min_length": 20,
                    "language": "en"
                },
                {
                    "text": (
                        "L'intelligence artificielle transforme "
                        "le secteur de la santé et de l'éducation. "
                        "Elle aide les professionnels à analyser "
                        "les informations et à améliorer leurs décisions."
                    ),
                    "max_length": 100,
                    "min_length": 20,
                    "language": "fr"
                }
            ]
        }
    )

    text: str = Field(
        ...,
        min_length=50,
        description="The text that needs to be summarized."
    )

    max_length: int = Field(
        default=130,
        ge=30,
        le=250
    )

    min_length: int = Field(
        default=30,
        ge=10,
        le=100
    )

    language: str = Field(
        default="en",
        description="Summary language: en (English) or fr (French)."
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if len(value) < 50:
            raise ValueError(
                "Text must contain at least 50 characters."
            )

        return value

    @field_validator("language")
    @classmethod
    def validate_language(cls, value):
        value = value.lower().strip()

        if value not in ("en", "fr"):
            raise ValueError(
                "Language must be 'en' or 'fr'."
            )

        return value

    @model_validator(mode="after")
    def validate_summary_lengths(self):
        if self.min_length >= self.max_length:
            raise ValueError(
                "min_length must be smaller than max_length."
            )

        return self


class SummarizeResponse(BaseModel):
    original_text: str
    summary: str
