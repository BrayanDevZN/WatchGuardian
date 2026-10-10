# WatchGuardian Server

Este documento explica como configurar, iniciar e consumir o servidor HTTP do WatchGuardian.

O servidor é construído sobre FastAPI e atualmente reúne as rotas de logs, observabilidade e autenticação/refresh de token.

---

## 1. Estrutura do servidor

A implementação do servidor fica em:

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

- `manage.py`: cria a aplicação FastAPI, registra CORS, rotas e middleware.
- `midlleware.py`: aplica rate limit usando Redis.
- `depends.py`: valida o token de usuário nas rotas protegidas.
- `handles/logs.py`: CRUD HTTP de logs.
- `handles/obs.py`: CRUD HTTP de observabilidade.
- `handles/auth.py`: gera um novo `user_token` usando o token antigo e um `refresh_token`.
- `schema/`: contém os schemas Pydantic usados nas entradas das rotas.

---

## 2. Criando o Settings

O `Server` recebe um objeto `Settings` já configurado.

Exemplo usando um arquivo `.env`:

```python
from src.service.module import Settings

settings = Settings(env_file=".env")
```

Ou deixando o `python-dotenv` procurar o `.env` padrão:

```python
settings = Settings()
```

Importante: carregar o arquivo `.env` não adiciona automaticamente as variáveis ao dicionário interno de `Settings`.

Antes de iniciar o servidor, registre as variáveis necessárias com `add_secret()`:

```python
settings.add_secret([
    "host",
    "port",
    "password",
    "origin",
    "rate_limit",
    "secret",
    "url",
])
```

Variáveis opcionais podem continuar com valor `None`, desde que o módulo que as consome aceite isso.

---

## 3. Variáveis de ambiente

### 3.1 Redis

O servidor usa Redis no middleware de rate limit.

Variáveis:

```env
host=localhost
port=6379
password=
```

Descrição:

| Variável | Obrigatória | Uso |
| --- | --- | --- |
| `host` | Sim | Host do Redis. |
| `port` | Sim | Porta do Redis. |
| `password` | Não | Senha do Redis. Pode ser `None` quando a instância não exige autenticação. |

O `CacheManage` usa essas variáveis para criar a conexão Redis.

---

### 3.2 Rate limit

```env
rate_limit=100
```

`rate_limit` define a quantidade máxima de requisições permitida pelo middleware dentro da janela controlada pelo cache.

O valor é carregado como string pelo ambiente e convertido para `int` no middleware.

Exemplo:

```env
rate_limit=100
```

---

### 3.3 CORS / Origin

```env
origin=http://localhost:3000
```

`origin` define quais origens podem acessar a API pelo navegador.

Exemplo para um único frontend:

```env
origin=http://localhost:3000
```

Se forem usadas várias origens, mantenha o formato esperado pela configuração da aplicação e garanta que o valor seja convertido para uma lista antes de ser entregue ao `CORSMiddleware`.

---

### 3.4 JWT Secret

```env
secret=uma-secret-segura
```

`secret` é usada para assinar e validar os JWTs do WatchGuardian.

Ela é necessária para:

- validar `user_token`;
- validar `refresh_token`;
- criar novos tokens;
- usar o endpoint `/auth/refresh`.

A mesma secret deve ser usada para gerar e validar os tokens.

Também é possível gerar uma secret pela CLI do projeto:

```bash
python -m src.cli.main auth secret
```

Esse comando imprime a secret. Ele não grava automaticamente o valor no `.env`.

---

### 3.5 Banco de dados

A URL do banco é lida pela variável:

```env
url=postgresql+asyncpg://usuario:senha@localhost:5432/watchguardian
```

`url` é opcional na camada `WatchDb`.

Quando ela não estiver configurada, `config_url()` pode usar o caminho local configurado pelo projeto para criar a URL alternativa de banco.

Para disponibilizar a variável no `Settings`:

```python
settings.add_secret("url")
```

