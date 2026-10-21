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

O PyPI instala a última versão publicada; alterações ainda não publicadas neste repositório só estarão disponíveis instalando o checkout local, por exemplo com `pip install -e .`.

Depois da instalação, os imports públicos são:

```python
from WatchGuardian import Settings, WatchLogs, WatchObs, WatchAuth
from WatchGuardian.database import WatchDb, CacheManage
from WatchGuardian.server import ClientHttp, WatchServer
from WatchGuardian.balance import WatchBalance, Replicator, Replicators
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
- estimativa do aumento de memória residente (RSS), em bytes, observado durante cada tarefa;
- servidor próprio de observabilidade baseado em FastAPI;
- WebSockets separados para eventos de logs e observabilidade em tempo real;
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

O servidor também publica eventos nos canais `/logs/ws` e `/obs/ws`. Veja [a documentação de realtime](docs/realtime.md) para autenticação, formato das mensagens e exemplos.

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

A API pública e toda a implementação distribuída ficam no pacote `WatchGuardian`. Os detalhes internos ficam em `WatchGuardian._internal`; use os imports documentados de `WatchGuardian`.

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

async with obs.begin(name="process-data", group="orders"):
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
    memory_bytes=0,
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
O rate limit Redis vale para requisições HTTP; as conexões WebSocket ficam fora desse middleware.

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

# Cada método mantém sua própria conexão e recebe só aquele tipo de evento.
import asyncio

async def main():
    async def receive_logs():
        async for event in client.listen_logs(token=user_token):
            print(event["type"], event["data"])

    async def receive_obs():
        async for event in client.listen_obs(token=user_token):
            print(event["type"], event["data"])

    await asyncio.gather(receive_logs(), receive_obs())

asyncio.run(main())
```

---

### Eventos em tempo real

O servidor fornece `/logs/ws` e `/obs/ws`; o `ClientHttp` tem `listen_logs(token)` e `listen_obs(token)`. Os iteradores recebem envelopes JSON de eventos futuros, sem histórico ou replay. Para detalhes sobre Redis Pub/Sub, autenticação, limites de fila e reconexão, consulte [docs/realtime.md](docs/realtime.md).

---

## Balance: `Replicator`, `Replicators` e `WatchBalance`

O módulo de balance recebe as requisições HTTP e escolhe uma réplica WatchGuardian saudável para atendê-las. Ele testa as réplicas configuradas em sequência, considera os métodos HTTP permitidos e redireciona a requisição para a primeira réplica compatível. Se nenhuma ficar disponível dentro do timeout, retorna erro.

- `Replicator` representa uma instância remota, com URL e regras de método, caminho e limite.
- `Replicators` monta uma lista de `Replicator` usando as configurações compartilhadas.
- `WatchBalance` cria a aplicação FastAPI do balanceador com o middleware e as rotas de redirecionamento.

No modo de projeto, essas configurações ficam em `settings.json`, dentro de `configs`:

```json
{
  "configs": {
    "replicator_name": "api",
    "replicator_urls": [
      "http://localhost:8001",
      "http://localhost:8002"
    ],
    "replicator_paths": "*",
    "replicator_methods": ["GET", "POST"],
    "replicator_limit": 60,
    "replicator_expires": 60
  }
}
```

`replicator_urls` lista as URLs dos servidores de destino. `replicator_methods` aceita `*` ou uma lista de métodos HTTP; `replicator_paths` aceita `*` ou uma lista com `logs` e/ou `obs`. `replicator_limit` e `replicator_expires` são os parâmetros de limite e expiração passados às instâncias `Replicator`.

O scaffold local começa com `http://localhost:8000` como URL de réplica. Troque esse valor pelas URLs das suas aplicações antes de iniciar o balanceador; apontar o balanceador para ele próprio cria um ciclo de redirecionamento.

Sem projeto, crie o balanceador passando um objeto `Replicators` ou uma lista de `Replicator` pelo formato CLI `modulo:atributo`. Com projeto, as réplicas são criadas das configurações acima.

## Projeto gerado: `ProjectApp` e `WatchModule`

