import logging
import sys
from pathlib import Path

import arklog
import dacite
import toml
import uvicorn

from spendpoint.configuration import Configuration
from spendpoint.main import get_application

arklog.set_config_logging()

data_dir = Path(__file__).resolve().parent.parent / Path("data")
logging.debug(f"Looking for configuration in '{data_dir}'.")
try:
    configuration = toml.loads((data_dir / Path("configuration.toml")).read_text(encoding="utf-8"))
    configuration = dacite.from_dict(data_class=Configuration, data=configuration, )
except FileNotFoundError as e:
    logging.error(f"Configuration 'configuration.toml' not found. {e}")
    sys.exit(8)
uvicorn.run(get_application(configuration), host=configuration.server.host, port=configuration.server.port)
