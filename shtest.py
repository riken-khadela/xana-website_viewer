import selenium, datetime

# Append-adds at last
print('fffffffff')
file1 = open("myfile.txt", "a")  # append mode
file1.write(f"Today : {datetime.datetime.now()} \n")
file1.close()