O comando `watchguardian project start` copia a pasta-template `WatchGuardian/project/watchguardian/` para o destino. O nome da pasta copiada pode ser escolhido com `--name`; ele é convertido para minúsculas. Sem `--name`, a pasta se chama `watchguardian`. Esse nome padrão é aplicado automaticamente; para `--name`, escolha outro nome. O template contém:

- `main.py`, que cria e exporta `app`;
- `manage.py`, `module.py` e `settings.py`, que inicializam e conectam os módulos.

O pacote público `WatchGuardian` é instalado como dependência do framework; ele não é duplicado dentro do template. A pasta-base `WatchGuardian/project/watchguardian/` também não contém `settings.json`.

O arquivo `WatchGuardian/_internal/project/file.py` copia o template e, em seguida, cria `settings.json` dentro da pasta gerada. Esse JSON recebe o nome, caminho, arquivo de ambiente, modo local/HTTP, nível de log e as configurações padrão. Assim, o arquivo só passa a existir no projeto do usuário depois de executar `project start`.

Exemplo:

```bash
watchguardian project start --path ./apps --name api
watchguardian server run --project ./apps/api
```

A classe `ProjectApp` lê o JSON. Quando chamada, ela prepara `ProjectSettings`, aplica as configurações salvas e inicializa um `WatchModule`. O objeto gerado fica disponível como `app` em `main.py`; depois da inicialização, `app.module` contém o agregador.

O campo `env_file` controla o modo:

- `null`: modo local; aplica os secrets e configs padrão de `ProjectSettings` e usa `http = null`;
- caminho para um arquivo: lê as variáveis do arquivo e usa o modo HTTP (`http = true`); variáveis ausentes recebem os defaults locais.

As configurações personalizadas vão no objeto `configs` do `settings.json`. Elas são adicionadas ao `Settings` compartilhado antes dos módulos serem construídos. Assim, por exemplo, as URLs de réplica do balanceador podem ser alteradas sem editar o código gerado.

### Módulos disponíveis em `WatchModule`

| Atributo | Instância | Para que serve |
| --- | --- | --- |
| `settings` | `Settings` | Configuração compartilhada por todos os módulos |
| `watch_db` | `WatchDb` | Banco do framework; também conecta os módulos de logs e observabilidade |
| `watch_logs` | `WatchLogs` | Logs ligados ao banco compartilhado |
| `watch_obs` | `WatchObs` | Registro de tarefas, estados, erros e latência |
| `watch_auth` | `WatchAuth` | Geração e validação de tokens |
| `cache` | `CacheManage` ou `None` | Cache Redis obtido pelo banco |
| `client_http` | `ClientHttp` | Cliente para consultar uma instância remota |
| `watch_server` / `server_app` | `WatchServer` / FastAPI | Servidor de observabilidade e sua aplicação ASGI |
| `replicators` | `Replicators` | Réplicas configuradas para o balanceador |
| `watch_balance` / `balance_app` | `WatchBalance` / FastAPI | Balanceador e sua aplicação ASGI |

`app.load_module()` carrega os módulos e retorna o próprio `WatchModule`. Os comandos `migrate`, `auth`, `server` e `balance` aceitam `--project`; se a opção for omitida, o CLI procura automaticamente `./watchguardian`. Para a lista completa de opções e exemplos, consulte [docs/cli.md](docs/cli.md).

Também é possível iniciar o agregador no código, sem usar a pasta gerada:

```python
import asyncio
from WatchGuardian.project.watchguardian.manage import watch_manage

async def main():
    modules = await watch_manage(env_file=None)
    await modules.watch_db.create_tables()

asyncio.run(main())
```

Passe um caminho em `env_file` para usar o modo HTTP do projeto; deixe `None` para carregar os defaults locais.

---

# CLI

A CLI possui os grupos `project`, `migrate`, `auth`, `server` e `balance`. Para a referência completa de opções, exemplos, ordem dos argumentos, `.env` e projetos, consulte [docs/cli.md](docs/cli.md).

```bash
watchguardian --help
watchguardian project --help
watchguardian migrate --help
watchguardian auth --help
watchguardian server --help
watchguardian balance --help
```

Início rápido para criar e usar um projeto:

```bash
watchguardian project start --with_env
watchguardian migrate make_tables
watchguardian auth secret
watchguardian auth token --type user_token
watchguardian server run --host 0.0.0.0 --port 8080
```