Se quiser fornecer um caminho por configuração interna:

```python
settings.add_config({
    "name": "path",
    "value": "./data.db"
})
```

---

## 4. Exemplo de `.env`

Exemplo completo para desenvolvimento local:

```env
host=localhost
port=6379
password=

origin=http://localhost:3000
rate_limit=100

secret=troque-esta-secret

url=sqlite+aiosqlite:///./watchguardian.db
```

Em produção, não versione secrets reais no Git.

---

## 5. Criando o servidor

Importe `Server` diretamente de `src.server.manage`:

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
    "url",
])

server = Server(settings=settings)
app = server.run()
```

O `run()` retorna a instância do FastAPI.

O `Server` também salva o objeto `Settings` no estado global da aplicação:

```python
app.state.settings
```

Isso permite que handlers recuperem a mesma configuração sem recriar `Settings` em cada requisição.

---

## 6. Executando com Uvicorn

Supondo que o código anterior esteja em um arquivo `main.py` na raiz:

```bash
uvicorn main:app --reload
```

Para expor na rede:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

A documentação automática do FastAPI normalmente fica disponível em:

```text
/docs
/redoc
```

---

## 7. Rotas de logs

Prefixo:

```text
/logs
```

As rotas de logs usam `depends_user` e, portanto, são rotas protegidas.

### 7.1 Criar log

```http
POST /logs/
```

Body:

```json
{
  "status": "INFO",
  "log": "Servidor iniciado"
}
```

Status aceitos pelo schema:

```text
SUCCESS
INFO
WARNING
ERROR
DEBUG
CRITICAL
```

---

### 7.2 Buscar logs

Buscar todos:

```http
GET /logs/
```

Buscar por ID:

```http
GET /logs/?id=1
```

Buscar por `public_id`:

```http
GET /logs/?public_id=<uuid>
```

`id` e `public_id` são opcionais. Sem os dois, a camada de banco pode retornar todos os registros.

---

### 7.3 Atualizar log

```http
PATCH /logs/?id=1
```

ou:

```http
PATCH /logs/?public_id=<uuid>
```

Body parcial:

```json
{
  "status": "ERROR"
}
```

Também é possível enviar:

```json
{
  "log": "Novo conteúdo",
  "status": "WARNING"
}
```

---

### 7.4 Deletar log

```http
DELETE /logs/?id=1
```

ou:

```http
DELETE /logs/?public_id=<uuid>
```

---

## 8. Rotas de observabilidade

Prefixo:

```text
/obs
```

Essas rotas também usam autenticação por token.

### 8.1 Criar observabilidade

```http
POST /obs/
```

Body:

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

Observação: `sucess` está escrito dessa forma no contrato atual do projeto.

---

### 8.2 Buscar observabilidade

Todos os registros:

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

---

### 8.3 Atualizar observabilidade

```http
PATCH /obs/?id=1
```

Body parcial:

```json
{
  "status": "sucess",
  "content": "Task concluída",
  "latency": 128
}
```

Os campos atualizáveis são:

```text
task
status
content
latency
```

---

### 8.4 Deletar observabilidade

```http
DELETE /obs/?id=1
```

ou:

```http
DELETE /obs/?public_id=<uuid>
```

---

## 9. Autenticação

O WatchGuardian possui dois tipos de token:

```text
user_token
refresh_token
```

### 9.1 User token

O `user_token` possui expiração automática de uma hora.

O payload gerado inclui:

```json
{
  "exp": "2026-10-10T18:30:00+00:00",
  "type": "user_token"
}
```

Campos extras podem ser adicionados ao payload.

Exemplo:

```python
token = await auth.user_token(
    payload={
        "user_id": "123",
        "role": "admin"
    }
)
```

---

### 9.2 Refresh token

O `refresh_token` não possui `exp` no formato atual do projeto.

Payload básico:

```json
{
  "type": "refresh_token"
}
```

Exemplo:

```python
refresh = await auth.refresh_token(
    payload={
        "user_id": "123"
    }
)
```

---

## 10. Gerando tokens pela CLI

User token:

```bash
python -m src.cli.main auth --env-file .env token --type user_token
```

Com payload adicional:

```bash
python -m src.cli.main auth --env-file .env token --type user_token --payload '{"user_id":"123","role":"admin"}'
```

Refresh token:

```bash
python -m src.cli.main auth --env-file .env token --type refresh_token --payload '{"user_id":"123"}'
```

Para esses comandos, a variável `secret` precisa estar carregada pelo fluxo da CLI.

---

## 11. Endpoint de refresh

O endpoint de refresh não usa `Depends` de propósito.

Isso permite que um `user_token` antigo seja recebido para gerar um novo token, em vez de a dependency rejeitar a requisição antes do handler executar.

Endpoint:

```http
POST /auth/refresh
```

Headers obrigatórios:

```text
X-user_token: <user-token-antigo>
X-refresh_token: <refresh-token>
```

O handler:

1. recebe os dois tokens;
2. valida a assinatura de ambos;
3. exige `type=user_token` no token normal;
4. exige `type=refresh_token` no refresh token;
5. copia o payload do token antigo;
6. remove `exp` e `type` antigos;
7. gera um novo `user_token`, com uma nova expiração.

Resposta:

```json
{
  "token": "<novo-user-token>"
}
```

---

## 12. Estado global da aplicação

O servidor salva `Settings` em:

```python
self.app.state.settings = settings
```

Dentro de um handler, o valor pode ser recuperado com:

```python
settings = request.app.state.settings
```

Use `app.state` para objetos compartilhados pela aplicação, como configurações e clientes reutilizáveis.

Não use `app.state` para dados específicos de um usuário ou de uma única requisição.

Para dados específicos da requisição, use:

```python
request.state
```

---

## 13. Redis e rate limit

O middleware utiliza `CacheManage` para contar requisições no Redis.

O Redis precisa estar disponível antes do servidor começar a processar requisições protegidas pelo middleware.

Exemplo local:

```bash
docker run --name watchguardian-redis -p 6379:6379 redis:latest
```

Com isso:

```env
host=localhost
port=6379
password=
```

O limite é definido por:

```env
rate_limit=100
```

---

## 14. Banco e tabelas

Os handlers de logs e observabilidade criam `WatchDb` usando o mesmo `Settings` armazenado no `app.state`:

```python
settings = request.app.state.settings
control_db = await WatchDb(settings=settings)
```

Depois utilizam:

```python
control_db.logs
control_db.observability
```

As operações disponíveis nas rotas são:

```text
create
select
update
delete
```

---

## 15. Exemplo completo de inicialização

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
    "url",
])

settings.add_config({
    "name": "path",
    "value": "./watchguardian.db"
})

app = Server(settings=settings).run()
```

Depois:

```bash
uvicorn main:app --reload
```

---

## 16. Resumo das variáveis

| Nome | Necessária para | Obrigatória |
| --- | --- | --- |
| `host` | Redis / cache / rate limit | Sim |
| `port` | Redis / cache / rate limit | Sim |
| `password` | Redis autenticado | Não |
| `origin` | CORS | Sim |
| `rate_limit` | Middleware de rate limit | Sim |
| `secret` | JWT, autenticação e refresh | Sim para auth |
| `url` | Banco de dados externo | Não, possui fluxo de fallback |

Config adicional:

| Nome | Uso |
| --- | --- |
| `path` | Caminho usado pelo fallback de banco quando necessário |

---

## 17. Observações sobre a implementação atual

A documentação acima descreve a API e a intenção atual do módulo `server`.

Ao alterar os nomes de headers, payloads JWT, variáveis de ambiente ou schemas, mantenha este arquivo atualizado para evitar que o código e a documentação desenvolvam carreiras independentes, tradição infelizmente comum em software.
