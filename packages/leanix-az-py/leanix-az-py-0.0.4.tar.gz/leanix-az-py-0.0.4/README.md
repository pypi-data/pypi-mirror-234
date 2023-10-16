# LeanIX Python Library for Azure


This package provides two basic functions used during the development of every Azure Function. 


This package contains :

#auth:  For authentication
```
-getBearerToken(base_url, api_token) returns the authentication header
```

#graphql: For managing GraphQL stuff.
```
-runGraphql(header, json_data) runs the given graphql query
```

TODO:
------
```
-LOTS
```

Useage
------
```
Example:
from leanixpy_az import graphql  

graphql.runGraphql(<Header>, <Query>)
```
