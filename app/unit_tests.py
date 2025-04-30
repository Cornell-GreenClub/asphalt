import data_generation as data_generation
import ithaca_model as ithaca_model

sample_input = [
        {'location': 'TST BOCES, 555 Warren Road, Northeast Ithaca, NY 14850', 'coords': {'lat': 42.4808, 'lng': -76.457}},
        {'location': 'Dewitt Middle School, 560 Warren Road, Ithaca, NY 14850', 'coords': {'lat': 42.4803, 'lng': -76.4566}},
        {'location': 'Northeast Elementary School, 425 Winthrop Dr, Ithaca, NY 14850', 'coords': {'lat': 42.4775, 'lng': -76.4647}}, 
        {'location': 'Cayuga Heights Elementary School, 110 E Upland Rd, Ithaca, NY 14850', 'coords': {'lat': 42.4697, 'lng': -76.4791}}, 
        {'location': 'Belle Sherman Elementary School, Valley Road, Ithaca, NY 14853', 'coords': {'lat': 42.4478, 'lng': -76.4766}}, 
        {'location': 'Caroline Elementary School, Slaterville Road, Besemer, NY 14881', 'coords': {'lat': 42.3839, 'lng': -76.4165}}, 
        {'location': 'South Hill Elementary School, 520 Hudson Street, Ithaca, NY 14850', 'coords': {'lat': 42.4336, 'lng': -76.495}}, 
        {'location': 'Beverly J. Martin Elementary School, 302 West Buffalo Street, Ithaca, NY', 'coords': {'lat': 42.4422, 'lng': -76.4976}}, 
        {'location': 'Fall Creek School, Linn Street, Ithaca, NY 14850', 'coords': {'lat': 42.4527, 'lng': -76.4869}}, 
        {'location': 'Boynton Middle School, 1601 North Cayuga Street, Ithaca, NY 14850', 'coords': {'lat': 42.4624, 'lng': -76.4921}}, 
        {'location': '602 Hancock Street, Ithaca, NY 14850', 'coords': {'lat': 42.4445, 'lng': -76.5097}}, 
        {'location': '737 Willow Ave, Ithaca, NY 14850', 'coords': {'lat': 42.4533, 'lng': -76.5054}}, 
        {'location': 'Enfield School, 20 Enfield Main Road, Ithaca, NY 14850', 'coords': {'lat': 42.4436, 'lng': -76.5491}}, 
        {'location': 'Lehmann Alternative Community School, 111 Chestnut Street, Ithaca, NY', 'coords': {'lat': 42.4506, 'lng': -76.515}}, 
        {'location': 'Recycling and Solid Waste Center, 160 Commercial Avenue, Ithaca, NY', 'coords': {'lat': 42.4461, 'lng': -76.5138}}
    ]



#confirm each csv is treated as a list of dicts
#print(revised_model.parse_matrix("weight_matrix.csv")[ :3])

print(data_generation.addresses_to_location_to_index(sample_input))

print(data_generation.get_original_route(sample_input))


print(ithaca_model.find_solution(sample_input))
