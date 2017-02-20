
def chunks(my_data, n):    
    for i in range(0, len(my_data), n):
        yield my_data[i:i+n]