Por padrão, os comandos procuram o projeto em `./watchguardian`. Para outro diretório, passe `--project ./apps/api`. Sem um projeto encontrado, os comandos usam as variáveis de ambiente disponíveis e falham se faltar alguma configuração necessária.

# Referência detalhada da API pública

Esta seção descreve os construtores e métodos públicos disponíveis nos módulos exportados por `WatchGuardian`. Métodos iniciados por `_` são auxiliares internos e não fazem parte da API pública estável.

## Configuração: `Settings`

Importação: `from WatchGuardian import Settings`

- `Settings(env_file: str | None = None)`: cria os dicionários `secrets` e `configs`. Se receber `env_file`, carrega esse arquivo; caso contrário, tenta carregar o `.env` do diretório atual.
- `add_secret(secrets: str | list[str]) -> None`: registra uma ou várias chaves para leitura do ambiente. Se uma variável de ambiente existir, ela prevalece; se não existir, preserva um valor que já estava salvo em `secrets`.
- `get_secret(secret_name: str) -> Any`: retorna o valor da chave ou `None` se ela não estiver registrada.
- `required_secrets(secret: str) -> Any`: retorna o valor obrigatório. Lança `SettingsNotFoundEnv` se a chave estiver ausente, vazia ou com valor `None`.
- `add_config(configs: dict | list[dict]) -> None`: adiciona configurações no formato `{"name": ..., "value": ...}`; aceita um item ou uma lista.
- `get_config(name: str) -> Any`: retorna a configuração ou `None` se não estiver registrada.
- `required_config(name: str) -> Any`: retorna a configuração e lança `SettingsNotFoundConfig` se o nome não existir. A verificação é pela existência da chave; um valor registrado como `None` é permitido.

Se o arquivo de ambiente informado não existir, o construtor lança `SettingsNotFoundEnvironment`.

## Logs: `WatchLogs`

Importação: `from WatchGuardian import WatchLogs`

- `WatchLogs(loglevel="INFO", watch_db=None)`: escolhe o nível mínimo exibido e, opcionalmente, conecta a instância de `WatchDb` para persistir os registros.
- `debug(text)`, `info(text)`, `success(text)`, `warning(text)`, `error(text)` e `critical(text)`: escrevem um registro no nível correspondente e retornam o registro criado ou `None` quando ele não passa pelo filtro de nível. Quando `watch_db` foi informado, registros exibidos são enviados ao banco em uma tarefa em background.

Os níveis aceitos no construtor são `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR` e `CRITICAL`.

## Observabilidade: `WatchObs`

Importação: `from WatchGuardian import WatchObs`

- `WatchObs(logs, watch_db)`: recebe um `WatchLogs` e um `WatchDb` compartilhados.
- `begin(name: str, group: str) -> ObsContext`: devolve um gerenciador de contexto assíncrono. Ao entrar, cria um registro pendente; ao sair, atualiza o registro com duração, conteúdo e resultado. O parâmetro `group` é obrigatório.

```python
async with obs.begin(name="process-data", group="orders"):
    await process_data()
```

O objeto de contexto oferece os métodos herdados de controle:

- `task(name, group) -> UUID`: inicia manualmente um registro pendente e retorna seu identificador público.
- `commit(content, error=False) -> None`: finaliza o registro como `success` ou `failure`, medindo a duração desde `task`. Use `error=True` para registrar falha.
- `close() -> None`: remove o registro atual.

Em geral, prefira `begin()`: o contexto chama `task` e `commit` automaticamente, inclusive ao propagar uma exceção ocorrida dentro do bloco.

## Autenticação: `WatchAuth`

Importação: `from WatchGuardian import WatchAuth`

- `WatchAuth(settings=None)`: obtém a chave JWT `secret` de `Settings`. Para criar ou validar tokens, forneça uma chave válida em `Settings`.
- `secret() -> str`: gera uma chave aleatória usando UUIDs; não a salva automaticamente no ambiente ou em `Settings`.
- `user_token(payload=None) -> str`: cria um JWT do tipo `user_token`, adicionando expiração de uma hora a partir do momento da criação.
- `refresh_token(payload=None) -> str`: cria um JWT do tipo `refresh_token` e remove qualquer `exp` recebido no payload.
- `encode(payload) -> str`: método herdado que codifica o payload com HS256.
- `decode(token) -> dict`: método herdado que valida e decodifica o JWT, retornando o payload. Erros de validação são propagados.

