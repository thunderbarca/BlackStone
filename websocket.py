# 异步函数
async def websocket_application(scope, receive, send):
    """
      var connection = new WebSocket('ws://127.0.0.1:8000/abc')

      scope: <class 'dict'> 详细如下
          {'type': 'websocket',
          'path': '/abc',
          'raw_path': b'/abc',
          'headers': [(b'host', b'127.0.0.1:8000'), (b'upgrade', b'WebSocket'), (b'connection', b'Upgrade'),
                      (b'sec-websocket-version', b'13'), (b'sec-websocket-key', b'2viLa4ZBnF2953ARONVITw=='),
                      (b'accept', b'*/*'), (b'accept-encoding', b'gzip, deflate'), (b'user-agent', b'Python/3.8 aiohttp/3.6.2')],
          'query_string': b'',
          'client': ['127.0.0.1', 47220],
          'server': ['127.0.0.1', 8000],
          'subprotocols': [],
          'asgi': {'version': '3.0'}}

      receive: <class 'method'> 详细如下
          <bound method Queue.get of <Queue at 0x7f92b14df5b0 maxsize=0 _queue=[{'type': 'websocket.connect'}] tasks=1>>

      send: <class 'function'>

    """
    while True:
        event = await receive()

        if event['type'] == 'websocket.connect':
            await send({
                'type': 'websocket.accept'
            })

        if event['type'] == 'websocket.disconnect':
            break

        if event['type'] == 'websocket.receive':
            if event['text'] == 'ping':
                await send({
                    'type': 'websocket.send',
                    'text': 'pong!'
                })
