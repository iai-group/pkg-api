import json
from pprint import pprint

import requests

prompt = """
Using add_owner_fact, add_fact, set_preference, and set_owner_preference, add the following facts to the KG:

I prefer action movies. --> add_owner_fact("prefer", "action movies")
I grew up watching Marvel movies. --> add_owner_fact("grew up watching", "Marvel movies")
I have seen every film starring Meryl Streep. --> add_owner_fact("seen", "every film starring Meryl Streep")
My sister's favorite actor is Tom Hanks. --> add_fact("my sister", "favorite actor", "Tom Hanks")
Emily loves romantic comedies. --> add_fact("Emily", "loves", "romantic comedies")
John and Mary often go to horror movie premieres. --> add_fact("John and Mary", "go to", "horror movie premieres")
My brother admires Christopher Nolan's work. --> add_fact("My brother", "admires", "Christopher Nolan's work")
Lisa and her friends regularly attend film festivals. --> add_fact("Lisa and her friends", "attend", "film festivals")
Alex dislikes superhero movies. --> add_fact("Alex", "dislikes", "superhero movies")
My dad often watches thrillers. --> add_fact("My dad", "watches", "thrillers")
My family enjoys animated films. --> add_fact("My family", "enjoys", "animated films")
Rachel really enjoys documentaries. --> set_preference("Rachel", "documentaries", 1)
Kevin has a strong preference for indie films. --> set_preference("Kevin", "indie films", 1)
Olivia loves classic Hollywood cinema. --> set_preference("Olivia", "classic Hollywood cinema", 1)
Mike isn't a fan of musicals. --> set_preference("Mike", "musicals", -1)
Anna dislikes black and white movies. --> set_preference("Anna", "black and white movies", -1)
I have a special liking for Pixar movies. --> set_owner_preference("Pixar movies", 1)
I am a big fan of Steven Spielberg's movies. --> set_owner_preference("Steven Spielberg's movies", 1)
I always enjoy watching films with Morgan Freeman. --> set_owner_preference("films with Morgan Freeman", 1)
I can't stand slasher films. --> set_owner_preference("slasher films", -1)
I have never enjoyed silent films. --> set_owner_preference("silent films", -1)
"""


while True:
    query = input("Enter a sentence: ") + " --> "
    # query = "My friend Bob owns a car --> "
    response = requests.post(
        "http://gustav1.ux.uis.no:8888/completion",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {
                "prompt": prompt + query,
                "max_tokens": 64,
                "temperature": 0.0,
                "top_p": 0.9,
                "n": 1,
                "stream": False,
                "logprobs": 10,
                "stop": ["\n"],
            }
        ),
    )

    j = json.loads(response.text)
    # pprint(j)
    # print("num input tokens:", j["generation_settings"])
    # print()
    # print("Input:", j["prompt"])
    print()
    print("Output:", j["content"])
