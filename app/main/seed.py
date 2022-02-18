import logging
from models.core_indicators import WorkingPropertyCoreIndicator,PropertyCoreIndicator
from models import Property

from db.seed.import_tool_seed import import_tool_seed_bd
from db.session import SessionLocalCRM

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocalCRM()
    import_tool_seed_bd(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
