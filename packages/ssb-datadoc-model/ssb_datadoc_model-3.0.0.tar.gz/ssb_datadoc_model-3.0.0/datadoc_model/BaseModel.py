from pydantic import ConfigDict, BaseModel


class DataDocBaseModel(BaseModel):
    """Defines configuration which applies to all Models in this application"""
    model_config = ConfigDict(validate_assignment=True, use_enum_values=True)
