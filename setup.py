import os
import exa_py

os.environ["EXA_API_KEY"] = "dfee28a8-09be-4da2-a70c-729cda3bbd3c"

# Create reusable client
exa_client = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])