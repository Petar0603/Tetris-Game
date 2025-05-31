COLUMNS = 32
HALF_PAGES = 12
PAGES = 6
NUM_BYTES = 192
PIXEL_WIDTH = 4

def mirror(matrix):
    for column in range(COLUMNS):
        for half_page in range(PAGES):
            mirror = 11 - half_page
            temp = matrix[column][half_page]
            matrix[column][half_page] = matrix[column][mirror]
            matrix[column][mirror] = temp
    return matrix

def convert_to_nibbles(matrix):
    
    nibbles = [0x00] * (COLUMNS * HALF_PAGES)
    index = 0 
    
    for column in range(COLUMNS):
        for half_page in range(HALF_PAGES):
            if(matrix[column][half_page] == 1):
                if(half_page % 2 == 0):
                    nibbles[index] = 0x0F
                else:
                    nibbles[index] = 0xF0
            else:
                nibbles[index] = 0x00
            index += 1
    
    return nibbles
            
def combine_nibbles(nibbles):
    
    combined_nibbles = [0x00] * NUM_BYTES

    lower_nibble_index = 0
    higher_nibble_index = 1

    for index in range(NUM_BYTES):
        combined_nibbles[index] = nibbles[lower_nibble_index] + nibbles[higher_nibble_index]
        lower_nibble_index += 2
        higher_nibble_index += 2

    return combined_nibbles

def form_data(combined_nibbles):
    
    data = [0x00] * NUM_BYTES * 4

    index = 0
    internal_index = 0

    for column in range(COLUMNS):
        for repeat in range(PIXEL_WIDTH):
            internal_index = column * PAGES
            for byte_data in range(PAGES):
                data[index] = combined_nibbles[internal_index]
                index += 1
                internal_index += 1
    
    return data

def convert(matrix):
    
    mirrored_matrix = mirror(matrix)
    nibbles = convert_to_nibbles(mirrored_matrix)
    combined_nibbles = combine_nibbles(nibbles)
    data = form_data(combined_nibbles)
    
    return data