"""Декоратор ValidAll."""
import re
from typing import Callable, Any, TypeVar

import jsonschema


class InputParameterVerificationError(Exception):
    """Исключение для input_validation."""

    def __init__(self: Any, message: str) -> None:
        """Конструктор своего исключения."""
        super().__init__(message)


class ResultVerificationError(Exception):
    """Исключение для result_validation."""

    def __init__(self: Any, message: str) -> None:
        """Конструктор своего исключения."""
        super().__init__(message)


class OnFailRepeatVerificationError(Exception):
    """Исключение для on_fail_repeat_time."""

    def __init__(self: Any, message: str) -> None:
        """Конструктор своего исключения."""
        super().__init__(message)


def default_func() -> None:
    """Функция исполняемая по умолчанию."""
    print("Произвольная функция для параметра default_behavior")
    return None


schema = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "test": "test"
        }
    ],
    "required": [
        "test"
    ],
    "properties": {
        "test": {
            "$id": "#/properties/test",
            "type": "string",
            "title": "The test schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "test"
            ]
        }
    }}


def json_validation(result: dict) -> Any:
    """Функиця для валидации json."""
    try:
        jsonschema.validate(result, schema)
        print(result)
        return result
    except jsonschema.ValidationError:
        return False


def regex_validation(validate_str: str) -> Any:
    """Функция для валидации по регулярке."""
    string_reg = re.compile("^[a-zA-Z]+$")
    if re.fullmatch(string_reg, validate_str):
        print(string_reg.fullmatch(validate_str))
        return string_reg.fullmatch(validate_str)
    else:
        return False


def default_function() -> None:
    """Функция вызывается по умолчанию."""
    print("Произвольная функция для параметра default_behavior")
    return None


RT = TypeVar('RT')


def valid_all(input_validation: Callable, result_validation: Callable, on_fail_repeat_times: int = 1,
              default_behavior: Callable = None) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """Декоратор с аргументами."""
    def decoration(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            if input_validation(*args, **kwargs) is False:
                raise InputParameterVerificationError("Невалидные входные параметры")

            else:
                result = func(*args, **kwargs)
                if result_validation(result) is False:
                    i = 0
                    while on_fail_repeat_times > i:
                        if default_behavior is None:
                            raise ResultVerificationError("Исключение произошло, потому что не пройдена проверка "
                                                          "результата выполнения функции (невалидный ключ json , "
                                                          "должен "
                                                          "быть 'test') или не указан параметр "
                                                          "default_behavior (default_behavior)")
                        else:
                            print("провал валидации результата, вызывается функция default_behavior()")
                            default_behavior()
                        i += 1
                if on_fail_repeat_times == 0:
                    raise OnFailRepeatVerificationError("on_fail_repeat = 0, самописное исключение")

                if on_fail_repeat_times >= 1:
                    result = result_validation(*args, **kwargs)
                    if result is True:
                        return result

                if on_fail_repeat_times < 0:
                    while True:
                        result = result_validation(*args, **kwargs)
                        print('Отрицательное значение on_fail_times, ждем  пока результат не пройдёт '
                              'условия проверки иначе бесконечный цикл')
                        if result is True:
                            break

        return wrapper

    return decoration


@valid_all(input_validation=regex_validation, result_validation=json_validation, on_fail_repeat_times=2,
           default_behavior=default_function)
def valid_function(st: str) -> Any:
    """Основная функция."""
    if st:
        js = {"test": st}
        return js


print(valid_function('adsdadsadasaddddsadSSSS'))
