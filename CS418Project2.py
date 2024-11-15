import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        user='studentdba',
        password='K*hKSu%6yZ',
        host='csci-cs418-23.dhcp.bsu.edu',
        database='Airport'
    )
    return connection

def create_table(airportCursor, table):
    createAirportTable = ('CREATE TABLE Airport('
                          'Id varchar(20),'
                          'Name varchar(50),'
                          'Country varchar(100),'
                          'CityState varchar(100),'
                          'StreetAddress varchar(100),'
                          'PRIMARY KEY(Id))')
    createFlightScheduleTable = ('CREATE TABLE FlightSchedule('
                                 'FlightID int,'
                                 'DepartureAirportId varchar(20),'
                                 'DestinationAirportId varchar(20),'
                                 'DepartureTime time,'
                                 'ArrivalTime time,'
                                 'FlightDate date,'
                                 'TerminalNum int,'
                                 'MaxNumPassengers int,'
                                 'PRIMARY KEY(FlightID),'
                                 'FOREIGN KEY(DepartureAirportID) REFERENCES Airport(Id),'
                                 'FOREIGN KEY(DestinationAirportID) REFERENCES Airport(Id))')
    createPassengerTable = ('CREATE TABLE Passenger('
                            'SSN int,'
                            'Name varchar(50),'
                            'CityState varchar(100),'
                            'Address varchar(100),'
                            'Country varchar(100),'
                            'PRIMARY KEY(SSN))')
    createBookingTable = ('CREATE TABLE Booking('
                          'PassengerSSN int,'
                          'FlightID int,'
                          'Class varchar(20),'
                          'FOREIGN KEY(PassengerSSN) REFERENCES Passenger(SSN),'
                          'FOREIGN KEY(FlightID) REFERENCES FlightSchedule(FlightID))')
    
    if table == 'airport':
        table = createAirportTable
        tableName = 'Airport'
    elif table == 'flight':
        table = createFlightScheduleTable
        tableName = 'FlightSchedule'
    elif table == 'passenger':
        table = createPassengerTable
        tableName = 'Passenger'
    elif table == 'booking':
        table = createBookingTable
        tableName = 'Booking'
    else:
        print('Unable to create table')

    if checkTableExists(airportCursor, tableName) == False:
        airportCursor.execute(table)

