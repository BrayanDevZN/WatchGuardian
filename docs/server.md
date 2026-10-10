# WatchGuardian Server

Este documento explica como configurar, iniciar e consumir o servidor HTTP do WatchGuardian.

O servidor é construído sobre FastAPI e reúne as rotas de logs, observabilidade e autenticação/refresh de token.

---

## 1. Estrutura do servidor

```text
src/server/
├── depends.py
├── manage.py
├── midlleware.py
├── handles/
│   ├── auth.py
│   ├── logs.py
│   └── obs.py
└── schema/
    ├── logs.py
    └── obs.py
```

Responsabilidades principais:

- `manage.py`: cria o FastAPI, registra CORS, routers e middleware.
- `midlleware.py`: aplica rate limit usando Redis.
- `depends.py`: valida o `user_token` nas rotas protegidas.
- `handles/logs.py`: CRUD HTTP de logs.
- `handles/obs.py`: CRUD HTTP de observabilidade.
- `handles/auth.py`: gera um novo `user_token` usando o token antigo e o `refresh_token`.
- `schema/`: schemas Pydantic usados pelos handlers.

---

## 2. Settings

O `Server` recebe uma instância de `Settings` já preparada.

Com arquivo `.env` explícito:

```python
from src.service.module import Settings

settings = Settings(env_file=".env")
```

Ou usando o `.env` padrão encontrado pelo `python-dotenv`:

```python
settings = Settings()
```

Carregar o `.env` não adiciona automaticamente as variáveis ao dicionário interno de `Settings`. As variáveis precisam ser registradas com `add_secret()` antes de serem usadas por `required_secrets()` ou `get_secret()`.

### Variáveis obrigatórias para o servidor

```python
settings.add_secret([
    "host",
    "port",
    "origin",
    "rate_limit",
    "secret",
])
```

### Variáveis opcionais

```python
settings.add_secret([
    "password",
    "url_db",
])
```

`password` e `url_db` podem ficar `None`.

### Config opcional `path`

`path` não é variável de ambiente no fluxo atual. Ele é uma config interna adicionada com `add_config()`:

```python
settings.add_config({
    "name": "path",
    "value": "./data"
})
```

O `path` é opcional e só participa da configuração do banco quando `url_db` não foi fornecida.

---

## 3. Variáveis e configs

### 3.1 `host`

**Obrigatória:** sim.

Usada pelo `CacheManage` para criar a conexão Redis.

```env
host=localhost
```

Sem `host`, o `Server` não consegue criar o cache porque `CacheManage` usa `required_secrets("host")`.

---

### 3.2 `port`

**Obrigatória:** sim.

Porta do Redis.

```env
port=6379
```

Assim como `host`, é lida com `required_secrets()`.

---

### 3.3 `password`

**Obrigatória:** não.

Senha do Redis quando a instância exige autenticação.

```env
password=minha-senha
```

Se o Redis não usar senha, a variável pode ser omitida ou resultar em `None`. O `CacheManage` lê esse valor com `get_secret()`.

---

### 3.4 `origin`

**Obrigatória:** sim.

Usada na configuração de CORS do servidor.

```env
origin=http://localhost:3000
```

O `Server._cors()` usa:

```python
self.settings.required_secrets(secret="origin")
```

Portanto, `origin` não pode estar ausente, `None` ou vazia.

---

### 3.5 `rate_limit`

**Obrigatória:** sim para o middleware de rate limit.

Define o limite de requisições controlado pelo Redis.

```env
rate_limit=100
```

O middleware lê esse valor com `required_secrets()` e converte para `int`:

```python
rate_limit = int(self.settings.required_secrets(secret="rate_limit"))
```

O valor precisa representar um inteiro válido.

---

### 3.6 `secret`

**Obrigatória:** sim para autenticação e rotas protegidas.

Usada para assinar e validar os JWTs.

```env
secret=uma-secret-segura
```

Ela é necessária para:

- validar `user_token`;
- validar `refresh_token`;
- criar novos tokens;
- acessar as rotas protegidas por `depends_user`;
- usar `/auth/refresh`.

É possível gerar uma secret pela CLI:

```bash
python -m src.cli.main auth secret
```

O comando apenas imprime a secret. Ele não salva automaticamente no `.env`.

---

### 3.7 `url_db`

**Obrigatória:** não.

A `url_db` define explicitamente qual banco será usado.

Exemplo PostgreSQL:

```env
url_db=postgresql+asyncpg://usuario:senha@localhost:5432/watchguardian
```

Exemplo SQLite explícito:

