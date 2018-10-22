alerta
------

add to /etc/alertad.conf

```
	AUTH_PROVIDER = 'cas'
	AUTH_REQUIRED = True

	OAUTH2_CLIENT_ID = 'client_id'
	OAUTH2_CLIENT_SECRET = 'client_secret'
	CAS_URL = 'https://cas_url'
	ALLOWED_CAS_GROUPS = ['*']
```



alerta-webui
------------
add to js/auth.js
```
	$authProvider.oauth2({
	  name: 'cas',
	  url: config.endpoint + '/auth/cas',
	  redirectUri: window.location.origin,
	  clientId: config.client_id,
	  requiredUrlParams: [],
	  authorizationEndpoint: config.cas_url + '/cas/oauth2.0/authorize'
	});
```