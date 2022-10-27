GPScode = input("Enter the Scrambled GPS code\n").split(',')
if GPScode[0] == "$GNGGA":
    Longitude = GPScode[3][:2] + " degrees " + GPScode[3][2:] + " decimal minutes"
    Latitude = GPScode[5][:3] + " degrees " + GPScode[5][3:] + " decimal minutes"
    if GPScode[4] != "N":
        Longitude = -Longitude
    if GPScode[6] != "W":
        Latitude = -Latitude
    print("The Longitude is " + Longitude + " " + GPScode[4])
    print("The Latitude is " + Latitude + " " + GPScode[6])