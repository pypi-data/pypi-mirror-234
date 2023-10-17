from randog.exceptions import FactoryConstructionError
from ._construct import factory as factory_from_model, factory_from_column


def custom(example, **kwargs):
    """custom_func for `randog.factory.from_example`
    to generate sqlalchemy-derived objects

    This function is an add-on for `randog.factory.from_example`.

    Specify this function as `custom_func` if you want to create a factory
    that generates sqlalchemy-derived objects in `from_example`.

    Examples
    --------
    >>> from sqlalchemy import Column, Integer, String
    >>> from sqlalchemy.orm import declarative_base
    >>> import randog.factory
    >>> import randog.sqlalchemy
    >>>
    >>> Base = declarative_base()
    >>>
    >>> class User(Base):
    ...     __tablename__ = "user"
    ...
    ...     id = Column(Integer, primary_key=True, autoincrement=True)
    ...     name = Column(String)
    >>>
    >>> # specify `randog.sqlalchemy.custom` as `custom_func`
    >>> factory = randog.factory.from_example(User,
    ...                                       custom_func=randog.sqlalchemy.custom)
    >>> generated = factory.next()
    """
    if kwargs.get("context") is not None:
        rnd = kwargs["context"].rnd
    else:
        rnd = kwargs.get("rnd")

    try:
        factory = factory_from_model(example, rnd=rnd)
    except FactoryConstructionError:
        factory = None

    if factory is None:
        try:
            factory = factory_from_column(example, rnd=rnd)
        except FactoryConstructionError:
            factory = None

    if factory is None:
        return NotImplemented
    else:
        return factory
