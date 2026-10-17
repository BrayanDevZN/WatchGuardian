# Eventos em tempo real

O servidor WatchGuardian oferece WebSockets autenticados para acompanhar novos registros de logs e observabilidade. Os canais são separados: cada conexão recebe apenas a categoria que solicitou.

## Endpoints

| WebSocket | Eventos |
| --- | --- |
| `/logs/ws` | `logs.created`, `logs.updated`, `logs.deleted` |
| `/obs/ws` | `observability.created`, `observability.updated`, `observability.deleted` |

Use `ws://` em desenvolvimento sem TLS e `wss://` atrás de HTTPS.

Os eventos são emitidos pelas operações HTTP correspondentes do WatchGuardian Server depois da gravação ou alteração do registro. Usar diretamente `WatchDb` em outro processo não publica automaticamente um evento no servidor.

## Autenticação

Cada conexão exige um JWT válido do tipo `user_token`. O servidor aceita o token em uma destas formas:

```text
X-user_token: <token>
Authorization: Bearer <token>
```

Ou como query string, para clientes que não permitem definir headers:

```text
ws://localhost:8000/logs/ws?token=<token>
```

Prefira os headers quando disponíveis; tokens na URL podem acabar em logs de proxy ou infraestrutura. Se o token for ausente, inválido ou não for do tipo `user_token`, o servidor fecha a conexão com código `4401`. Uma origem WebSocket que não está na lista `origin` configurada é fechada com código `4403`.

## Formato das mensagens

Cada mensagem é um objeto JSON:

```json
{
  "id": "uuid-do-evento",
  "type": "logs.created",
  "timestamp": "2026-10-17T15:00:00+00:00",
  "data": {
    "id": 1,
    "public_id": "uuid-do-registro",
    "status": "INFO",
    "log": "Servidor iniciado",
    "created_at": "2026-10-17T15:00:00"
  }
}
```

`type` identifica a ação e `data` contém o registro. No canal `/obs/ws`, o registro também inclui `group`, `task`, `latency` e `memory_bytes`. Datas e UUIDs são convertidos para strings para o transporte JSON.

O servidor responde `pong` quando recebe a mensagem de texto `ping`. O cliente Python atual não envia pings da aplicação automaticamente; a biblioteca WebSocket mantém o heartbeat do protocolo.

## Cliente Python

`ClientHttp` fornece dois iteradores assíncronos:

O cliente usa a dependência `websockets`, incluída nas dependências do projeto. Se instalar o código-fonte manualmente, instale as dependências por `pip install -e .` ou `pip install -r requirements.txt`.

```python
async for event in client.listen_logs(token=user_token):
    print(event["type"], event["data"])

async for event in client.listen_obs(token=user_token):
    print(event["type"], event["data"])
```

Cada iterador abre uma conexão própria. Para escutar os dois ao mesmo tempo, rode-os concorrentemente:

```python
import asyncio

async def main():
    async def receive_logs():
        async for event in client.listen_logs(token=user_token):
            print("log:", event)

    async def receive_obs():
        async for event in client.listen_obs(token=user_token):
            print("observabilidade:", event)

    await asyncio.gather(receive_logs(), receive_obs())

asyncio.run(main())
```

O cliente converte `http://` em `ws://` e `https://` em `wss://`, e envia o token pelo header `X-user_token`. Os métodos não fazem reconexão automática: erros de conexão são propagados e a aplicação consumidora decide quando tentar novamente.

## CLI

Os comandos `server logs` e `server obs` fazem uma consulta HTTP e encerram por padrão. A opção `--realtime` é `false` por padrão; quando presente, o comando conecta ao WebSocket correspondente e continua exibindo eventos até a conexão ser encerrada, por exemplo com Ctrl+C.

```bash
watchguardian server logs --token SEU_TOKEN --realtime
watchguardian server obs --token SEU_TOKEN --realtime
```

O token pode vir de `--token` ou do secret `token` do projeto carregado com `--project`.

## Redis, escopo e limites

O servidor sempre distribui eventos aos WebSockets do mesmo processo. Se `host` e `port` estiverem configurados, ele também publica e escuta o canal Redis `watchguardian:realtime`, permitindo entrega entre instâncias.

Sem Redis configurado ou disponível, a entrega fica limitada ao processo local. Redis Pub/Sub não guarda histórico: eventos publicados enquanto um cliente está desconectado não são repetidos quando ele reconecta. Para consultar registros existentes, use as rotas HTTP de logs e observabilidade.

Cada conexão tem uma fila de até 256 eventos. Se ela encher, o evento mais antigo daquela conexão é descartado. O rate limit HTTP continua usando Redis e não é executado nas conexões WebSocket.

Sem Redis configurado ou disponível, o servidor pode iniciar e os WebSockets podem receber eventos locais, mas as rotas HTTP respondem `503` porque o middleware de rate limit depende do Redis.

## Testes

Execute os testes relacionados com:

```bash
python -m tests.unit.realtime_client
python -m tests.unit.realtime_ws
python -m tests.unit.server_middleware
```

Eles cobrem URL e header do cliente, autenticação no servidor, rejeição de token inválido, isolamento dos canais e respostas do rate limit Redis HTTP.
