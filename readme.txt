This is Can Turgay's response to fullstack challeng#e

the application needs a Database with given "pokemon" table loaded.
here is the sql command for it:

CREATE TABLE IF NOT EXISTS public.pokemons
(
    id integer NOT NULL,
    identifier character varying(30) COLLATE pg_catalog."default" NOT NULL,
    species_id integer NOT NULL,
    height integer NOT NULL,
    weight integer NOT NULL,
    base_experience integer NOT NULL,
    "order" integer NOT NULL,
    is_default boolean,
    CONSTRAINT pokemons_pkey PRIMARY KEY (id)
)

requirements are listed in requirements.txt
required environmental variables are listed ins example.env

open new terminal
cd to the root of this folder
>> npm run start-api
open new terminal
>> npm run start-ui

browser
http://127.0.0.1:5000/


##app.py
Here is a minimal flask app as backend
- If the application is in debug mode it will just proxy front-end server. Otherwise (in production) serve the static files.

##/frontend/src/components/Pokedex.value
Here is the frontend logic.
It utilizes following libraries
- bootstrap-vue
- axios
- vuex