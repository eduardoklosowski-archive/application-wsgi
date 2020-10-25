from socket import gethostname


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)

    http_values = ''.join(
        '<tr><td>%s</td><td>%s</td></tr>' % (k, v)
        for k, v in sorted(
            (k, v)
            for k, v in environ.items()
            if k.startswith('HTTP_')
        )
    )

    yield str('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>%(hostname)s</title>
    <style>
      body { background-color: #c0c0c0; font-family: sans-serif }
      table { border: 1px solid #000000; border-collapse: collapse }
      th, td { background-color: #ffffff; border: 1px solid #000000; padding: 5px }
    </style>
  </head>
  <body>
    <h1>Server: %(hostname)s</h1>
    <table>
      <thead>
        <tr><th>Name</th><th>Value</th></tr>
      </thead>
      <tbody>
        <tr><td>REQUEST_METHOD</td><td>%(request_method)s</td></tr>
        <tr><td>SCRIPT_NAME</td><td>%(script_name)s</td></tr>
        <tr><td>PATH_INFO</td><td>%(path_info)s</td></tr>
        <tr><td>QUERY_STRING</td><td>%(query_string)s</td></tr>
        <tr><td>CONTENT_TYPE</td><td>%(content_type)s</td></tr>
        <tr><td>CONTENT_LENGTH</td><td>%(content_length)s</td></tr>
        <tr><td>SERVER_NAME</td><td>%(server_name)s</td></tr>
        <tr><td>SERVER_PORT</td><td>%(server_port)s</td></tr>
        <tr><td>SERVER_PROTOCOL</td><td>%(server_protocol)s</td></tr>
        %(http_values)s
      </tbody>
    </table>
  </body>
</html>''' % {
        'hostname': gethostname(),
        'request_method': environ.get('REQUEST_METHOD'),
        'script_name': environ.get('SCRIPT_NAME'),
        'path_info': environ.get('PATH_INFO'),
        'query_string': environ.get('QUERY_STRING'),
        'content_type': environ.get('CONTENT_TYPE'),
        'content_length': environ.get('CONTENT_LENGTH'),
        'server_name': environ.get('SERVER_NAME'),
        'server_port': environ.get('SERVER_PORT'),
        'server_protocol': environ.get('SERVER_PROTOCOL'),
        'http_values': http_values,
    }).encode('utf-8')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8000, application)
    print('Serving on port 8000...')
    httpd.serve_forever()
