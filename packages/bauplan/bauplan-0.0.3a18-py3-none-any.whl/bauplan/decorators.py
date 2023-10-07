import functools
from typing import Any, Callable, Dict, Optional


def model(
    python_version: str,
    name: Optional[str]=None,
    dependencies: Optional[Dict[str, str]]=None,
    materialize: Optional[bool]=None,
) -> Callable:
    """Define a Bauplan Model.

    Args:
        python_version (str): the python version required to run the model (e.g. '3.11')
        name (Optional[str]): the name of the model (e.g. 'users'); if missing the function name is used
        decorators (Optional[List[Callable]]): a list of decorators to apply to the model function (e.g. {'requests': '2.26.0'})
        materialize (Optional[bool]): whether the model should be materialized (default True)
    """
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)
        return wrapper
    return decorator


def expectation(
    python_version: str,
    dependencies: Optional[Dict[str, str]]=None,
) -> Callable:
    """Define a Bauplan Expecation.

    Args:
        python_version (str): the python version required to run the model (e.g. '3.11')
        decorators (Optional[List[Callable]]): a list of decorators to apply to the model function (e.g. {'requests': '2.26.0'})
    """
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return f(*args, **kwargs)
        return wrapper
    return decorator
