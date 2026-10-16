<div align="center">
  <img src="assets/watchguardian-logo.svg" width="220" alt="WatchGuardian logo" />

# WatchGuardian

### Observe. Control. Integrate. Evolve.

**Framework Python modular de observabilidade e infraestrutura para aplicações backend.**

O WatchGuardian reúne logging, observabilidade, banco de dados, cache, autenticação, cliente HTTP, CLI e um **servidor próprio de observabilidade** em uma API pública simples e reutilizável.

[![PyPI](https://img.shields.io/pypi/v/watchguardian?style=for-the-badge&logo=pypi&logoColor=white&color=3775A9)](https://pypi.org/project/watchguardian/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/build.yaml/badge.svg?branch=main)](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/build.yaml)
[![Functional](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/server.yaml/badge.svg?branch=main)](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/server.yaml)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/BrayanDevZN/WatchGuardian/actions)
[![Unit Tests](https://img.shields.io/badge/tests-unit-2EA44F?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/build.yaml)
[![Integration Tests](https://img.shields.io/badge/tests-integration-6F42C1?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/build.yaml)
[![Functional Tests](https://img.shields.io/badge/tests-functional-D97706?style=for-the-badge&logo=pytest&logoColor=white)](https://github.com/BrayanDevZN/WatchGuardian/actions/workflows/server.yaml)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?style=for-the-badge&logo=opentelemetry&logoColor=white)](https://opentelemetry.io/)

</div>

---

## Instalação pública

O WatchGuardian está disponível publicamente no PyPI.

```bash
pip install watchguardian
```

Para atualizar para a versão mais recente:

```bash
pip install --upgrade watchguardian
```

Depois da instalação, os imports públicos são:

```python
from WatchGuardian import Settings, WatchLogs, WatchObs, WatchAuth
from WatchGuardian.database import WatchDb, CacheManage
from WatchGuardian.server import ClientHttp, WatchServer
```

E a CLI fica disponível diretamente no terminal:

```bash
watchguardian --help
```

---

## O que é o WatchGuardian?

O **WatchGuardian é um framework**, não apenas uma coleção de helpers.

Ele fornece uma camada integrada para aplicações Python que precisam de observabilidade, persistência, autenticação, cache e comunicação entre serviços sem reconstruir a mesma infraestrutura em cada projeto.

O framework pode ser usado de duas formas:

1. **Embutido na própria aplicação**, usando módulos como `WatchLogs`, `WatchObs`, `WatchDb`, `CacheManage` e `WatchAuth`.
2. **Como servidor central de observabilidade**, usando `WatchServer` para subir uma API própria e `ClientHttp` para outras aplicações se conectarem a ela.

### Principais recursos

- logging com `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR` e `CRITICAL`;
- persistência opcional de logs em background;
- observabilidade assíncrona de tarefas, latência, status e erros;
- servidor próprio de observabilidade baseado em FastAPI;
- PostgreSQL assíncrono e SQLite como fallback;
- Redis para cache, TTL, contadores, hashes e Pub/Sub;
- JWT com `user_token` e `refresh_token`;
- cliente HTTP para comunicação com instâncias WatchGuardian;
- CLI própria com `watchguardian`;
- testes unitários, de integração e funcionais;
- CI automatizado com GitHub Actions;
- distribuição pública via PyPI;
- projeto **open source** sob licença MIT, aberto a sugestões e contribuições via Pull Request.

---

## Servidor próprio de observabilidade

Um dos pontos centrais do framework é a possibilidade de montar uma instância WatchGuardian dedicada à observabilidade.

```text
Aplicação A ─┐
Aplicação B ─┼──> WatchGuardian Server ───> Logs / Observabilidade / Banco / Redis
Aplicação C ─┘
```

Essa instância centraliza:

- logs de múltiplos serviços;
- tarefas e status de execução;
- latência;
- falhas e erros;
- autenticação das requisições;
- persistência de dados;
- consultas remotas via `ClientHttp`;
- rate limit e cache com Redis.

Assim, o WatchGuardian pode funcionar tanto como framework dentro de um projeto quanto como um serviço separado de observabilidade para vários sistemas.

---

## Arquitetura

```mermaid
flowchart TD
    A[Aplicação] --> B[WatchGuardian API pública]

    B --> C[Core]
    B --> D[Database]
    B --> E[Server]

    C --> F[Settings]
    C --> G[WatchLogs]
    C --> H[WatchObs]
    C --> I[WatchAuth]

    D --> J[WatchDb]
    D --> K[CacheManage]

    E --> L[ClientHttp]
    E --> M[WatchServer]

    M --> N[Servidor de observabilidade]
    N --> O[Logs]
    N --> P[Observabilidade]
    N --> Q[Autenticação]
    N --> R[Redis]
    N --> S[Database]
```

A camada `WatchGuardian/` é a API pública. A implementação interna permanece em `src/`, permitindo evoluir a arquitetura sem obrigar quem usa o framework a depender da estrutura interna.

---

# Uso dos módulos

## `Settings`

Centraliza variáveis de ambiente e configurações.

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

Configurações em memória também podem ser registradas:

```python
settings.add_config({
    "name": "environment",
    "value": "development",
})

mode = settings.required_config("environment")
```

---

## `WatchLogs`

Gerencia logs estruturados.

```python
from WatchGuardian import WatchLogs

logs = WatchLogs(loglevel="DEBUG")

logs.debug("Entrando no fluxo")
logs.info("Processando dados")
logs.success("Operação concluída")
logs.warning("Tempo de resposta alto")
logs.error("Falha na operação")
logs.critical("Falha crítica")
```

Para persistir os logs:

```python
from WatchGuardian import WatchLogs
from WatchGuardian.database import WatchDb

watch_db = await WatchDb(settings=settings)
logs = WatchLogs(loglevel="INFO", watch_db=watch_db)

logs.info("Esse log também será persistido")
```

Quando `watch_db` é informado, a persistência é executada em background para não bloquear o fluxo principal.

---

## `WatchObs`

Registra execução, status, latência e falhas de tarefas.

```python
from WatchGuardian import WatchLogs, WatchObs
from WatchGuardian.database import WatchDb

watch_db = await WatchDb(settings=settings)
logs = WatchLogs(loglevel="INFO", watch_db=watch_db)
obs = WatchObs(logs=logs, watch_db=watch_db)

async with obs.begin("process-data"):
    await process_data()
```

Ao entrar no contexto a tarefa é registrada. Ao sair, o framework finaliza automaticamente a observabilidade, incluindo erros quando ocorrerem.

---

## `WatchAuth`

Cria e valida JWTs.

```python
from WatchGuardian import Settings, WatchAuth

settings = Settings()
settings.add_secret("secret")

auth = WatchAuth(settings=settings)

user_token = await auth.user_token({"user_id": "123"})
refresh_token = await auth.refresh_token({"user_id": "123"})

payload = await auth.decode(user_token)
```

Gerar uma secret:

```python
from WatchGuardian import WatchAuth

secret = WatchAuth().secret()
print(secret)
```

---

## `WatchDb`

Fornece acesso ao banco usado pelo framework e aos dados de logs e observabilidade.

```python
from WatchGuardian import Settings
from WatchGuardian.database import WatchDb

settings = Settings()
settings.add_secret("url_db")

watch_db = await WatchDb(settings=settings)
```

Sem `url_db`, o framework pode utilizar SQLite como fallback.

### Tabelas

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

logs = await watch_db.logs.select()
```

### Observabilidade

```python
await watch_db.observability.create(
    task="etl",
    status="pending",
    content="starting",
    latency=0,
)
```

---

## `CacheManage`

Interface Redis do framework.

```python
from WatchGuardian import Settings
from WatchGuardian.database import CacheManage

settings = Settings()
settings.add_secret(["host", "port", "password"])

cache = CacheManage(settings=settings)
```

Contador com TTL:

```python
value = await cache.incr("rate:user:123", time=60)
```

Hash:

```python
await cache.hash(
    key="user:123",
    data={"name": "Brayan", "status": "active"},
    time=3600,
)

user = await cache.read("user:123", hash=True)
```

Pub/Sub:

```python
await cache.publish("watchguardian:events", "task_finished")

async for event in cache.listen("watchguardian:events"):
    print(event)
```

---

## `WatchServer`

Monta o servidor próprio de observabilidade do framework.

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

Depois execute com Uvicorn:

```bash
uvicorn main:app --reload
```

O servidor inclui rotas internas de logs, observabilidade e autenticação, além de CORS, rate limit e integração com Redis.

---

## `ClientHttp`

Conecta aplicações ao servidor WatchGuardian.

```python
from WatchGuardian import Settings
from WatchGuardian.server import ClientHttp

settings = Settings()
client = ClientHttp(settings=settings)
```

Por padrão usa `http://localhost:8000`. Também pode usar a variável `url`.

```python
logs = await client.logs(token=user_token).get_log()
items = await client.obs(token=user_token).get_obs()

result = await client.auth(
    user_token=user_token,
    refresh_token=refresh_token,
).refresh()
```

---

# CLI

Após instalar pelo PyPI:

```bash
pip install watchguardian
```

A CLI fica disponível como:

```bash
watchguardian [comando]
```

### Ajuda

```bash
watchguardian --help
```

### Banco

```bash
watchguardian migrate make_tables
watchguardian migrate reset
watchguardian migrate drop
```

Com arquivo `.env` específico:

```bash
watchguardian migrate --env-file .env.production make_tables
```

### Autenticação

```bash
watchguardian auth secret
watchguardian auth token --type user_token --payload '{"user_id":"123"}'
watchguardian auth token --type refresh_token --payload '{"user_id":"123"}'
```

### Servidor

```bash
watchguardian server run main:app
```

```bash
watchguardian server run main:app --host 0.0.0.0 --port 8080
```

```bash
watchguardian server run main:app --detached
```

### Consultar dados do servidor

```bash
watchguardian server logs --token SEU_TOKEN
watchguardian server obs --token SEU_TOKEN
```

---

## Exemplo rápido da versão pública

Depois de instalar:

```bash
pip install watchguardian
```

Crie um arquivo `main.py`:

```python
import asyncio
import os

from WatchGuardian import Settings, WatchLogs, WatchObs, WatchAuth
from WatchGuardian.database import WatchDb


async def main() -> None:
    os.environ["secret"] = WatchAuth().secret()

    settings = Settings()
    settings.add_secret("secret")

    db = await WatchDb(settings=settings)
    await db.create_tables()

    logs = WatchLogs(loglevel="INFO", watch_db=db)
    obs = WatchObs(logs=logs, watch_db=db)
    auth = WatchAuth(settings=settings)

    token = await auth.user_token({"user_id": "123"})

    logs.success("WatchGuardian iniciado")

    async with obs.begin("example-task"):
        await asyncio.sleep(0.2)

    print(token)


asyncio.run(main())
```

Execute:

```bash
python main.py
```

---

## Variáveis de ambiente

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

Cada módulo utiliza apenas as configurações necessárias para sua função.

---

## Testes e CI/CD

O projeto possui três níveis de testes:

### Unitários

Validam componentes isolados como banco, logs, cache, token e comandos internos.

### Integração

Validam a comunicação entre módulos, incluindo integração entre banco, logging e observabilidade.

### Funcionais

Sobem o servidor WatchGuardian e exercitam o fluxo completo via cliente HTTP e CLI.

Os testes são executados no GitHub Actions. O workflow `build.yaml` executa testes unitários e de integração com Redis como serviço, enquanto `server.yaml` executa os testes funcionais do servidor.

O projeto também está preparado para fluxo de CI/CD com GitHub Actions e publicação de releases no PyPI. Atualmente a validação contínua é automatizada e a distribuição pública é feita pelo pacote `watchguardian`.

---

## Open source e contribuições

O **WatchGuardian é open source** e o desenvolvimento é aberto à comunidade.

Sugestões, melhorias, correções de bugs, documentação e novos recursos podem ser enviados por **Pull Request** no GitHub. Antes de abrir um PR, prefira manter a API pública compatível, adicionar ou atualizar testes quando necessário e garantir que os workflows de CI continuem passando.

Fluxo recomendado para contribuir:

1. faça um fork do repositório;
2. crie uma branch para a alteração;
3. implemente a mudança e execute os testes;
4. faça push da branch;
5. abra um Pull Request descrevendo o problema, a solução e o impacto da mudança.

Issues também podem ser usadas para propor recursos, relatar bugs ou discutir mudanças antes da implementação.

---

## Licença

O WatchGuardian é distribuído sob a **MIT License**. Isso permite usar, copiar, modificar, distribuir e incorporar o framework em projetos pessoais ou comerciais, respeitando os termos presentes no arquivo [`LICENSE`](LICENSE).

---

## Estrutura do projeto

```text
WatchGuardian/
├── WatchGuardian/          # API pública do framework
│   ├── __init__.py
│   ├── database.py
│   └── server.py
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
│   ├── unit/
│   ├── integration/
│   └── functional/
│
├── .github/workflows/
├── assets/
├── LICENSE
├── pyproject.toml
└── README.md
```

---

## Desenvolvimento local

```bash
git clone https://github.com/BrayanDevZN/WatchGuardian.git
cd WatchGuardian
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Gerar o pacote:

```bash
python -m pip install build
python -m build
```

---

## Status

Versão pública atual: **0.1.0**.

- [x] Framework instalável via PyPI
- [x] API pública em `WatchGuardian`
- [x] Settings
- [x] Logging
- [x] Observabilidade
- [x] JWT
- [x] Banco assíncrono
- [x] Redis
- [x] HTTP Client
- [x] Servidor próprio de observabilidade
- [x] CLI `watchguardian`
- [x] Testes unitários
- [x] Testes de integração
- [x] Testes funcionais
- [x] CI com GitHub Actions
- [x] Open source sob licença MIT

---

<div align="center">

### WatchGuardian

**Observability for real projects.**

Um framework Python open source para observar, controlar e conectar infraestrutura backend sem repetir o mesmo trabalho em cada aplicação.

</div>
