"""Run claudemy's scrape.py with SSL errors treated like other network errors."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("scrape", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36", "Accept-Language": "en,ru;q=0.8"}
m.NETWORK_ERRORS = (*m.NETWORK_ERRORS, OSError)
m.main(Path(sys.argv[2]).resolve(), "web")
