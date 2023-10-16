from contextlib import contextmanager

__connection__ = None
__db_url__ = None
__default_db_url__ = None
__session_maker__ = None


def setup_db_connection(database=None, host=None, username=None, password=None):
    from sqlalchemy import create_engine
    from sqlalchemy.engine.url import make_url
    from stratus_api.core.settings import get_settings
    from copy import deepcopy
    app_settings = get_settings(settings_type='app')
    db_settings = get_settings(settings_type='db')
    db_name = db_settings['db_name'] + app_settings['prefix'].split('-')[0]
    db_url_format = "{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    global __db_url__
    __db_url__ = make_url(
        db_url_format.format(db_name=db_name, **{k: v for k, v in db_settings.items() if k not in {"db_name"}})
    )
    global __default_db_url__
    __default_db_url__ = deepcopy(__db_url__)
    __default_db_url__.database = db_settings.get('default_db_name', 'postgres')
    global __connection__
    __connection__ = create_engine(__db_url__)
    configure_session_maker(bind=__connection__)
    return __db_url__


def configure_session_maker(**kwargs):
    from sqlalchemy.orm import sessionmaker

    global __session_maker__
    if __session_maker__ is None:
        __session_maker__ = sessionmaker()
    __session_maker__.configure(**kwargs)
    return __session_maker__


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global __session_maker__
    session = __session_maker__()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_test_db():
    from sqlalchemy import create_engine
    from alembic.config import Config
    from alembic import command
    global __default_db_url__
    global __db_url__
    default_db = create_engine(__default_db_url__)
    with default_db.connect() as conn:
        conn.execute("COMMIT")
        conn.execute('create database {0}'.format(__db_url__.database))
    alembic_cfg = Config("/apps/app/alembic.ini")
    command.upgrade(alembic_cfg, "head")


def delete_test_db():
    global __connection__
    global __default_db_url__
    global __db_url__
    from sqlalchemy import create_engine
    from stratus_api.core.settings import get_settings
    assert get_settings()['environment'] == 'test' and get_settings()['prefix']
    __connection__.dispose()
    default_db = create_engine(__default_db_url__)

    with default_db.connect() as conn:
        conn.execute("COMMIT")
        conn.execute("""drop database {0};""".format(__db_url__.database))