`user_token`, `refresh_token`, `encode` e `decode` são assíncronos.

## Persistência: `WatchDb`

Importação: `from WatchGuardian.database import WatchDb`

- `WatchDb(settings, http=False)`: cria acesso local ao banco quando `http` é falso ou `None`; com `http=True`, encaminha operações para um servidor via HTTP e requer o secret `token`. A instância é awaitable: use `db = await WatchDb(settings)` para inicializá-la.
- `create_tables() -> None`: cria as tabelas locais se ainda não existirem.
- `reset_tables() -> None`: apaga os registros das tabelas locais de logs e observabilidade.
- `drop_tables() -> None`: remove as tabelas locais.
- `logs`: serviço CRUD de logs.
- `observability`: serviço CRUD de observabilidade.
- `cache`: instância de `CacheManage` quando `host` e `port` estão configurados; caso contrário, `None`.

Os três métodos de tabela só funcionam no modo local; no modo HTTP lançam `RuntimeError`.

### `watch_db.logs`

Os métodos são assíncronos:

- `create(log: str, status: str) -> dict`: grava um log.
- `select(id=None, public_id=None) -> dict | list[dict] | None`: lista todos os registros se nenhum identificador for passado, ou busca pelo ID numérico ou público.
- `update(id=None, public_id=None, log=None, status=None) -> dict | None`: atualiza os campos enviados. Informe um dos identificadores e pelo menos um campo.
- `delete(id=None, public_id=None) -> dict | None`: remove pelo ID numérico ou público.

### `watch_db.observability`

Os métodos são assíncronos:

- `create(group, task, status, content, latency, public_id=None, memory_bytes=0) -> dict`: cria um registro; `memory_bytes` guarda o aumento estimado de RSS em bytes; gera um identificador público se não receber um.
- `select(id=None, public_id=None, group=None) -> dict | list[dict] | None`: lista registros ou filtra por identificador e/ou grupo.
- `update(id=None, public_id=None, group=None, task=None, status=None, content=None, latency=None, memory_bytes=None) -> dict | None`: atualiza os campos fornecidos; exige um identificador e pelo menos um campo para alterar.
- `delete(id=None, public_id=None) -> dict | None`: remove pelo ID numérico ou público.

Os dois serviços usam cache Redis quando `watch_db.cache` está disponível. Se não houver cache configurado, operam diretamente no banco ou no servidor HTTP.

## Cache: `CacheManage`

Importação: `from WatchGuardian.database import CacheManage`

- `CacheManage(settings)`: conecta ao Redis usando os secrets obrigatórios `host` e `port`; `password` é opcional.
- `incr(key, time=None) -> int`: incrementa um contador e aplica TTL em segundos. O TTL padrão é 60 segundos.
- `hash(key, data, time=None) -> None`: grava os pares do dicionário em um hash Redis e aplica o TTL, também de 60 segundos por padrão.
- `read(key, hash=False) -> Any`: lê um valor simples; com `hash=True`, lê o hash inteiro.
- `delete(key) -> bool`: apaga a chave e retorna se alguma chave foi removida.
- `publish(channel, event) -> int`: publica uma mensagem e retorna quantos assinantes a receberam.
- `listen(channel) -> AsyncIterator[Any]`: assina o canal e produz mensagens conforme chegam; o canal é desassinado quando a iteração termina ou é cancelada.

Todos os métodos Redis acima são assíncronos.

## Servidor: `WatchServer`

Importação: `from WatchGuardian.server import WatchServer`

- `WatchServer(settings)`: prepara uma aplicação FastAPI com rotas de logs, observabilidade, autenticação e health check, além dos middlewares configurados.
- `run() -> FastAPI`: instala CORS, rotas e middleware e retorna a aplicação ASGI para executar com Uvicorn.

## Cliente: `ClientHttp`

Importação: `from WatchGuardian.server import ClientHttp`