def checkTableExists(airportCursor, tableName):
    airportCursor.execute(""" 
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tableName.replace('\'', '\'\'')))
    if airportCursor.fetchone()[0] == 1:
        return True
    else: 
        return False

def insertData(connection, airportCursor, table, data):
    if table == 'airport':
        insertStatement = ('INSERT INTO Airport (Id, Name, Country, CityState, StreetAddress) VALUES(%s, %s, %s, %s, %s)')
        existsStatement = ('SELECT EXISTS(SELECT * FROM Airport WHERE Id = %s)')
        existsData = [data[0]]
    elif table == 'flight':
        insertStatement = ('INSERT INTO FlightSchedule (FlightID, DepartureAirportID, DestinationAirportID, DepartureTime, ArrivalTime, FlightDate, TerminalNum, MaxNumPassengers) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)')
        existsStatement = ('SELECT EXISTS(SELECT * FROM FlightSchedule WHERE FlightID = %s)')
        existsData = [data[0]]
    elif table == 'passenger':
        insertStatement = ('INSERT INTO Passenger (SSN, Name, CityState, Address, Country) VALUES(%s, %s, %s, %s, %s)')
        existsStatement = ('SELECT EXISTS(SELECT * FROM Passenger WHERE SSN = %s)')
        existsData = [data[0]]
    elif table == 'booking':
        insertStatement = ('INSERT INTO Booking (PassengerSSN, FlightID, Class) VALUES(%s, %s, %s)')
        existsStatement = ('SELECT EXISTS(SELECT * FROM Booking WHERE PassengerSSN = %s AND FlightID = %s)')
        existsData = [data[0], data[1]]
    else:
        print('Unable to insert data')

    airportCursor.execute(existsStatement, existsData)
    isInTableAlready = airportCursor.fetchone()[0]
    
    if (isInTableAlready == 0):
        airportCursor.execute(insertStatement, data)
        connection.commit()
        print('Success!')

def selectData(airportCursor, table):
    if table == 'airport':
        selectStatement = ('SELECT * FROM Airport')
        attributes = ['Id', 'Name', 'Country', 'CityState', 'StreetAddress']
    elif table == 'flight':
        selectStatement = ('SELECT * FROM FlightSchedule')
        attributes = ['FlightID', 'DepartureAirportId', 'DestinationAirportId', 'ArrivalTime', 'FlightDate', 'TerminalNum', 'MaxNumPassengers', 'AirportId']
    elif table == 'passenger':
        selectStatement = ('SELECT * FROM Passenger')
        attributes = ['SSN', 'Name', 'CityState', 'Address', 'Country']
    elif table == 'booking':
        selectStatement = ('SELECT * FROM Booking')
        attributes = ['PassengerSSN', 'FlightID', 'Class']
    else:
        print('Unable to select data')

    airportCursor.execute(selectStatement)
    selectedData = airportCursor.fetchall()

    for row in selectedData:
        i = 0
        for attr in attributes:
            print(attr, ': ', row[i])
            i = i + 1
        print('------------------------------')

def deleteBookingData(connection, airportCursor, PassengerSSN, FlightID):
    deleteStatement = ('DELETE FROM Booking WHERE PassengerSSN = %s AND FlightID = %s')
    deleteData = [PassengerSSN, FlightID]

    checkBookingExists = ('SELECT EXISTS(SELECT * FROM Booking WHERE PassengerSSN = %s AND FlightID = %s)')
    airportCursor.execute(checkBookingExists, deleteData)
    isInTableAlready = airportCursor.fetchone()[0]

    if isInTableAlready == 1:
        airportCursor.execute(deleteStatement, deleteData)
        connection.commit()
        print('Booking Cancelled')
    else:
        print('This booking does not exist')    

def selectBooking(airportCursor, passengerSSN, flightID):
    selectStatement = ('SELECT * FROM Booking WHERE PassengerSSN = %s AND FlightID = %s')
    attributes = ['PassengerSSN', 'FlightID', 'Class']
    checkBookingExists = ('SELECT EXISTS(SELECT * FROM Booking WHERE PassengerSSN = %s AND FlightID = %s)')
    existsData = [passengerSSN, flightID]
    airportCursor.execute(checkBookingExists, existsData)
    isInTableAlready = airportCursor.fetchone()[0]

    if isInTableAlready == 1:
        airportCursor.execute(selectStatement, [passengerSSN, flightID])
        selectedData = airportCursor.fetchall()

        print('------------------------------\nBooking Information:')
        for row in selectedData:
            i = 0
            for attr in attributes:
                print(attr, ': ', row[i])
                i = i + 1
    else: 
        print('This Booking does not exist.')

def login(connection, airportCursor):
    passengerSSN = int(input('Please enter your ssn:'))
    existsStatement = ('SELECT EXISTS(SELECT * FROM Passenger WHERE SSN = %s)')
    airportCursor.execute(existsStatement, [passengerSSN])
    passengerExists = airportCursor.fetchone()[0]

    if passengerExists != 1:
        name = int(input('Enter your name: '))
        cityState = input('Enter your city and/or state: ')
        address = input('Enter your street address: ')
        country = input('Enter your country: ')
        passengerData = [passengerSSN, name, cityState, address, country]

        insertData(connection, airportCursor, 'passenger', passengerData)

    return passengerSSN

def insertStatements(connection, airportCursor):
    airportData1 = ['ABC', 'ABC Aiport', 'US', 'Muncie, IN', '1234 University Ave']
    insertData(connection, airportCursor, 'airport', airportData1)
    airportData2 = ['BCD', 'BCD Aiport', 'US', 'Indiapolis, IN', '1234 Neil Ave']
    insertData(connection, airportCursor, 'airport', airportData2)
    airportData3 = ['CDE', 'CDE Aiport', 'US', 'Terre Haute, IN', '1234 McKinely Ave']
    insertData(connection, airportCursor, 'airport', airportData3)
    airportData4 = ['DEF', 'DEF Aiport', 'US', 'Fort Wayne, IN', '1234 Colliseum Blvd']
    insertData(connection, airportCursor, 'airport', airportData4)

    flightData1 = [1, 'ABC', 'BCD', '01:00:00', '05:00:00', '2025-01-01', 1, 50]
    insertData(connection, airportCursor, 'flight', flightData1)
    flightData2 = [2, 'BCD', 'CDE', '02:00:00', '06:00:00', '2025-02-01', 2, 50]
    insertData(connection, airportCursor, 'flight', flightData2)
    flightData3 = [3, 'ABC', 'BCD', '01:00:00', '04:00:00', '2025-03-01', 3, 50]
    insertData(connection, airportCursor, 'flight', flightData3)
    flightData4 = [4, 'ABC', 'CDE', '04:00:00', '12:00:00', '2025-04-01', 4, 50]
    insertData(connection, airportCursor, 'flight', flightData4)

    passengerData1 = [234567890, 'Laura', 'Leo, IN', '2345 Alphabet Ln', 'United States']
    insertData(connection, airportCursor, 'passenger', passengerData1)
    passengerData2 = [345678901, 'Shane', 'Fort Wayne, IN', '5678 Alphabet Dr', 'United States']
    insertData(connection, airportCursor, 'passenger', passengerData2)
    passengerData3 = [456789012, 'Luke', 'South Bend, IN', '1357 Alphabet Rd', 'United States']
    insertData(connection, airportCursor, 'passenger', passengerData3)
    passengerData4 = [567890123, 'Owen', 'Fort Wayne, IN', '2468 Alphabet Ln', 'United States']
    insertData(connection, airportCursor, 'passenger', passengerData4)

    bookingData1 = [234567890, 1, 'First']
    insertData(connection, airportCursor, 'booking', bookingData1)
    bookingData2 = [234567890, 2, 'Economy']
    insertData(connection, airportCursor, 'booking', bookingData2)
    bookingData3 = [456789012, 1, 'Business']
    insertData(connection, airportCursor, 'booking', bookingData3)
    bookingData4 = [567890123, 4, 'First']
    insertData(connection, airportCursor, 'booking', bookingData4)

def main():
    connection = create_connection()
    airportCursor = connection.cursor()
    
    create_table(airportCursor, 'airport')
    create_table(airportCursor, 'flight')
    create_table(airportCursor, 'passenger')
    create_table(airportCursor, 'booking')
    
    insertStatements(connection, airportCursor)

    passengerSSN = login(connection, airportCursor)

    print('------------------------------\nHello! Welcome to Falcone Airlines! What would you like to do?\n')
    choice = input('1. Book\n2. View Reservation\n3. Cancel Reservation\n4. Quit\n')

    while (choice != '4' or choice == 'Quit' or choice == 'q'):
        if choice == '1' or choice == 'Book':
            print('Flight Schedule:')
            print(selectData(airportCursor, 'flight'))

            flightID = int(input('Enter the FlightID for the flight you would like to take: '))
            flightClass = input('What class would you like? (First, Economy, or Business) ')
            insertData(connection, airportCursor, 'booking', [passengerSSN, flightID, flightClass])
        
        elif choice == '2' or choice == 'View Reservation':
            flightID = int(input('Enter the FlightID of your reservation: \n'))
            selectBooking(airportCursor, passengerSSN, flightID)

        elif choice == '3' or choice == 'Cancel Reservation':
            flightID = int(input('Enter the FlightID of your reservation: \n'))
            deleteBookingData(connection, airportCursor, passengerSSN, flightID)

        else:
            print('That is not a valid option. Try again')

        choice = input('1. Book\n2. View Reservation\n3. Cancel Reservation\n4. Quit\n')

if __name__ == '__main__':
    main()