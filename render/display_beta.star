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
    NUM_URL = 'http://www.randomnumberapi.com/api/v1.0/random?min=0&max=' + max_entries + '&count=3'

    num_rep = http.get(NUM_URL)
    if num_rep.status_code != 200:
        fail("whoops", num_rep.status_code)

    random_number_one = str(int(num_rep.json()[0]))
    random_number_two = str(int(num_rep.json()[1]))
    random_number_three = str(int(num_rep.json()[2]))

    data_one = rep.json()['indiv_flights'][random_number_one]
    data_two = rep.json()['indiv_flights'][random_number_two]
    data_three = rep.json()['indiv_flights'][random_number_three]

    logo_one = base64.decode(logo.json()[data_one['iata_code'][0:2]])
    logo_two = base64.decode(logo.json()[data_two['iata_code'][0:2]])
    logo_three = base64.decode(logo.json()[data_three['iata_code'][0:2]])

    return render.Root(
        delay = 5000,
        child = render.Animation(
        children = [
        render.Row(
          children = [
              render.Box(width=38, height=32,
                child = render.Image(base64.decode(data_one['map']))),
                render.Box(width=26, height=32,
                child = render.Column(
                  expanded=True,
                  main_align = 'space_evenly',
                  cross_align = 'center',
                  children = [
                    render.Image(src=logo_one),
                    render.Text(data_one['dep_iata'] + data_one['arr_iata'], font = 'tom-thumb'),
                    render.Text(data_one['reg'], font = 'tom-thumb'),
                    render.Text(data_one['model'], font = 'tom-thumb')]))]),
          render.Row(
            children = [
                render.Box(width=38, height=32,
                  child = render.Image(base64.decode(data_two['map']))),
                  render.Box(width=26, height=32,
                  child = render.Column(
                    expanded=True,
                    main_align = 'space_evenly',
                    cross_align = 'center',
                    children = [
                      render.Image(src=logo_two),
                      render.Text(data_two['dep_iata'] + data_two['arr_iata'], font = 'tom-thumb'),
                      render.Text(data_two['reg'], font = 'tom-thumb'),
                      render.Text(data_two['model'], font = 'tom-thumb')]))]),
          render.Row(
              children = [
                  render.Box(width=38, height=32,
                      child = render.Image(base64.decode(data_three['map']))),
                      render.Box(width=26, height=32,
                      child = render.Column(
                        expanded=True,
                        main_align = 'space_evenly',
                        cross_align = 'center',
                        children = [
                          render.Image(src=logo_three),
                          render.Text(data_three['dep_iata'] + data_three['arr_iata'], font = 'tom-thumb'),
                          render.Text(data_three['reg'], font = 'tom-thumb'),
                          render.Text(data_three['model'], font = 'tom-thumb')]))])



        ]
        )


)
