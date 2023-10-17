import random
import time
import asyncio
from typing_extensions import Optional, Union, Literal, Callable, Awaitable
from datetime import datetime


class Logger:
    """
    The logger instance for a consistent logging experience.

    ```py
    logger = Logger();
    ```
    """

    __log_id: str = ""
    """The current log id as an empty `str`"""
    __exec_timestamp: int = 0
    """Initialise the execution timestamp as `0`"""
    __proc_timestamp: int = 0
    """Initialise a process' timestamp as `0`"""
    __delta: int = 0
    """Initialise the delta for the sequence as `0`"""
    __cache: str = ""
    """Initialise the cache for the previous call's process as an empty `string`"""
    id_length: int = 5
    """The log id length; defaults to 5 `chars`"""
    american_date: bool = False
    """Whether or not the date should be logged in the amrican format"""
    time_format: str = "%d %b %Y @ %H:%M"
    """Other options for the log time output"""

    def __init__(
        self,
        id_length: Optional[int] = None,
        american_date: Optional[bool] = None,
        time_format: Optional[str] = None,
    ) -> None:
        """
        Create a new `Logger` instance and begin logging processes, their relative processing times, as well the an execution time from start to finish

        #### Some Use Cases
            - Route handler logs
            - Function logs
            - Process tracking
            - Chaining logs for an entire process

        ### Example

        #### code

        ```py
        from qolpy import Logger
        from .some_function import some_function
        from fastapi import FastAPI, Request

        app = FastAPI()
        logger = Logger()

        @app.middleware("http")
        async def handler(req: Request, call_next):
            logger.new_log("log", req.method, req.url.path)

            logger.log("log", "some_function", "Doing something...")
            some_function()
            logger.proc_time()

            response = await call_next(req)

            logger.execTime()
            return response

        ...
        ```

        #### terminal output

        ```sh
        [log • aGy5Op]: GET => /hello | 07 Oct 2023 @ 19:40
        [log • aGy5Op]: some_function => Doing something... | 07 Oct 2023 @ 19:40
        [stats • aGy5Op]: some_function => 53.24ms
        [exec • aGy5Op]: 121.07ms
        ```

        Parameters:
        - id_length (int, None): The log id length; defaults to 5 characters.
        - american_date (bool, None): Whether or not the date should be logged in the American format; defaults to False.
        - time_format (str, None): The datetime format; defaults to `%d %b %Y @ %H:%M`
        """
        if id_length:
            self.id_length = id_length

        if american_date:
            self.american_date = american_date

        if time_format:
            self.time_format = time_format

    def __gen_log_id__(self) -> None:
        """Generate an ID for logs"""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        alphabet_array = list(alphabet)

        i = 0
        log_id = ""

        while True:
            random_index = random.randrange(len(alphabet_array))
            log_id += alphabet_array[random_index]
            i += 1

            if i == self.id_length:
                break

        self.__log_id = log_id

    def __gen_timestamp__(self) -> str:
        """enerate the log timestamp"""
        d = datetime.now()
        time = d.strftime(self.time_format)
        return time

    def new_log(
        self,
        config: Union[Literal["stats"], Literal["log"], Literal["error"]],
        process: str,
        message: str,
    ) -> None:
        """Create a new log chain; This will change the `log id`"""
        d = time.time() * 1000
        self.__gen_log_id__()
        self.__exec_timestamp = d
        self.__proc_timestamp = d

        print(
            f"[{config} • {self.__log_id}]: {process} => {message} | {self.__gen_timestamp__()}"
        )

    def log(
        self,
        config: Union[Literal["stats"], Literal["log"], Literal["error"]],
        process: str,
        message: str,
    ) -> None:
        """Add a log to the log chain; This will not change the `log id`"""
        d = time.time() * 1000

        old_proc_timestamp = self.__proc_timestamp
        self.__proc_timestamp = d

        self.__delta = d - old_proc_timestamp
        self.__cache = process

        print(
            f"[{config} • {self.__log_id}]: {process} => {message} | {self.__gen_timestamp__()}"
        )

    def proc_time(self) -> None:
        """Log the processing time between this call and the previous call to view their processing time"""
        print(f"[stats • {self.__log_id}]: {self.__cache} => {self.__delta:.2f}ms")
        self.__cache = ""

    def exec_time(self) -> None:
        """View the entire execution time"""
        d = time.time() * 1000
        delta = d - self.__exec_timestamp

        print(f"[exec • {self.__log_id}]: {delta:.2f}ms")

        self.__log_id = ""
        self.__cache = ""
        self.__exec_timestamp = 0
        self.__proc_timestamp = 0
        self.__delta = 0

    def lax(self, func: Union[Callable, Awaitable]):
        """
        A decorator method ideally for use in functions only to log their usage and execution time; it works for sync and async functions by default.

        NOTE that this decorator is not chainable, but, you may chain from within the function you use it as a decorator by calling `logger.log(...)`

        #### Code

        ```py
        logger = Logger()

        @logger.lax
        def api_call() -> str:
            req = requests.get("https://api.site.com/hello")
            logger.log("log", "api_call", "request successfull!")

            res = req.json()
            return res["msg"]

        api_call()
        ```

        #### Terminal Output

        ```sh
        [log • cy1zD]: api_call => Executing with no args | 07 Oct 2023 @ 23:52
        [log • cy1zD]: api_call => request successfull!| 07 Oct 2023 @ 23:52
        [exec • cy1zD]: 107.09ms
        ```
        """

        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args, **kwargs):
                args_list = [f"{value!r}" for value in args]
                kwargs_list = [f"{key}={value!r}" for key, value in kwargs.items()]

                msg = "Executing with"

                if args:
                    args_str = ", ".join(args_list)
                    single_plural_args = "arg" if len(args_list) == 1 else "args"
                    msg += f" {single_plural_args} {args_str}"

                if kwargs:
                    prefix = "and " if len(args_list) > 0 else ""
                    kwargs_str = " ".join(kwargs_list)
                    single_plural_kwargs = (
                        f"{prefix}kwarg" if len(kwargs_list) == 1 else f"{prefix}kwargs"
                    )
                    msg += f" {single_plural_kwargs} {kwargs_str}"

                if len(args_list) == 0 and len(kwargs_list) == 0:
                    msg += "out args nor kwargs"

                self.new_log("log", func.__name__, msg)
                result = await func(*args, **kwargs)
                self.exec_time()
                return result

            return async_wrapper
        else:

            def wrapper(*args, **kwargs):
                args_list = [f"{value!r}" for value in args]
                kwargs_list = [f"{key}={value!r}" for key, value in kwargs.items()]

                msg = "Executing with"

                if args:
                    args_str = ", ".join(args_list)
                    single_plural_args = "arg" if len(args_list) == 1 else "args"
                    msg += f" {single_plural_args} {args_str}"

                if kwargs:
                    prefix = "and " if len(args_list) > 0 else ""
                    kwargs_str = " ".join(kwargs_list)
                    single_plural_kwargs = (
                        f"{prefix}kwarg" if len(kwargs_list) == 1 else f"{prefix}kwargs"
                    )
                    msg += f" {single_plural_kwargs} {kwargs_str}"

                if len(args_list) == 0 and len(kwargs_list) == 0:
                    msg += "out args nor kwargs"

                self.new_log("log", func.__name__, msg)

                result_sync = func(*args, **kwargs)
                self.exec_time()
                return result_sync

            return wrapper
