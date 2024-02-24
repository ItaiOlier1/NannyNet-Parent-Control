import sqlite3
import hashlib


class MyDatabase:
    def __init__(self, dbname):
        # Connect to the database (or create if it doesn't exist)
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        # Create the tables if they don't exist
        self._create_parents_table()
        self._create_computers_table()
        self._create_kids_table()

    def _create_parents_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Parents (
            parentID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )''')
        self.conn.commit()

    def _create_computers_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Computers (
            mac_address TEXT PRIMARY KEY,
            computer_name TEXT,
            parentID INTEGER
        )''')
        self.conn.commit()

    def _create_kids_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kids (
                kidID INTEGER PRIMARY KEY AUTOINCREMENT,
                parentID INTEGER NOT NULL,
                username TEXT NOT NULL,
                browsingHistory TEXT DEFAULT "",
                prohibitedHours TEXT DEFAULT "",
                prohibitedURLs TEXT DEFAULT "",
                prohibitedApplications TEXT DEFAULT "",
                timeLimit TEXT DEFAULT "24:00:00",
                remainingTime TEXT DEFAULT "24:00:00",
                computerLimit BOOLEAN DEFAULT False,
                internetLimit BOOLEAN DEFAULT False,
                reachedAddresses TEXT DEFAULT "",
                FOREIGN KEY (parentID) REFERENCES parents(parentID) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def _hashing(self, string):
        """
        hash the string
        :param string: a string to hash
        :return: hashed string
        """
        # Create a SHA-256 hash object
        hash_object = hashlib.sha256()
        # Convert the password string to bytes and feed it into the hash object
        hash_object.update(string.encode('utf-8'))
        # Get the hashed password as a hex string
        hashed_str = hash_object.hexdigest()
        return hashed_str

    def checkSignUp(self, username, password):
        """
        check the user input details and if they are correct, add a new parent
        :param username: username input
        :param password: password input
        :return: boolean if the details are correct
        """
        ret = False
        # Check if the parent already exists
        if not self._isParentExist(username, password) and not username.startswith("@"):
            self._addParent(username, self._hashing(password))
            ret = True
        return ret

    def checkLogIn(self, username, password):
        """
        check the user input details and if they are correct
        :param username: username input
        :param password: password input
        :return: boolean if the details are correct
        """
        ret = False
        # Check if the parent already exists
        if self._isParentExist(username, password):
            # Insert the new parent into the table
            ret = True
        return ret

    def _addParent(self, username, password):
        """
        ad a new parent to the data base
        :param username: his username
        :param password: his password
        :return: the new parent id
        """
        # Insert the new parent into the table
        new_parentID = self._getAmountOfParents() + 1
        self.cur.execute("INSERT INTO Parents (parentID, username, password) VALUES (?, ?, ?)", (new_parentID, username, password))
        self.conn.commit()
        return new_parentID

    def _isParentExist(self, username, password):
        """
        check if the parent is already exists
        :param username: username
        :param password: password
        :return: boolean answer
        """
        self.cur.execute("SELECT COUNT(*) FROM Parents WHERE username=? and password=?", (username, self._hashing(password),))
        count = self.cur.fetchone()[0]
        return count > 0

    def _getAmountOfParents(self):
        """
        get the amount of parents to set the next parent id
        :return: amount of parents
        """
        self.cur.execute("SELECT COUNT(*) FROM Parents;")
        count = self.cur.fetchone()[0]
        return count

    def getParentIDByUsernameAndPassword(self, username, password):
        """
        get the parent id by the username nad the password
        :param username: username of a parent
        :param password:password of a parent
        :return:parent id
        """
        self.cur.execute("SELECT parentID FROM Parents WHERE username=? and password=?", (username, self._hashing(password,)))
        return self.cur.fetchone()[0]

    def addComputer(self, mac_address, computer_name, parentID):
        """
        add a new computer
        :param mac_address: parent mac address
        :param computer_name:  the computer name the parent chose
        :param parentID: the parent id
        :return: boolean if it added or not
        """
        flag = False
        # Check if the computer already exists or not
        if not self._isComputerExist(mac_address):
            print(f"typ mac: {type(mac_address)}, type computer name: {type(computer_name)}, type parentID: {type(parentID)}")
            # Insert the new computer into the table
            self.cur.execute("INSERT INTO Computers (mac_address, computer_name, parentID) VALUES (?, ?, ?)",
                             (mac_address, computer_name, parentID))
            self.conn.commit()
            flag = True
        return flag

    def _isComputerExist(self, mac_address):
        """
        check if a computer exist by a mac address
        :param mac_address: mac address
        :return: boolean
        """
        self.cur.execute("SELECT COUNT(*) FROM Computers WHERE mac_address=?", (mac_address,))
        count = self.cur.fetchone()[0]
        return count > 0

    def getAllParentComputers(self, parentID):
        """
        get all computer's mac and nickname of a parent
        :param parentID: parent id
        :return: all the parent's computers details
        """
        self.cur.execute("SELECT mac_address, computer_name FROM Computers WHERE parentID=?", (parentID,))
        return self.cur.fetchall()

    def getAllParentKidsUsername(self, parentID):
        """
        get all the username of a parent's kids
        :param parentID: the id of a parent
        :return: all the username of a parent's kids
        """
        self.cur.execute("SELECT username FROM Kids WHERE parentID=?", (parentID,))
        result = self.cur.fetchall()
        usernames = [row[0] for row in result]
        return ','.join(usernames)

    def getParentIDByMac(self, mac_address):
        """
        get the parent id by mac address
        :param mac_address: mac address of a kid's computer
        :return: parent id of None
        """
        parent_id = None
        if self._isComputerExist(mac_address):
            self.cur.execute("SELECT parentID FROM Computers WHERE mac_address=?", (mac_address,))
            parent_id = self.cur.fetchone()[0]
        return parent_id

    def addKid(self, parentID, username):
        """
        add a kid by parent id and a username
        :param parentID: the parent id
        :param username: kid's username
        :return: boolean if the server added the kid or not
        """
        ret = False
        if not self._isKidExist(parentID, username):
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO kids (parentID, username) VALUES (?, ?)', (parentID, username))
            self.conn.commit()
            ret = True
        return ret

    def _isKidExist(self, parentID, username):
        """
        check if kid exists
        :param parentID: parent id
        :param username: kid's username
        :return: if the kid exists
        """
        self.cur.execute('SELECT COUNT(*) FROM kids WHERE parentID=? and username=?', (parentID, username,))
        count = self.cur.fetchone()[0]
        print(f"count - {count}")
        return count > 0

    def _isKidExistByKidID(self, kidID):
        """
        check if kid exists
        :param kidID: the id of the kid
        :return: if the kid exists
        """
        self.cur.execute('SELECT COUNT(*) FROM kids WHERE kidID=?', (kidID,))
        count = self.cur.fetchone()[0]
        return count > 0

    def setTimeLimit(self, kidID, timeLimit):
        """
        set the time limit
        :param kidID: the id of the kid
        :param timeLimit: the new time limit
        :return: boolean
        """
        ret = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('UPDATE kids SET timeLimit=? WHERE kidID=?', (timeLimit, kidID))
            self.cur.execute('UPDATE kids SET remainingTime=? WHERE kidID=?', (timeLimit, kidID))
            self.conn.commit()
            ret = True
        return ret

    def getTimeLimit(self, kidID):
        """
        get the time limit
        :param kidID: the id of the kid
        :return:
        """
        time_limit = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT timeLimit FROM kids WHERE kidID=?', (kidID,))
            time_limit = self.cur.fetchone()[0]
        return time_limit

    def setRemainingTime(self, kidID, remainingTime):
        """
        set remaining time
        :param kidID: kid id
        :param remainingTime: new time
        :return: None
        """
        print("kid_id: " ,  kidID)
        self.cur.execute('UPDATE kids SET remainingTime=? WHERE kidID=?', (remainingTime, kidID))
        self.conn.commit()

    def getRemainingTime(self, kidID):
        """
        get remaining time
        :param kidID: kid id
        :return: remaining time
        """
        remainingTime = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT remainingTime FROM kids WHERE kidID=?', (kidID,))
            remainingTime = self.cur.fetchone()[0]
        return remainingTime

    def updateHistory(self, kidID, address):
        """
        update history list
        :param kidID: kid id
        :param address: address to add
        :return: None
        """
        max_size = 20
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT browsingHistory FROM kids WHERE kidID=?', (kidID,))
            browsing_history = self.cur.fetchone()[0]
            if browsing_history:
                browsing_history = address + ',' + browsing_history
                # check the amount of strings that in the list:
                browsing_history_list = browsing_history.split(',')
                if len(browsing_history_list) > max_size - 1:
                    # delete the last string in the list:
                    browsing_history_list = browsing_history_list[:-1]
                    browsing_history = ",".join(browsing_history_list)

            else:
                browsing_history = address
            self.cur.execute('UPDATE kids SET browsingHistory=? WHERE kidID=?', (browsing_history, kidID))
            self.conn.commit()
            print(f"\nTHE BROWSING HISTORY: {browsing_history}")

    def getHistory(self, kidID):
        """
        get the history list
        :param kidID: kid id
        :return: the history list
        """
        self.cur.execute('SELECT browsingHistory FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]

    def addProhibitedSetOfHours(self, kidID, set):
        """
        add prohibited set of hours
        :param kidID: kid id
        :param set: set of hours
        :return: True or None
        """
        ret = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedHours FROM kids WHERE kidID=?', (kidID,))
            prohibited_hours = self.cur.fetchone()[0]
            if prohibited_hours:
                prohibited_hours += ',' + set
            else:
                prohibited_hours = set
            self.cur.execute('UPDATE kids SET prohibitedHours=? WHERE kidID=?', (prohibited_hours, kidID))
            self.conn.commit()
            ret = True
        return ret

    def deleteProhibitedSetOfHours(self, kidID, set):
        """
        delete a set of prohibited hours
        :param kidID: kid id
        :param set: a set of hours to delete
        :return: None
        """
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedHours FROM kids WHERE kidID=?', (kidID,))
            prohibited_hours = self.cur.fetchone()[0]
            prohibited_hours = prohibited_hours.replace(set, '').replace(',,', ',').strip(',')
            self.cur.execute('UPDATE kids SET prohibitedHours=? WHERE kidID=?', (prohibited_hours, kidID))
            self.conn.commit()

    def getProhibitedHours(self, kidID):
        """
        get kid's prohibited hours
        :param kidID: kid id
        :return: string of  the prohibited hours
        """
        self.cur.execute('SELECT prohibitedHours FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]

    def addProhibitedURL(self, kidID, url):
        """
        add a address to the prohibited addresses list
        :param kidID: id of a kid
        :param url: an address
        :return: None or True
        """
        ret = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedURLs FROM kids WHERE kidID=?', (kidID,))
            prohibited_URLs = self.cur.fetchone()[0]
            if url not in prohibited_URLs:
                if prohibited_URLs:
                    prohibited_URLs += ',' + url
                else:
                    prohibited_URLs = url
                self.cur.execute('UPDATE kids SET prohibitedURLs=? WHERE kidID=?', (prohibited_URLs, kidID))
                self.conn.commit()
            ret = True
        return ret

    def deleteProhibitedURL(self, kidID, url):
        """
        delete and address from the prohibited addresses list
        :param kidID: id of a kid
        :param url: address to delete
        :return: None
        """
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedURLs FROM kids WHERE kidID=?', (kidID,))
            prohibitedURLs = self.cur.fetchone()[0]
            prohibitedURLs = prohibitedURLs.replace(url, '').replace(',,', ',').strip(',')
            self.cur.execute('UPDATE kids SET prohibitedURLs=? WHERE kidID=?', (prohibitedURLs, kidID))
            self.conn.commit()

    def isAddressIsProhibited(self, kidID, address):
        """
        check if an address is prohibited or not
        :param kidID: kid id
        :param address: address
        :return: True or False
        """
        flag = False
        # Execute the query to check if the address is in the table
        prohibited_addresses = self.getProhibitedURLs(kidID)

        if address in prohibited_addresses:
            flag = True

        return flag

    def getReachedAddresses(self, kidID):
        """
        get all the prohibited addresses the kid searched
        :param kidID: kid id
        :return: all the prohibited addresses the kid searched
        """
        self.cur.execute('SELECT reachedAddresses FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]

    def addReachedAddress(self, kidID, address):
        """
        add an address
        :param kidID: the id of a kid
        :param address: hte address to add
        :return: True or None
        """
        ret = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT reachedAddresses FROM kids WHERE kidID=?', (kidID,))
            reachedAddresses = self.cur.fetchone()[0]
            if address not in reachedAddresses:
                if reachedAddresses:
                    reachedAddresses += ',' + address
                else:
                    reachedAddresses = address
                self.cur.execute('UPDATE kids SET reachedAddresses=? WHERE kidID=?', (reachedAddresses, kidID))
                self.conn.commit()
            ret = True
        return ret

    def deleteAllReachedAddress(self, kidID):
        """
        delete all reached address of a kid
        :param kidID: id of a kid
        :return: None
        """
        if self._isKidExistByKidID(kidID):
            self.cur.execute('UPDATE kids SET reachedAddresses=? WHERE kidID=?', ('', kidID))
            self.conn.commit()




    def getProhibitedURLs(self, kidID):
        """
        get all prohibited addresses of a kid
        :param kidID: id of a kid
        :return: all prohibited addresses of a kid
        """
        self.cur.execute('SELECT prohibitedURLs FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]



    def addProhibitedApplication(self, kidID, app):
        """
        add an address to the list of prohibited applications
        :param kidID: id of a kid
        :param app: application
        :return: True or None
        """
        ret = None
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedApplications FROM kids WHERE kidID=?', (kidID,))
            prohibitedApps = self.cur.fetchone()[0]
            if app not in prohibitedApps:
                if prohibitedApps:
                    prohibitedApps += ',' + app
                else:
                    prohibitedApps = app
                self.cur.execute('UPDATE kids SET prohibitedApplications=? WHERE kidID=?', (prohibitedApps, kidID))
                self.conn.commit()
            ret = True
        return ret

    def deleteProhibitedApplication(self, kidID, app):
        """
        delete prohibited application from the list
        :param kidID: kid id
        :param app: application to delete
        :return: None
        """
        if self._isKidExistByKidID(kidID):
            self.cur.execute('SELECT prohibitedApplications FROM kids WHERE kidID=?', (kidID,))
            prohibitedApps = self.cur.fetchone()[0]
            prohibitedApps = prohibitedApps.replace(app, '').replace(',,', ',').strip(',')
            self.cur.execute('UPDATE kids SET prohibitedApplications=? WHERE kidID=?', (prohibitedApps, kidID))
            self.conn.commit()

    def getProhibitedApplications(self, kidID):
        """
        get all prohibited applications of a kid
        :param kidID: kid id
        :return: all prohibited applications of a kid
        """
        self.cur.execute('SELECT prohibitedApplications FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]

    def _resetRemainingTime(self):
        """
        update remaining time for all the kid's
        :return: None
        """
        # Update remaining time for each kid
        self.cur.execute('SELECT kid_id, time_limit FROM kids')
        kids = self.cur.fetchall()
        for kid in kids:
            kid_id = kid[0]
            time_limit = kid[1]
            self.cur.execute('UPDATE kids SET remaining_time=? WHERE kid_id=?', (time_limit, kid_id))

    def setComputerLimit(self, kidID, limit):
        """
        set the computer limit of a kid
        :param kidID:  kid id
        :param limit: number 0/1
        :return: None
        """
        self.cur.execute('UPDATE kids SET computerLimit=? WHERE kidID=?', (limit, kidID))
        self.conn.commit()

    def getComputerLimit(self, kidID):
        """
        get computer limit of a kid
        :param kidID: id of a kid
        :return: computer limit of a kid
        """
        self.cur.execute('SELECT computerLimit FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]

    def getKidDataForActiveParentToKid(self, parentID, username):
        """
        get kid's data to send to a parent that is active to this kid (in his profile page)
        :param parentID: the id of a parent
        :param username: the username of a kid
        :return: kid's data to send to a parent that is active to this kid (in his profile page) or None
        """
        ret = None
        if self._isKidExist(parentID, username):
            self.cur.execute(
                'SELECT kidID, remainingTime, computerLimit, internetLimit, reachedAddresses  FROM kids WHERE parentID=? and username=?',
                (parentID, username))
            ret = self.cur.fetchone()
        print(f"ret {ret}")
        return ret

    def getKidCurrentLimitationsForKidComputer(self, username, parentID):
        """
         get kid's data to send to a kid's computer when it connects with the server
        :param username: kid's username
        :param parentID: parent id
        :return: kid's data to send to a kid's computer when it connects with the server
        """
        print("USERNAME - " + str(username) + "\nPARENT ID - " + str(parentID))
        self.cur.execute(
        'SELECT kidID, prohibitedURLs, prohibitedApplications, computerLimit, internetLimit FROM kids WHERE username=? AND parentID=?', (username, parentID))
        return self.cur.fetchone()

    def setInternetLimit(self, kidID, limit):
        self.cur.execute('UPDATE kids SET internetLimit=? WHERE kidID=?', (limit, kidID))
        self.conn.commit()

    def getInternetLimit(self, kidID):
        self.cur.execute('SELECT internetLimit FROM kids WHERE kidID=?', (kidID,))
        return self.cur.fetchone()[0]


if __name__ == '__main__':
    # tests
    db = MyDatabase("myDataBase")
    db.addKid(1, "meni")
    print(db._isKidExist(1, "meni"))
    # print(db._getAmountOfParents())
    # #print(f"isParentExistByID - {db._isParentExistByID(1)}")
    # #db.checkSignUp("tal", "1234")
    # db.addComputer("64-00-6A-42-4B-C8", "itai computer", 1)
    # db.addComputer("64-00-8C-42-5C-C8", "ori computer", 1)
    # print(db.getAllParentComputers(1))
    # print(db.getParentIDByMac("64-00-6A-42-4B-C8"))
    # db.addKid(1, "itai")
    # print(f"KID: {db.getKid(1)}")
    # db.setTimeLimit(1, 5)
    # print(db.getTimeLimit(1))
    # # db.setTimeUsed(1, 4)
    # print(f"Time Used: {db.getTimeUsed(1)}")
    # db.updateHistory(1, "micmac.com")
    # # db.updateHistory(1, "aaa.com")
    # print(db.getHistory(1))
    # db.addProhibitedSetOfHours(1, "18:00-20:00")
    # db.addProhibitedSetOfHours(1, "14:00-15:00")
    # db.deleteProhibitedSetOfHours(1, "14:00-15:00")
    # db.addProhibitedSetOfHours(1, "18:00-20:00")
    # print(db.getProhibitedHours(1))
    # db.addProhibitedApplication(1, "facebook")
    # db.addProhibitedApplication(1, "booking")
    # #db.deleteProhibitedApplication(1, "booking")
    # print(db.getProhibitedApplications(1))
    # db._resetTimeUsed()
    # print(db.getKidCurrentDataForKidComputer("itai", 1))
    # print("\n" + str(db.getKidCurrentLimitationsForKidComputer('itai', 1)))









