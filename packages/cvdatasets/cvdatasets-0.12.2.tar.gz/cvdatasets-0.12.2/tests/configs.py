import os
import abc

from pathlib import Path

class config(abc.ABC):
	BASE_DIR = Path(os.environ.get("BASE_DIR", Path(__file__).parent))

	INFO_FILE = str(BASE_DIR / "test_info.yml")

print(config.BASE_DIR)
