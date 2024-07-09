from alembic.config import Config
from alembic import command


def apply_migrations():
    alembic_cfg = Config("alembic_test.ini")
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    apply_migrations()
