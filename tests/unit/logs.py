from src.logs.module import Logs, logger


def test_logs() -> None:

    instance = Logs(loglevel="SUCCESS")

    text = "Teste"
    methods = [
        instance.success,
        instance.info,
        instance.warning,
        instance.debug,
        instance.error,
        instance.critical,
    ]

    for log in methods:

        result = log(text=text)
        print(result)



if __name__  == "__main__":
    test_logs()