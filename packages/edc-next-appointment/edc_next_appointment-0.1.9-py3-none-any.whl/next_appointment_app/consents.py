from datetime import datetime
from zoneinfo import ZoneInfo

from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents
from edc_constants.constants import FEMALE, MALE

v1 = Consent(
    "next_appointment_app.subjectconsent",
    version="1",
    start=datetime(2018, 1, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
    end=datetime(2023, 1, 1, 0, 0, tzinfo=ZoneInfo("UTC")),
    age_min=18,
    age_is_adult=18,
    age_max=110,
    gender=[MALE, FEMALE],
)

site_consents.register(v1)
