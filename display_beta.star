load("render.star", "render")
load("http.star", "http")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")

JSON_URL = 'http://www.planerange.me/resources/current_locations.json'
LOGOS_URL = 'http://tid-resources.000webhostapp.com/resources/logos.json'

def main():

    rep = http.get(JSON_URL)
    logo = http.get(LOGOS_URL)
    if rep.status_code != 200:
        fail("whoops", rep.status_code)

    max_entries = rep.json()['max_entry']
    NUM_URL = 'http://www.randomnumberapi.com/api/v1.0/random?min=0&max=' + max_entries + '&count=1'

    num_rep = http.get(NUM_URL)
    if num_rep.status_code != 200:
        fail("whoops", num_rep.status_code)

    random_number = str(int(num_rep.json()[0]))

    data = rep.json()['indiv_flights'][random_number]

    logo = base64.decode(logo.json()[data['iata_code'][0:2]])

    return render.Root(
        delay = 500,
        child = render.Row(
          children = [
              render.Box(width=38, height=32,
                child = render.Image(base64.decode(data['map']))),
                render.Box(width=26, height=32,
                child = render.Column(
                  expanded=True,
                  main_align = 'space_evenly',
                  cross_align = 'center',
                  children = [
                    render.Image(src=logo),
                    render.Text(data['dep_iata'] + data['arr_iata'], font = 'tom-thumb'),
                    render.Text(data['reg'], font = 'tom-thumb'),
                    render.Text(data['model'], font = 'tom-thumb'),


                  ]

                ))



          ]
      )
)