```env
url_db=sqlite+aiosqlite:///./watchguardian.db
```

O `WatchDb` lê a variável assim:

```python
url = settings.get_secret(secret_name="url_db")
```

Portanto, `url_db=None` é válido.

A prioridade do banco é:

```text
url_db definida
    ↓
usa exatamente a URL informada

url_db None + path definido
    ↓
usa SQLite em <path>/watch.db

url_db None + path None
    ↓
usa sqlite+aiosqlite:///watch.db
```

Ou seja, o projeto funciona sem a variável `url_db`.

---

### 3.8 `path`

**Obrigatória:** não.

**Tipo:** config interna de `Settings`, não secret/env no fluxo atual.

É usada somente como fallback do SQLite quando `url_db` é `None`.

Exemplo:

```python
settings.add_config({
    "name": "path",
    "value": "./data"
})
```

Com esse valor, `config_url()` monta:

```text
sqlite+aiosqlite:///./data/watch.db
```

O diretório informado em `path` precisa existir. Se não existir, `config_url()` levanta `FileNotFoundError`.

Exemplo:

```bash
mkdir -p data
```

Não passe o nome do arquivo SQLite em `path`. O próprio `config_url()` acrescenta `watch.db` ao caminho.

Correto:

```python
{"name": "path", "value": "./data"}
```

Resultado:

```text
./data/watch.db
```

Se `url_db` estiver definida, `path` é ignorado.

Se nem `url_db` nem `path` forem definidos, o fallback é:

```text
sqlite+aiosqlite:///watch.db
```

---

## 4. Resumo das variáveis

| Nome | Tipo | Obrigatória? | Usada por | Comportamento se ausente |
| --- | --- | --- | --- | --- |
| `host` | env/secret | Sim | Redis / `CacheManage` | erro em `required_secrets()` |
| `port` | env/secret | Sim | Redis / `CacheManage` | erro em `required_secrets()` |
| `password` | env/secret | Não | Redis | fica `None` |
| `origin` | env/secret | Sim | CORS | erro em `required_secrets()` |
| `rate_limit` | env/secret | Sim para rate limit | middleware | erro quando o middleware tenta ler o limite |
| `secret` | env/secret | Sim para auth | JWT / rotas protegidas / refresh | autenticação não consegue funcionar corretamente |
| `url_db` | env/secret | Não | banco | usa fallback SQLite |
| `path` | config | Não | fallback SQLite | usa `sqlite+aiosqlite:///watch.db` |

### Prioridade do banco

| `url_db` | `path` | Banco usado |
| --- | --- | --- |
| definida | qualquer valor | usa `url_db` |
| `None` | diretório existente | `<path>/watch.db` |
| `None` | `None` | `watch.db` na raiz de execução |

---

## 5. Exemplo de `.env`

Configuração mínima típica usando Redis, autenticação e SQLite padrão:

```env
host=localhost
port=6379
origin=http://localhost:3000
rate_limit=100
secret=troque-esta-secret
```

Redis com senha:

```env
password=minha-senha
```

Banco externo opcional:

```env
url_db=postgresql+asyncpg://usuario:senha@localhost:5432/watchguardian
```

Se `url_db` não existir, isso não é erro. O sistema pode usar SQLite.

---

## 6. Criando o servidor

### 6.1 Usando o SQLite padrão

```python
from src.server.manage import Server
from src.service.module import Settings

settings = Settings(env_file=".env")

settings.add_secret([
    "host",
    "port",
    "password",
    "origin",
    "rate_limit",
    "secret",
    "url_db",
])

app = Server(settings=settings).run()
```

Mesmo registrando `url_db`, ela pode estar ausente no ambiente. Nesse caso `get_secret("url_db")` retorna `None` e o banco cai no fallback.

Sem `url_db` e sem `path`, o banco será:

```text
sqlite+aiosqlite:///watch.db
```

### 6.2 Escolhendo a pasta do SQLite

```python
from src.server.manage import Server
from src.service.module import Settings

settings = Settings(env_file=".env")

settings.add_secret([
    "host",
    "port",
    "password",
    "origin",
    "rate_limit",
    "secret",
    "url_db",
])

settings.add_config({
    "name": "path",
    "value": "./data"
})

app = Server(settings=settings).run()
```

Nesse exemplo, se `url_db` for `None`, o banco será criado/usado em:

```text
./data/watch.db
```

O diretório `./data` precisa existir antes.

### 6.3 Usando banco externo

Basta definir `url_db`:

```env
url_db=postgresql+asyncpg://usuario:senha@localhost:5432/watchguardian
```

