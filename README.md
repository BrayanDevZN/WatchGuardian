<div align="center">
  <img src="assets/watchguardian-logo.svg" width="220" alt="WatchGuardian logo" />

# WatchGuardian

### Observe. Control. Integrate. Evolve.

Framework Python modular para observabilidade, logging, banco de dados, cache, autenticação, servidor HTTP e integração entre aplicações.

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?style=for-the-badge&logo=opentelemetry&logoColor=white)](https://opentelemetry.io/)
[![Requests](https://img.shields.io/badge/Requests-20232A?style=for-the-badge&logo=python&logoColor=white)](https://requests.readthedocs.io/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=111111)](https://pypi.org/project/python-dotenv/)
[![asyncpg](https://img.shields.io/badge/asyncpg-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://pypi.org/project/asyncpg/)
[![aiosqlite](https://img.shields.io/badge/aiosqlite-0F80CC?style=for-the-badge&logo=sqlite&logoColor=white)](https://pypi.org/project/aiosqlite/)

</div>

---

## Visão geral

O **WatchGuardian** foi criado para concentrar recursos comuns de backend em uma única base reutilizável. Em vez de repetir configuração de logs, observabilidade, cache, autenticação, banco e servidor em cada projeto, o framework fornece módulos prontos e uma API pública simples.

Além de funcionar como biblioteca embutida na aplicação, o WatchGuardian também pode **montar um servidor próprio dedicado à observabilidade**. Esse servidor expõe rotas para logs, observabilidade e autenticação, permitindo que múltiplas aplicações enviem, consultem e centralizem dados operacionais em uma única instância WatchGuardian.

A interface pública fica em `WatchGuardian/`, enquanto a implementação interna permanece organizada em `src/`.

```python
from WatchGuardian import Settings, WatchLogs, WatchObs, WatchAuth
from WatchGuardian.database import WatchDb, CacheManage
from WatchGuardian.server import ClientHttp, WatchServer
```

### Principais recursos

- logging com níveis `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR` e `CRITICAL`;
- persistência opcional dos logs em banco;
- observabilidade de tarefas com contexto assíncrono;
- PostgreSQL assíncrono e fallback SQLite;
- Redis para cache, contadores, hashes e Pub/Sub;
- autenticação JWT com `user_token` e `refresh_token`;
- **servidor próprio de observabilidade** baseado em FastAPI;
- servidor FastAPI pronto com CORS, rate limit e rotas internas;
- cliente HTTP para outras aplicações enviarem e consultarem dados na instância WatchGuardian;
- CLI própria com o comando `watchguardian`;
- arquitetura modular, separando API pública e implementação interna.

---

## Servidor próprio de observabilidade

O WatchGuardian pode ser usado como uma camada central de observabilidade da sua infraestrutura.

Em vez de cada aplicação armazenar e consultar seus próprios logs isoladamente, você pode subir uma instância WatchGuardian como serviço separado e fazer seus projetos conversarem com ela via HTTP.

```text
Aplicação A ─┐
Aplicação B ─┼──> WatchGuardian Server ───> Logs / Observabilidade / Banco / Redis
Aplicação C ─┘
```

Isso permite centralizar:

- logs de múltiplos serviços;
- status de tarefas;
- latência e falhas;
- eventos de observabilidade;
- autenticação das requisições;
- consulta remota via `ClientHttp`;
- persistência em PostgreSQL ou SQLite;
- cache e rate limit com Redis.

O objetivo é permitir que o WatchGuardian seja tanto uma biblioteca interna quanto um **serviço de observabilidade independente**.

---

## Arquitetura

```mermaid
flowchart TD
    A[Seu projeto] --> B[WatchGuardian API pública]

    B --> C[WatchGuardian/__init__.py]
    B --> D[WatchGuardian/database.py]
    B --> E[WatchGuardian/server.py]

    C --> F[Settings]
    C --> G[WatchLogs]
    C --> H[WatchObs]
    C --> I[WatchAuth]

    D --> J[WatchDb]
    D --> K[CacheManage]

    E --> L[ClientHttp]
    E --> M[WatchServer]

    M --> V[Servidor próprio de observabilidade]
    L --> V
    V --> W[Logs]
    V --> X[Observabilidade]
    V --> Y[Autenticação]

    F --> N[src/core]
    G --> O[src/logs + src/service]
    H --> P[src/service/obs]
    I --> Q[src/auth]
    J --> R[src/database]
    K --> S[src/cache]
    L --> T[src/client]
    M --> U[src/server]
```

A ideia é simples: quem usa a biblioteca trabalha com `WatchGuardian.*`; a estrutura `src.*` fica como implementação interna. Assim a API pública pode permanecer estável mesmo que a organização interna evolua.

---

## Instalação

### Instalar diretamente do GitHub

```bash
pip install git+https://github.com/BrayanDevZN/WatchGuardian.git
```

### Instalar em modo desenvolvimento

```bash
git clone https://github.com/BrayanDevZN/WatchGuardian.git
cd WatchGuardian
pip install -e .
```

Depois disso a CLI fica disponível globalmente no ambiente virtual:

```bash
watchguardian --help
```

### Requisitos

- Python `>= 3.12`
- Redis para os recursos de cache e para o servidor
- PostgreSQL opcional
- SQLite usado como fallback quando não há URL externa de banco

---

## API pública

### Base

```python
from WatchGuardian import (
    Settings,
    WatchLogs,
    WatchObs,
    WatchAuth,
)
```

### Banco e cache

```python
from WatchGuardian.database import (
    WatchDb,
    CacheManage,
)
```

### Servidor e cliente

```python
from WatchGuardian.server import (
    ClientHttp,
    WatchServer,
)
```

---

# Módulos

## `Settings`

Centraliza variáveis de ambiente e configurações da aplicação.

```python
from WatchGuardian import Settings

settings = Settings(env_file=".env")

settings.add_secret([
    "secret",
    "host",
    "port",
])

secret = settings.required_secrets("secret")
host = settings.get_secret("host")
```

Também é possível registrar configurações que não vêm do ambiente:

```python
settings.add_config({
    "name": "environment",
    "value": "development",
})

mode = settings.required_config("environment")
```

### Métodos principais

| Método | Função |
| --- | --- |
| `add_secret()` | carrega uma ou várias variáveis de ambiente |
| `get_secret()` | busca uma variável já registrada |
| `required_secrets()` | busca uma variável e gera erro se estiver ausente |
| `add_config()` | registra configuração em memória |
| `get_config()` | retorna uma configuração opcional |
| `required_config()` | exige uma configuração existente |

---

## `WatchLogs`

Gerencia logs estruturados e pode persistir os registros no banco em background.

```python
from WatchGuardian import WatchLogs

logs = WatchLogs(loglevel="DEBUG")

logs.debug("Entrando no fluxo")
logs.info("Processando dados")
logs.success("Operação concluída")
logs.warning("Tempo de resposta alto")
logs.error("Falha durante a operação")
logs.critical("Falha crítica")
```

Para persistir os logs no banco:

```python
from WatchGuardian import WatchLogs
from WatchGuardian.database import WatchDb

watch_db = await WatchDb(settings=settings)
logs = WatchLogs(loglevel="INFO", watch_db=watch_db)

logs.info("Esse log também será persistido")
```

Quando `watch_db` é fornecido, a escrita é disparada em background para evitar bloquear o fluxo principal.

---

## `WatchObs`

Permite acompanhar tarefas, latência, status e conteúdo de execução.

```python
from WatchGuardian import WatchLogs, WatchObs
from WatchGuardian.database import WatchDb

watch_db = await WatchDb(settings=settings)
logs = WatchLogs(loglevel="INFO", watch_db=watch_db)
obs = WatchObs(logs=logs, watch_db=watch_db)

async with obs.begin("process-data"):
    await process_data()
```

Ao entrar no contexto, a tarefa é registrada. Ao sair, o WatchGuardian finaliza a observabilidade automaticamente e registra sucesso ou erro.

---

## `WatchAuth`

Fornece geração e validação de JWTs.

```python
from WatchGuardian import Settings, WatchAuth

settings = Settings()
settings.add_secret("secret")

auth = WatchAuth(settings=settings)

user_token = await auth.user_token({
    "user_id": "123"
})

refresh_token = await auth.refresh_token({
    "user_id": "123"
})

payload = await auth.decode(user_token)
```

### Gerar uma secret

```python
from WatchGuardian import WatchAuth

secret = WatchAuth().secret()
print(secret)
```

A secret gerada pelo framework combina dois UUIDs aleatórios para produzir uma chave longa para assinatura.

---

## `WatchDb`

Abstrai o acesso ao banco e fornece controles para logs e observabilidade.

```python
from WatchGuardian import Settings
from WatchGuardian.database import WatchDb

settings = Settings()
settings.add_secret("url_db")

watch_db = await WatchDb(settings=settings)
```

Se `url_db` não estiver configurada, o projeto pode trabalhar com SQLite como fallback.

### Migrações básicas

```python
await watch_db.create_tables()
await watch_db.reset_tables()
await watch_db.drop_tables()
```

### Logs

```python
created = await watch_db.logs.create(
    log="Aplicação iniciada",
    status="INFO",
)

result = await watch_db.logs.select(id=created["id"])
```

### Observabilidade

```python
created = await watch_db.observability.create(
    task="etl",
    status="pending",
    content="starting",
    latency=0,
)
```

---

## `CacheManage`

Fornece operações Redis com TTL e suporte a Pub/Sub.

```python
from WatchGuardian import Settings
from WatchGuardian.database import CacheManage

settings = Settings()
settings.add_secret(["host", "port", "password"])

cache = CacheManage(settings=settings)
```

### Contador com TTL

```python
value = await cache.incr(
    key="rate:user:123",
    time=60,
)
```

### Hash

```python
await cache.hash(
    key="user:123",
    data={
        "name": "Brayan",
        "status": "active",
    },
    time=3600,
)

user = await cache.read(
    key="user:123",
    hash=True,
)
```

### Delete

```python
await cache.delete("user:123")
```

### Pub/Sub

```python
await cache.publish(
    channel="watchguardian:events",
    event="task_finished",
)
```

```python
async for event in cache.listen("watchguardian:events"):
    print(event)
```

---

## `ClientHttp`

Cliente HTTP para conversar com uma API WatchGuardian.

Por padrão usa `http://localhost:8000`. Também pode ler a variável de ambiente `url`.

Esse módulo é a ponte entre aplicações externas e o servidor próprio de observabilidade do WatchGuardian.

```python
from WatchGuardian import Settings
from WatchGuardian.server import ClientHttp

settings = Settings()
client = ClientHttp(settings=settings)
```

### Buscar logs

```python
logs = await client.logs(
    token=user_token,
).get_log()
```

### Buscar observabilidade

```python
items = await client.obs(
    token=user_token,
).get_obs()
```

### Refresh de autenticação

```python
result = await client.auth(
    user_token=user_token,
    refresh_token=refresh_token,
).refresh()
```

---

## `WatchServer`

O `WatchServer` monta o **servidor próprio de observabilidade do WatchGuardian**.

Ele cria uma aplicação FastAPI pronta para receber, persistir e consultar dados operacionais, com rotas de logs, observabilidade e autenticação, além de CORS, rate limit e integração com Redis.

Isso permite rodar o WatchGuardian como um serviço separado da aplicação principal e centralizar a observabilidade de múltiplos projetos.

```python
from WatchGuardian import Settings
from WatchGuardian.server import WatchServer

settings = Settings()
settings.add_secret([
    "secret",
    "origin",
    "host",
    "port",
    "password",
    "rate_limit",
])

server = WatchServer(settings=settings)
app = server.run()
```

A variável `app` retornada é um objeto FastAPI e pode ser iniciada com Uvicorn.

```bash
uvicorn main:app --reload
```

Depois, outras aplicações podem acessar essa instância usando `ClientHttp`.

---

# CLI

Depois da instalação, use diretamente:

```bash
watchguardian [comando]
```

## Ajuda

```bash
watchguardian --help
```

## Banco

Criar tabelas:

```bash
watchguardian migrate make_tables
```

Resetar tabelas:

```bash
watchguardian migrate reset
```

Dropar tabelas:

```bash
watchguardian migrate drop
```

Usando um arquivo `.env` específico:

```bash
watchguardian migrate --env-file .env.production make_tables
```

## Autenticação

Gerar secret:

```bash
watchguardian auth secret
```

Gerar user token:

```bash
watchguardian auth token --type user_token --payload '{"user_id":"123"}'
```

Gerar refresh token:

```bash
watchguardian auth token --type refresh_token --payload '{"user_id":"123"}'
```

## Servidor

```bash
watchguardian server run main:app
```

Com host e porta personalizados:

```bash
watchguardian server run main:app --host 0.0.0.0 --port 8080
```

Em detached:

```bash
watchguardian server run main:app --detached
```

## Consultar logs

```bash
watchguardian server logs --token SEU_TOKEN
```

## Consultar observabilidade

```bash
watchguardian server obs --token SEU_TOKEN
```

---

## Variáveis de ambiente

Dependendo dos módulos utilizados, o WatchGuardian pode ler as seguintes variáveis:

```env
# JWT
secret=your-secret

# Redis
host=localhost
port=6379
password=

# Database
url_db=postgresql+asyncpg://user:password@localhost:5432/watchguardian

# Server
origin=http://localhost:3000
rate_limit=100

# Client HTTP
url=http://localhost:8000
```

Nem todas são obrigatórias em todos os cenários. Cada módulo valida apenas as configurações que precisa para funcionar.

---

## Exemplo completo

```python
import asyncio

from WatchGuardian import Settings, WatchLogs, WatchObs, WatchAuth
from WatchGuardian.database import WatchDb


async def main() -> None:
    settings = Settings(env_file=".env")
    settings.add_secret([
        "secret",
        "url_db",
        "host",
        "port",
        "password",
    ])

    db = await WatchDb(settings=settings)
    logs = WatchLogs(loglevel="INFO", watch_db=db)
    obs = WatchObs(logs=logs, watch_db=db)
    auth = WatchAuth(settings=settings)

    token = await auth.user_token({
        "user_id": "123"
    })

    logs.success("WatchGuardian iniciado")

    async with obs.begin("example-task"):
        await asyncio.sleep(0.1)

    print(token)


asyncio.run(main())
```

---

## Estrutura do projeto

```text
WatchGuardian/
├── WatchGuardian/          # API pública da biblioteca
│   ├── __init__.py         # Settings, WatchLogs, WatchObs, WatchAuth
│   ├── database.py         # WatchDb, CacheManage
│   └── server.py           # ClientHttp, WatchServer
│
├── src/                    # implementação interna
│   ├── auth/
│   ├── cache/
│   ├── cli/
│   ├── client/
│   ├── core/
│   ├── database/
│   ├── logs/
│   ├── server/
│   ├── service/
│   └── util/
│
├── tests/
├── assets/
│   └── watchguardian-logo.svg
├── pyproject.toml
└── README.md
```

---

## Filosofia do projeto

O WatchGuardian segue quatro ideias principais:

**Observe**: tenha visibilidade sobre logs, tarefas, erros e latência.

**Control**: centralize configuração, banco, cache e autenticação.

**Integrate**: permita que aplicações diferentes conversem por HTTP e eventos.

**Evolve**: mantenha uma API pública simples enquanto a implementação interna continua evoluindo.

---

## Status

O WatchGuardian está em desenvolvimento ativo e atualmente está na versão `0.1.0`.

Áreas já presentes no projeto:

- [x] Settings
- [x] Logging
- [x] Observabilidade
- [x] JWT
- [x] Banco assíncrono
- [x] Redis
- [x] HTTP Client
- [x] FastAPI Server
- [x] Servidor próprio de observabilidade
- [x] CLI
- [x] Pacote instalável via `pyproject.toml`

---

## Desenvolvimento

Clone o projeto e instale em modo editável:

```bash
git clone https://github.com/BrayanDevZN/WatchGuardian.git
cd WatchGuardian
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Para gerar os artefatos do pacote:

```bash
python -m pip install build
python -m build
```

O resultado será criado em `dist/`.

---

## Repositório

GitHub: [BrayanDevZN/WatchGuardian](https://github.com/BrayanDevZN/WatchGuardian)

---

<div align="center">

### WatchGuardian

**Observability for real projects.**

Feito para transformar infraestrutura repetitiva em módulos reutilizáveis e centralizar a observabilidade em um servidor próprio quando necessário.

</div>