- `ClientHttp(settings=None, url=None)`: cria um cliente para a URL informada, para o secret `url` de `Settings`, ou para `http://localhost:8000` nessa ordem.
- `logs(token) -> LogsClient`: cria um cliente de operações de logs autenticado pelo token.
- `obs(token) -> ObsClient`: cria um cliente de operações de observabilidade autenticado pelo token.
- `auth(user_token, refresh_token) -> AuthClient`: cria um cliente de autenticação com os dois tokens.
- `health() -> bool`: consulta `/health` e retorna se o servidor está acessível.
- `listen_logs(token)`: conecta ao WebSocket autenticado `/logs/ws` e retorna um iterador assíncrono somente de eventos de logs.
- `listen_obs(token)`: conecta ao WebSocket autenticado `/obs/ws` e retorna um iterador assíncrono somente de eventos de observabilidade.

Os métodos de operação HTTP são assíncronos:

- Em `client.logs(token)`: `create_log(status, log)`, `get_log(id=None, public_id=None)`, `update_log(id=None, public_id=None, log=None, status=None)` e `delete_log(id=None, public_id=None)`.
- Em `client.obs(token)`: `create_obs(group, task, status, content, latency, memory_bytes=0)`, `get_obs(id=None, public_id=None, group=None)`, `update_obs(id=None, public_id=None, group=None, task=None, status=None, content=None, latency=None, memory_bytes=None)` e `delete_obs(id=None, public_id=None)`.

- Em `client.auth(user_token, refresh_token)`: `refresh()` envia os tokens para a rota de renovação.

`WatchObs.begin()` grava o RSS inicial em `memory_bytes` quando cria o registro pendente. Ao sair do contexto, atualiza o campo com o aumento estimado do pico de RSS observado durante a task. A amostragem ocorre a cada 50 ms, então picos mais curtos podem passar despercebidos. Em tarefas assíncronas concorrentes, o RSS é compartilhado pelo processo; o valor final é uma estimativa e não uma atribuição isolada de memória para cada coroutine. `memory_bytes` também pode ser enviado pelo cliente HTTP; no banco, registros antigos recebem `0` quando a coluna é adicionada.

Os clientes retornam o JSON da resposta. Quando a resposta HTTP tem status 400 ou superior, registram o erro e retornam `None`.

## Balanceamento: `Replicator`, `Replicators` e `WatchBalance`

Importação: `from WatchGuardian.balance import Replicator, Replicators, WatchBalance`

### `Replicator`

- `Replicator(url, cache, limit, name, paths="*", methods="*", limit_expires=60)`: representa uma réplica remota. `paths` aceita `*` ou caminhos `logs` e `obs`; `methods` define métodos aceitos e pode ser `*`.
- `valid() -> bool`: valida a configuração e verifica `/health` na instância remota. O balanceador usa esse resultado para escolher o destino.

### `Replicators`

- `Replicators(settings)`: lê `replicator_name`, `replicator_urls`, `replicator_paths`, `replicator_methods`, `replicator_limit` e `replicator_expires` de `Settings`; também cria a conexão de cache usada pelas réplicas.
- `get_replicas() -> list[Replicator]`: constrói e retorna uma réplica para cada URL configurada.

### `WatchBalance`

- `WatchBalance(replicas, timeout=60)`: recebe `Replicators` ou uma lista de `Replicator`. O timeout define por quanto tempo tenta encontrar uma réplica válida.
- `run() -> FastAPI`: instala o middleware seletor e as rotas do balanceador e retorna a aplicação ASGI. As requisições são redirecionadas com status 307; se não houver destino válido antes do timeout, retorna erro 501.

Nota sobre os parâmetros `limit` e `limit_expires`: eles são armazenados pela classe `Replicator`, mas o fluxo atual de validação não incrementa nem consulta o contador. Portanto, não use esses parâmetros como garantia de rate limit nesta versão.

## Projeto: `ProjectSettings`, `WatchModule` e `ProjectApp`

Esses módulos pertencem ao template de projeto em `WatchGuardian/project/watchguardian/`; a função de cópia fica em `WatchGuardian/_internal/project/file.py`.

### `ProjectSettings`

