:rotating_light: :computer: :rotating_light:
# Roam (Backend)
> An augmented reality game set in a futuristic post-apocalyptic world. Battle your enemies, team up with your friends, scavenge for inventory items and conquer bosses!

## Purpose
Our backend server is in charge of data storage, GeoJSON location-based polygon shape generation, AI-based generation of items and bosses, user authentication, live multiplayer tallying (both of scores and positions), weather checkup (to augment game environment) and other sorts of stuff. Of course, this is all accessible both as a RESTful API and as a realtime websocket-based interface!

## TechStack
We used the following technology stack for our game:
* :baggage_claim: **Redis** - quick in-memory key-value store for storing user location
* :baggage_claim: **Postgres** - good ol' relational database to store good ol' relational data. We'll also be using the Postgres `PostGIS` 
* :snake: **Python** - backend application server language of choice
* :whale: **Docker** - for containerizing our backend application

As we're using Docker, our backend is completely portable! Just make sure to have Docker and Docker-Compose installed and run `docker-compose up`!

## API Routes

* POST _/signup_
  * Request Body: `{username:string, password:string}` 
  * Response: `{status:int, message:"success"|"failure"}`
* POST _/login_
  * Request Body: `{username:string, password:string}`
  * Response: `{jwt_token:string}`

* GET _/user/me/account_
  * Request Header: User's JWT Token
  * Response: 
  ```
  {
      username: string, 
      hp: int, 
      xp: int, 
      inventory: [{
        id: int, quantity: int, 
        name: string, description: string 
      }]
  }
  ``` 
* POST _/user/me/account_
  * Request Header: User's JWT Token
  * Request Body 
  ```
  {
      username: string, 
      hp: int, 
      xp: int, 
      inventory: [{
        id: int, quantity: int
      }]
  }
  ```

* POST _/maprender_
  * Request Header: User's JWT Token 
  * Request Body:
  ```
  {
      x:int, 
      y:int, 
      {
        latitude: float, 
        longitude:float
      }
  }
  ```
  * Response: 
  ```
  {
     image_url: string, 
     weather: "sunny"|"rainy"|"cloudy", 
     render_objects:[
        {
         type: "player"|"ai"|"marker"|"item", 
         description: string, 
         latitude: float,
         longitude: float,
         ...
        }
      ]
  }
  ```
    
* GET _/items_
  * Response: items_schema as JSON
* GET _/experiences_
  * Response: experiences_schema as JSON
 
## Database Schema
The schema of the data, as represented in **Postgres**
* **classes** - id:int, name:varchar, description:text
* **items** - id:int, name:varchar, description:text
* **ais** - id:int, name:varchar, description:text
* **experiences** - id:int, name:varchar, description:text, xp:int
* **users** - id:int, username:varchar, password:varchar, class_id:int, created_at:timestamp, xp:int, hp:int 
* **users_items** - user_id:int, item_id:int, quantity:int
* **users_experiences** - user_id:int, experience_id:string
