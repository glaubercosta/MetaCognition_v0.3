import os


CREWAI_MODE = os.getenv("CREWAI_MODE", "stub").lower()  # stub | real
CREWAI_API_KEY = os.getenv("CREWAI_API_KEY", "")
DEFAULT_ENGINE = os.getenv("DEFAULT_ENGINE", "crewai").lower()

