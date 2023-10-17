"""Top-level package for dwai."""
import os

api_key = os.environ.get("DW_API_KEY")
api_base_china = os.environ.get("DW_API_CHINA_BASE")
api_base_singapore = os.environ.get("DW_API_SINGAPORE_BASE")

api_timeout_seconds = 300