Quando `url_db` existe, ela tem prioridade e `path` não interfere.

---

## 7. `app.state`

O `Server` salva o `Settings` globalmente na aplicação:

```python
self.app.state.settings = settings
```

Nos handlers:

```python
settings = request.app.state.settings
```

Use `app.state` para objetos compartilhados pela aplicação, como configurações e clientes globais.

Para informações específicas de uma requisição, use `request.state`.

---

## 8. Executando com Uvicorn

Supondo que o objeto `app` esteja em `main.py`:

```bash
uvicorn main:app --reload
```

Para expor na rede:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Documentação automática do FastAPI:

```text
/docs
/redoc
```

---

## 9. Autenticação das rotas

As rotas de logs e observabilidade usam `depends_user`.

O token normal é um JWT com:

```json
{
  "exp": "2026-10-10T18:30:00+00:00",
  "type": "user_token"
}
```

O `exp` é salvo como string ISO UTC.

O `refresh_token` possui:

```json
{
  "type": "refresh_token"
}
```

No formato atual ele não possui `exp`.

---

## 10. Gerando tokens pela CLI

User token:

```bash
python -m src.cli.main auth --env-file .env token --type user_token
```

Com payload:

```bash
python -m src.cli.main auth --env-file .env token --type user_token --payload '{"user_id":"123","role":"admin"}'
```

Refresh token:

```bash
python -m src.cli.main auth --env-file .env token --type refresh_token --payload '{"user_id":"123"}'
```

Gerar secret:

```bash
python -m src.cli.main auth secret
```

---

## 11. Endpoint de refresh

```http
POST /auth/refresh
```

Esse endpoint não usa `Depends` de propósito, porque ele precisa aceitar o token normal antigo para gerar outro.

Headers obrigatórios:

```text
X-user_token: <user-token-antigo>
X-refresh_token: <refresh-token>
```

Fluxo:

1. recebe os dois tokens;
2. valida a assinatura;
3. exige `type=user_token` no token normal;
4. exige `type=refresh_token` no refresh;
5. copia o payload do token antigo;
6. remove `exp` e `type` antigos;
7. cria um novo `user_token` com nova expiração.

Resposta:

```json
{
  "token": "<novo-user-token>"
}
```

---

## 12. Rotas de logs

Prefixo:

```text
/logs
```

### Criar

```http
POST /logs/
```

```json
{
  "status": "INFO",
  "log": "Servidor iniciado"
}
```

Status aceitos:

```text
SUCCESS
INFO
WARNING
ERROR
DEBUG
CRITICAL
```

### Buscar

Todos:

```http
GET /logs/
```

Por ID:

```http
GET /logs/?id=1
```

Por `public_id`:

```http
GET /logs/?public_id=<uuid>
```

### Atualizar

```http
PATCH /logs/?id=1
```

Body parcial:

```json
{
  "status": "ERROR"
}
```

### Deletar

```http
DELETE /logs/?id=1
```

---

## 13. Rotas de observabilidade

Prefixo:

```text
/obs
```

### Criar

```http
POST /obs/
```

```json
{
  "task": "process_data",
  "status": "pending",
  "content": "Task iniciada",
  "latency": 0
}
```

Status aceitos atualmente:

```text
sucess
pending
failure
```

`sucess` está escrito dessa forma no contrato atual do projeto.

### Buscar

Todos:

```http
GET /obs/
```

Por ID:

```http
GET /obs/?id=1
```

Por `public_id`:

```http
GET /obs/?public_id=<uuid>
```

### Atualizar

```http
PATCH /obs/?id=1
```

```json
{
  "status": "sucess",
  "content": "Task concluída",
  "latency": 128
}
```

Campos atualizáveis:

```text
task
status
content
latency
```

### Deletar

```http
DELETE /obs/?id=1
```

---

## 14. Redis e rate limit

O `CacheManage` é criado no `Server` e usa Redis para o rate limit.

Exemplo local:

```bash
docker run --name watchguardian-redis -p 6379:6379 redis:latest
```

Configuração mínima:

```env
host=localhost
port=6379
rate_limit=100
```

`password` só é necessária quando o Redis exigir senha.

---

## 15. Banco e tabelas

Os handlers criam o banco com o mesmo `Settings` salvo no `app.state`:

```python
settings = request.app.state.settings
control_db = await WatchDb(settings=settings)
```

Depois usam:

```python
control_db.logs
control_db.observability
```

Operações disponíveis:

```text
create
select
update
delete
```

O banco não exige uma `url_db` externa. Sem `url_db`, o WatchGuardian usa o fallback SQLite descrito anteriormente.
