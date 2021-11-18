import logging
import time


def interval_wait(cond, msg: str = "", retries: int = 10, delay: float = 1.0):
    """
    :param cond: лямбда-функция, в которой содержится код события, который мы ждём
    :param msg: сообщение
    :param retries: кол-во попыток на проверку события
    :param delay: задержка при проверке события
    :return: если результатом выполнения лямбды будет значение типа bool, то мы проверяем, дождались мы события или нет
             если результатом выполнения лямбы будет значение НЕ типа bool, то мы его просто возвращаем
    """
    actual_retries = 0
    result = None

    while 1:
        logging.debug(f"Выполнен повторный запрос №{actual_retries+1}")
        try:
            result = cond()
        except Exception:
            pass
        if result:
            break
        actual_retries += 1
        if actual_retries == retries:
            break
        if delay:
            time.sleep(delay)

    if isinstance(result, bool):
        assert result, f"{msg}"
    else:
        return result
