"""Valida o encaminhamento do balanceador até a rota health."""

import requests


BALANCE_URL = "http://127.0.0.1:8003/balance/health/"


def test_balance_health() -> None:
    response = requests.get(BALANCE_URL, timeout=10, allow_redirects=True)

    assert response.status_code == 200, response.text
    assert response.json() == {"status": "ok"}
    assert response.history, "A resposta não passou pelo redirecionamento do balanceador"
    assert response.url.startswith(("http://127.0.0.1:8000/", "http://127.0.0.1:8001/", "http://127.0.0.1:8002/"))

    print(f"Balance encaminhou /health/ para {response.url}")


if __name__ == "__main__":
    test_balance_health()
