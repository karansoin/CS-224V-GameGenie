import os
import exa_py

os.environ["EXA_API_KEY"] = "6d43a0cd-7d42-4824-a255-7421ee166473"

# Create reusable client
exa_client = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])