- `ProjectSettings(env_file=None, local=False)`: prepara um `Settings` para o projeto.
- `local_secret() -> None`: registra os secrets consumidos pelos módulos e preenche defaults locais ausentes.
- `local_config() -> None`: registra as configurações de banco e réplicas, lendo primeiro os valores do ambiente e usando defaults quando faltarem.
- `get() -> Settings`: retorna as configurações e preenche secrets e configs ausentes com defaults locais, também quando um `env_file` foi informado.

### `WatchModule`

O agregador compartilha as mesmas configurações e dependências entre os módulos.

- `WatchModule(settings, http=None, loglevel="INFO")`: prepara os atributos para as instâncias dos módulos.
- `database() -> WatchDb`: inicializa o banco uma vez, conecta o cache e prepara o logger com persistência.
- `logs() -> WatchLogs`: retorna logs conectados ao banco compartilhado.
- `observability() -> WatchObs`: cria a observabilidade usando os logs e banco compartilhados.
- `auth() -> WatchAuth`: retorna autenticação configurada com os secrets compartilhados.
- `cache_module() -> CacheManage | None`: retorna o cache do banco, se estiver configurado.
- `client() -> ClientHttp`: retorna o cliente HTTP compartilhado.
- `server() -> WatchServer`: prepara o servidor e sua aplicação FastAPI em `server_app`.
- `balance() -> WatchBalance`: prepara as réplicas, o balanceador e sua aplicação FastAPI em `balance_app`.
- `load_modules() -> WatchModule`: inicializa todos os módulos e retorna o próprio agregador.

Os métodos de inicialização são idempotentes para as instâncias armazenadas: chamadas seguintes retornam o objeto já criado.

### `ProjectApp` e criação do projeto

- `ProjectApp()`: lê o `settings.json` ao lado de `main.py`.
- `load_module() -> WatchModule`: resolve o `env_file` relativo à pasta do projeto, aplica configurações do JSON, carrega todos os módulos e retorna o agregador em `app.module`.
- Após `await app.load_module()`, os módulos ficam disponíveis em `app.watch_db`, `app.watch_logs`, `app.watch_obs`, `app.watch_auth`, `app.cache`, `app.client_http`, `app.watch_server`, `app.server_app`, `app.replicators`, `app.watch_balance` e `app.balance_app`. Esses atributos são encaminhados ao `WatchModule`; também é possível acessar o agregador por `app.module`.
- `copy_watchguardian(path=None, name=None, env_file=None) -> Path`: copia o template para `path/name`, gera o `settings.json` no destino e retorna o caminho criado. `path=None` usa o diretório atual; `name=None` usa `watchguardian`; o arquivo `file.py` não é copiado junto com o template.

A CLI `project start` chama essa função. Use `project reset` para restaurar os defaults locais e `project delete` para remover o projeto. Ajuste as configurações em `settings.json` antes de executar servidor ou balanceador.


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

    async with obs.begin(name="example-task", group="examples"):
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

# Redis (rate limit HTTP e eventos entre instâncias)
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

Validam componentes isolados como banco, logs, cache, token, comandos internos, flag `--realtime` do CLI, os canais WebSocket e o rate limit Redis HTTP.

### Integração

Validam a comunicação entre módulos, incluindo integração entre banco, logging e observabilidade.

### Funcionais

Sobem o servidor WatchGuardian e exercitam o fluxo completo via cliente HTTP e CLI.

Os testes são executados no GitHub Actions. O workflow `build.yaml` executa testes unitários e de integração; nele, Redis é iniciado como serviço. Os testes de WebSocket verificam autenticação, serialização de datas e isolamento dos canais. O workflow `server.yaml` executa os testes funcionais do servidor.

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
WatchGuardian/                  # pacote público
├── __init__.py
├── balance.py
├── database.py
├── server.py
├── _internal/                   # implementação e CLI do framework
│   ├── auth/
│   ├── cache/
│   ├── cli/
│   ├── client/
│   ├── core/
│   ├── database/
│   ├── logs/
│   ├── project/                 # copiador do template
│   ├── server/
│   ├── service/
│   └── util/
└── project/
    └── watchguardian/           # template gerado pelo CLI

tests/
.github/workflows/
assets/
LICENSE
pyproject.toml
README.md
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

Versão preparada para a próxima publicação: **0.2.14**.

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
