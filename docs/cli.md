# CLI WatchGuardian

A CLI oficial é `watchguardian`. Ela oferece os grupos `project`, `migrate`, `auth`, `server` e `balance`.

Instale ou atualize o pacote:

```bash
python -m pip install --upgrade watchguardian
```

Confira a ajuda geral ou a ajuda de um grupo/subcomando:

```bash
watchguardian --help
watchguardian project --help
watchguardian migrate --help
watchguardian auth --help
watchguardian server --help
watchguardian balance --help
```

Também existe o executável `watchguardian-project`, que aceita os mesmos subcomandos de `project`.

## Gerenciar um projeto

### Criar

```bash
watchguardian project start
watchguardian project start --path ./apps --name api
watchguardian project start --with_env
watchguardian project start --env-file ./config/.env
watchguardian project start --with_env --env-file ./config/.env
```

| Opção | Efeito |
| --- | --- |
| `--path PASTA` | Pasta pai onde o projeto será criado. Padrão: diretório atual. |
| `--name NOME` | Nome da pasta gerada, convertido para minúsculas. Se omitido, usa `watchguardian`. |
| `--env-file ARQUIVO` | Arquivo de ambiente existente. O caminho é resolvido antes de ser salvo no projeto. |
| `--with_env` ou `--with-env` | Cria um arquivo `.env` dentro do projeto com secrets e configs locais. |

Sem opções, cria `./watchguardian`. `watchguardian project start --path ./apps --name api` cria `./apps/api`. O nome `watchguardian` é reservado para o padrão; omita `--name` para usar esse padrão.

Se `--env-file` for usado sem `--with_env`, o projeto aponta para o arquivo informado. Se ambas as opções forem usadas, os valores do arquivo informado são copiados para o `.env` gerado e prevalecem sobre os defaults correspondentes. Variáveis ausentes recebem defaults locais. Um projeto com arquivo de ambiente externo usa `http = true`; com `--with_env`, usa modo local (`http = null`).

O `.env` gerado contém as chaves de secret `host`, `port`, `password`, `origin`, `rate_limit`, `secret`, `url`, `token` e `url_db`, além das configs `path` e `replicator_*`. O `settings.json` guarda o caminho do ambiente e as configs do projeto. Não publique o `.env`: ele pode conter credenciais e o secret de autenticação.

### Resetar

```bash
watchguardian project reset
watchguardian project reset --project ./apps/api
```

Sem `--project`, usa `./watchguardian`. O reset restaura os defaults em `settings.json` e recria o `.env` com valores locais. Isso substitui o `.env` existente, inclusive valores personalizados.

`project reset` restaura a configuração do projeto. Não confunda com `migrate reset`, que atua nas tabelas do banco.

### Excluir

```bash
watchguardian project delete
watchguardian project delete --project ./apps/api
```

Sem `--project`, usa `./watchguardian`. O comando remove a pasta inteira do projeto e tudo que estiver nela. Confira o caminho antes de executar.

### Usar o app no Python

O projeto gerado exporta `app` em `main.py`. Para uma pasta chamada `api`:

```python
import asyncio
from api.main import app

async def main():
    modules = await app.load_module()
    await modules.watch_db.create_tables()

asyncio.run(main())
```

`app.load_module()` carrega todos os módulos e retorna o `WatchModule`. Após a carga, as instâncias também ficam acessíveis por propriedades como `app.watch_db`, `app.watch_logs`, `app.watch_auth`, `app.client_http`, `app.watch_server` e `app.watch_balance`. Execute esse exemplo do diretório pai do pacote gerado ou adicione esse diretório ao `PYTHONPATH`.

## Descoberta automática de projeto

`migrate`, `auth`, `server` e `balance` aceitam `--project` onde indicado nas seções abaixo. Sem essa opção, o CLI procura exatamente `./watchguardian` no diretório atual. Para um nome ou local personalizado, informe o caminho, por exemplo `--project ./apps/api`.

Se não houver o projeto padrão, os comandos tentam usar o `.env` do diretório atual ou o arquivo indicado por `--env-file`, quando disponível. Se faltarem as configurações necessárias, encerram com erro. `auth secret` pode gerar um secret sem projeto. Os comandos do balanceador também podem receber as réplicas diretamente como `modulo:atributo`.

## Banco de dados: migrate

```bash
watchguardian migrate make_tables
watchguardian migrate reset
watchguardian migrate drop
```

| Subcomando | Ação |
| --- | --- |
| `make_tables` | Cria tabelas que ainda não existem. |
| `reset` | Reseta as tabelas do banco. |
| `drop` | Remove as tabelas. |

