# ragchain Turbo Puffer

import turbopuffer as tpuf
import os

tpuf.api_key = os.getenv("TURBO_PUFFER_API_KEY")
ns = tpuf.Namespace('ezgpt')

