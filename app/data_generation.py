"""

Code to dynamically generate the data necessary for computation

i.e. -> lists of dictionaries for weight, elevation, distance, and work

NOTE: as a temporary solution, this uses the data from the csv files

"""

import csv



#dictionary that maps addresses to locations:
addresses_to_locations = {
    'TST BOCES, 555 Warren Road, Northeast Ithaca, NY 14850' : 'tst boces tompkins',
    'Dewitt Middle School, 560 Warren Road, Ithaca, NY 14850': '1. dewitt middle school',
    'Northeast Elementary School, 425 Winthrop Dr, Ithaca, NY 14850' : '2. northeast elementary',
    'Cayuga Heights Elementary School, 110 E Upland Rd, Ithaca, NY 14850' : '3. cayuga heights elementary',
    'Belle Sherman Elementary School, Valley Road, Ithaca, NY 14853' : '4. belle sherman',
    'Caroline Elementary School, Slaterville Road, Besemer, NY 14881' : '5. caroline elementary',
    'South Hill Elementary School, 520 Hudson Street, Ithaca, NY 14850' : '6. south hill elementary',
    'Beverly J. Martin Elementary School, 302 West Buffalo Street, Ithaca, NY' : '7. bjm elementary',
    'Fall Creek School, Linn Street, Ithaca, NY 14850' : '8. fall creek elementary',
    'Boynton Middle School, 1601 North Cayuga Street, Ithaca, NY 14850' : '9. boynton middle school',
    '602 Hancock Street, Ithaca, NY 14850' : '10. maint garage',
    '737 Willow Ave, Ithaca, NY 14850' : '11. bus garage',
    'Enfield School, 20 Enfield Main Road, Ithaca, NY 14850' : '12. enfield elementary',
    'Lehmann Alternative Community School, 111 Chestnut Street, Ithaca, NY' : '13. lehman alternative',
    'Recycling and Solid Waste Center, 160 Commercial Avenue, Ithaca, NY' : '14. tompkins recycling'
}

"""
generate the new locations to index, converting addresses to locations first

stops: a list of dictionaries each containing the address and a dict of lat/long of a each included stop

returns: a dictionary of each stop to an index
"""
def addresses_to_location_to_index(stops):
    index = 0 #index counter for the dictionary
    location_to_index = {}

    for stop in stops:
        address = stop.get('location')

        #check if the address is contained
        if (addresses_to_locations.get(address) == None):
            print(address, " is not contained.")
            #otherwise, add it to the location to index dictionary, and increment index
        else:
            location_to_index.update({addresses_to_locations.get(address) : index})
            index += 1

    return location_to_index

"""
creates a mapping of index to location

location_to_index: a dictionary of locations to indices

returns: a list where each index corresponds to its location in the input dictinoary
"""
def create_index_to_location(location_to_index):
    index_to_location_name = [None] * len(location_to_index)

    for location, index in location_to_index.items():
        index_to_location_name[index] = location

    return index_to_location_name

"""
Parses a matrix as a list of dictionaries, where each key is the column name and each value is the value at the row of the index of the list

returns: a list of dictionaries
"""
def parse_matrix(file_path):
    """
    Reads a CSV file and returns as a list of dictionaries.
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


"""
Saves list of dictionaries representing the matrix to a CSV file.
"""
def save_matrix_to_csv(matrix, output_file_name):
   
    if not matrix:
        print("Matrix is empty. Nothing to save.")
        return

    # extract field names from the first dictionary in the matrix
    fieldnames = matrix[0].keys()

    # write data to the CSV file
    with open(output_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matrix)

"""
generates a simple original route list of sequential 0... n-1 for n stops

requires n to be at least 1

stops: list of dicts of stops

returns: list of sequential 0... n-1
"""
def get_original_route(stops):
    og_route = list(range(0, len(stops)))
    og_route.append(0)
    return og_route