No projeto gerado, o SQLite usa por padrão `<projeto>/data/watch.db`. `--path` troca o diretório e salva a escolha em `settings.json`.

```bash
watchguardian migrate make_tables --project ./apps/api
watchguardian migrate make_tables --project ./apps/api --path ./storage
watchguardian migrate --project ./apps/api reset
watchguardian migrate --env-file .env.production make_tables
```

`--project` e `--path` podem aparecer antes ou depois do subcomando. `--env-file` vem antes do subcomando. Sem projeto, migrate exige um arquivo de ambiente existente ou variáveis de banco no ambiente do processo.

`migrate reset` e `migrate drop` podem remover dados ou tabelas; confira o alvo antes de executá-los.

## Autenticação: auth

### Gerar um secret

```bash
watchguardian auth secret
watchguardian auth secret --project ./apps/api
```

Sem projeto, `secret` gera e mostra um novo secret. Com projeto, usa as configurações desse projeto.

### Gerar tokens

```bash
watchguardian auth token --type user_token
watchguardian auth token --type refresh_token --payload '{"user_id":"123"}'
watchguardian auth token --type user_token --project ./apps/api
watchguardian auth --env-file .env token --type user_token
```

`--type` é obrigatório e aceita `user_token` ou `refresh_token`. `--payload` recebe uma string JSON. O comando precisa do secret `secret` no projeto ou no ambiente.

## Servidor: server

### Iniciar

```bash
watchguardian server run --project ./apps/api
watchguardian server run --project ./apps/api --host 0.0.0.0 --port 8080
watchguardian server run --project ./apps/api --detached
watchguardian server --env-file .env run main:app
```

| Argumento | Descrição |
| --- | --- |
| `app` | Alvo ASGI `modulo:objeto`; necessário sem projeto, por exemplo `main:app`. |
| `--project PASTA` | Projeto gerado. Sem a opção, procura `./watchguardian`. |
| `--host` | Endereço de escuta. Padrão: `127.0.0.1`. |
| `--port` | Porta do servidor. Padrão: `8000`. |
| `--detached` | Inicia em segundo plano. |
| `--env-file ARQUIVO` | Configuração sem projeto; deve aparecer antes de `run`. |

Sem projeto, use um alvo ASGI e configure o ambiente para o banco. O CLI cria as tabelas antes de executar o app.

### Consultar logs e observabilidade

```bash
watchguardian server logs
watchguardian server obs
watchguardian server logs --project ./apps/api --token SEU_TOKEN
watchguardian server obs --project ./apps/api --realtime
watchguardian server --env-file .env logs --realtime
```

`logs` consulta logs; `obs` consulta registros de observabilidade. `--token` substitui o token configurado. Sem a opção, o CLI lê `token` do projeto ou ambiente. `--realtime` mantém a conexão WebSocket aberta para receber novos eventos. Sem projeto, configure a URL do servidor em `url` e forneça um token válido.

## Balanceador: balance

### Iniciar

```bash
watchguardian balance create --project ./apps/api
watchguardian balance create --project ./apps/api --host 0.0.0.0 --port 8081
watchguardian balance create --project ./apps/api --detached
watchguardian balance create myconfig:replicas --host 127.0.0.1 --port 8000
```

Com projeto, as réplicas vêm das configs `replicator_*`. Sem projeto, forneça um alvo `modulo:atributo` que seja um `Replicators`, uma lista de `Replicator` ou uma função que retorne um desses valores.

Opções de `create`: alvo opcional, `--project`, `--host`, `--port` e `--detached`.

### Verificar réplicas e consultar logs

```bash
watchguardian balance valid --project ./apps/api
watchguardian balance valid myconfig:replicas
watchguardian balance logs --project ./apps/api --token SEU_TOKEN
watchguardian balance logs myconfig:replicas --env-file .env
```

`valid` lista réplicas saudáveis. `logs` consulta logs nas réplicas saudáveis; use `--token` ou configure `token` no ambiente. `logs` aceita `--env-file` para apontar o arquivo usado para obter o token. `valid` e `logs` também aceitam um alvo `modulo:atributo` sem projeto.

## Onde informar as opções

As opções devem acompanhar o grupo ou subcomando que as define. Por exemplo, em `auth` e `server`, `--env-file` vem antes de `token`, `logs` ou `run`. Em `balance`, `--env-file` só está disponível em `balance logs`. Consulte `watchguardian <grupo> --help` para a sintaxe instalada.

Para projetos gerados, o arquivo de ambiente é carregado e os valores ausentes recebem defaults locais. Sem projeto, configure no `.env`, em `--env-file` quando disponível ou nas variáveis do processo.
