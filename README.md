:rotating_light: :computer: :rotating_light:
# Roam (Backend)
> An augmented reality game set in a futuristic post-apocalyptic world. Battle your enemies, team up with your friends, scavenge for inventory items and conquer bosses!

## Purpose
Our backend server is in charge of data storage, GeoJSON location-based polygon shape generation, AI-based generation of items and bosses, user authentication, live multiplayer tallying (both of scores and positions), weather checkup (to augment game environment) and other sorts of stuff. Of course, this is all accessible both as a RESTful API and as a realtime websocket-based interface!

## API Routes

* POST _/signup_
  * Request Body: `{username:string, password:string}` 
  * Response: `{status:int, message:"success"|"failure"}`
* POST _/login_
  * Request Body: `{username:string, password:string}`
  * Response: JWT Token that is then passed to the Auth-Header

* GET _/user/me/account_
  * Request: Auth Header - User's JWT Token
  * Response: `{username:string, xp:int, inventory:{string:int}}` 
* POST _/user/me/account_
  * Request: Auth Header - User's JWT Token
  * Response: `{username:string, xp:int, inventory:{string:int}}`

* GET _/maprender_

## Technology Stack
We used the following technology stack for our game:
* :globe_with_meridians: **GeoJSON** - a way to efficiently represent location-based geometric data using JSON, one of the most preferred data exchange formats in the internet
* :baggage_claim: **MongoDB** - for querying and storing location-based geometric data
* :baggage_claim: **Postgres** - good ol' relational database to store good ol' relational data
* :snake: **Python** - backend application server language of choice
* :whale: **Docker** - for containerizing our backend application


