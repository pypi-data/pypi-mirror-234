from settings_models._combat import SettingsModel, Field


class EnforcementSettings(SettingsModel):
    """
    Settings for enforcement service
    """
    payment_deadline_hours: int = Field(..., gt=0, description="How long someone can pay after exiting parking lot "
                                                               "(not including generally applied additional day)")
    strictness: int = Field(..., description="Strictness level for enforcement. Values to be defined")
