load("render.star", "render")
load("http.star", "http")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")

JSON_URL = 'http://tid-resources.000webhostapp.com/resources/current_locations.json'

def main():

    rep = http.get(JSON_URL)
    if rep.status_code != 200:
        fail("whoops", rep.status_code)

    zero_im = base64.decode(rep.json()['frame_one'])
    one_im = base64.decode(rep.json()['frame_two'])
    two_im = base64.decode(rep.json()['frame_three'])

    return render.Root(
        delay = 500,
        child = render.Box(
            child = render.Animation(
                children = [
                    render.Image(src=zero_im),
                    render.Image(src=one_im),
                    render.Image(src=two_im)
                ]

            )


        )
      )
