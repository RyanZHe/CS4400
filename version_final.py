from tkinter import *
import pymysql
import re
from tkinter import messagebox

# initiate check buttons from a list, vertical layout
class CheckBar(Frame):
    def __init__(self, parent=None, choices = [], side = TOP, anchor = W):
        Frame.__init__(self, parent)
        self.vars = []
        self.choices = choices
        for choice in choices:
            var = IntVar()
            check = Checkbutton(self, text = choice, variable = var)
            check.pack(side = side, anchor = anchor, expand = 1)
            self.vars.append(var)

    def checked(self):
        checkedList = list(map((lambda selected : selected.get()), self.vars))
        result = []
        i = 0
        for element in checkedList:
            if element == 1:
                result.append(self.choices[i])
            i = i + 1
        return result

    def clear(self):
        for var in self.vars:
            var.set(0)

# main class
class version2():

###################################################### Login & Register

    def __init__(self, root):

        ### Login Page
        self.loginWin = root
        self.loginWin.title("Login")

        f = Frame(self.loginWin)
        Label(f, text = "Sign In", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.loginWin)
        Label(f, text = "Username").grid(row = 0, column = 0)
        Label(f, text = "Password").grid(row = 1, column = 0)
        self.sLoginUser = StringVar()
        Entry(f, textvariable = self.sLoginUser).grid(row = 0, column = 1)
        self.sLoginPass = StringVar()
        Entry(f, textvariable = self.sLoginPass).grid(row = 1, column = 1)
        f.pack()

        f = Frame(self.loginWin)
        Button(f, text = "Register", command = self.register).grid(row = 0, column = 0)
        Button(f, text = "Login", command = self.login).grid(row = 0, column = 1)
        f.pack()

        self.selection = IntVar()

    def register(self):
        # self.loginWin.withdraw()
        ### New User Registration Window Initiation
        self.registrationWin = Toplevel(self.loginWin)
        self.registrationWin.title("New User Registration")

        f = Frame(self.registrationWin)
        Label(f, text = "New User Registration", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.registrationWin)
        Label(f, text = "Username").grid(row = 0, column = 0)
        Label(f, text = "Password").grid(row = 1, column = 0)
        Label(f, text = "Confirm Password").grid(row = 2, column = 0)
        Label(f, text = "GT Email Address").grid(row = 3, column = 0)
        self.sRegisterUser = StringVar()
        Entry(f, textvariable = self.sRegisterUser).grid(row = 0, column = 1)
        self.sRegisterPass = StringVar()
        Entry(f, textvariable = self.sRegisterPass).grid(row = 1, column = 1)
        self.sRegisterConPass = StringVar()
        Entry(f, textvariable = self.sRegisterConPass).grid(row = 2, column = 1)
        self.sRegisterEmail = StringVar()
        Entry(f, textvariable = self.sRegisterEmail).grid(row = 3, column = 1)
        f.pack()

        f = Frame(self.registrationWin)
        Button(f, text = "Submit", command = self.checkRegistration).pack()
        f.pack()

    def checkRegistration(self):
        username = self.sRegisterUser.get()
        password = self.sRegisterPass.get()
        confirmedPassword = self.sRegisterConPass.get()
        email = self.sRegisterEmail.get()
        emailFormat = re.compile("\w*@gatech.edu")
        if password != confirmedPassword or emailFormat.match(email) == None:
            if password != confirmedPassword:
                self.sRegisterPass.set("")
                self.sRegisterConPass.set("")
                error = messagebox.showerror("Passwords Doesn't Match", "Re-enter Password")
            elif emailFormat.match(email) == None:
                self.sRegisterEmail.set("")
                error = messagebox.showerror("Email Format Error", "Enter a Valid GT Email")
        else:
            num1 = self.connect("SELECT * FROM User WHERE Username = \'%s\'" % username, "Return Execution Number")
            num2 = self.connect("SELECT * FROM User WHERE Email = \'%s\'" % email, "Return Execution Number")
            if num1 != 0 or num2 != 0:
                error = messagebox.showerror("Existed Username or Email", "Pick Another Username or Email")
            else:
                # managerEmailFormat = re.compile("\w*@gttravel.com")
                # isManager = "0"
                # if managerEmailFormat.match(email) != None:
                #     isManager = "1"
                parameter = (username, email, password, 2016, "NULL", "student")
                sql = "INSERT INTO User(Username, Email, Password, Year, Major, UserType) VALUES (\'%s\' ,\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % parameter
                self.connect(sql, "Insertion")
                message = messagebox.showinfo("Congratulations", "Registered Successfully")
                self.registrationWin.withdraw()
                self.loginWin.deiconify()

    def login(self):
        if self.sLoginUser.get() == "" or self.sLoginPass.get() == "":
            error = messagebox.showerror("Blank", "Fill in All Blanks")
        else:
            parameters = (self.sLoginUser.get(), self.sLoginPass.get())
            num = self.connect("SELECT * FROM User WHERE Username = \'%s\' AND Password = \'%s\'" % parameters, "Return Execution Number")
            if num == 0:
                error = messagebox.showerror("Invalid Credentials", "Please Register")
            else:
                sql = "SELECT * FROM User WHERE UserType = 'student' AND Username = \'%s\'" % self.sLoginUser.get()
                isAdmin = self.connect(sql, "Return Execution Number")
                self.user = self.sLoginUser.get()
                self.sLoginUser.set("")
                self.sLoginPass.set("")
                message = messagebox.showinfo("Congratulations", "Login Successfully")

                # self.loginWin.withdraw()
                if isAdmin != 0:
                    self.operation()
                else:
                    self.chooseFunctionality()

###################################################### Select Operaions

    def operation(self):
        ### Select Operation Window Initiation
        self.selectWin = Toplevel(self.loginWin)
        self.selectWin.title("Main Page")

        f = Frame(self.selectWin)
        Label(f, text = "Main Page", font=("Helvetica", 20)).pack()
        Button(f, text = "Me", command = self.countrySearch).pack()
        Button(f, text = "View Project", command = self.citySearch).pack()
        Button(f, text = "Project Search", command = self.locationSearch).pack()
        Button(f, text = "Project Filter", command = self.eventSearch).pack()
        # Button(f, text = "See Past Reviews", command = self.seePreviousReview).pack()
        f.pack()

###################################################### Admin Functionalities

    def chooseFunctionality(self):
        self.chooseFuncWin = Toplevel(self.loginWin)
        self.chooseFuncWin.title("Choose Functionality")

        f = Frame(self.chooseFuncWin)
        Label(f, text = "Choose Functionality", font=("Helvetica", 20)).pack()
        Button(f, text = "View Applications", command = self.viewApplications).pack()
        Button(f, text = "View popular project report", command = self.viewPopularProjectReport).pack()
        Button(f, text = "View Application report", command = self.viewApplicationReport).pack()
        Button(f, text = "Add a Project", command = self.addProject).pack()
        Button(f, text = "Add a Course", command = self.addCourse).pack()
        f.pack()

    def viewApplications(self):
        self.viewAppsWin = Toplevel(self.loginWin)
        self.viewAppsWin.title("View Applications")

    def viewPopularProjectReport(self):
        self.viewPopRptWin = Toplevel(self.loginWin)
        self.viewPopRptWin.title("View popular project report")

    def viewApplicationReport(self):
        self.viewAppRptWin = Toplevel(self.loginWin)
        self.viewAppRptWin.title("View Application report")

    def addProject(self):
        self.addProjectWin = Toplevel(self.loginWin)
        self.addProjectWin.title("Add a Project")

    def addCourse(self):
        self.addCourseWin = Toplevel(self.loginWin)
        self.addCourseWin.title("Add a Course")


######################################################

    def countrySearch(self):

        ### Country Search Window Initiation
        self.countrySearchWin = Toplevel(self.loginWin)
        self.countrySearchWin.title("Country Search")

        f = Frame(self.countrySearchWin)
        Label(f, text = "Country Search", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.countrySearchWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        Label(f, text = "Population").grid(row = 1, column = 0)

        #dropdowm menu displaying country names
        OPTIONS = self.connect("SELECT CountryName FROM Country", "Return Single Item")
        self.dCountry = StringVar()
        dropdown = OptionMenu(f, self.dCountry, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 0, column = 1)

        self.sCountrySearchPopulation1 = StringVar()
        Entry(f, textvariable = self.sCountrySearchPopulation1).grid(row = 1, column = 1)
        Label(f, text = " TO ").grid(row = 1, column = 2)
        self.sCountrySearchPopulation2 = StringVar()
        Entry(f, textvariable = self.sCountrySearchPopulation2).grid(row = 1, column = 3)

        # display languages
        Label(f, text = "Language").grid(row = 2, column = 0)
        languages = self.connect("SELECT * FROM LANGUAGE", "Return Single Item")
        self.displayLanguage = CheckBar(f, languages)
        self.displayLanguage.grid(row = 2, column = 1)
        f.pack()

        f = Frame(self.countrySearchWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.countrySearchWin, self.selectWin)).grid(row = 0, column = 0)
        Button(f, text = "Search", command = self.searchCountry).grid(row = 0, column = 1)
        f.pack()

    def searchCountry(self):

        selectedLanguages = self.displayLanguage.checked()
        selectedCountry = self.dCountry.get()
        selectedPopulation1 = self.sCountrySearchPopulation1.get()
        selectedPopulation2 = self.sCountrySearchPopulation2.get()
        countryList = []

        sql = "SELECT CountryName, CityName, CountryPopulation, CountryLanguage FROM (CITY NATURAL JOIN COUNTRY_LANGUAGE NATURAL JOIN COUNTRY) WHERE Is_Capital = '1' %s %s %s ORDER BY CountryName ASC"

        countryString = ""
        if selectedCountry != "":
            countryString = " AND CountryName = \'" + selectedCountry + "\'"

        populationString = ""
        try:
            if selectedPopulation1 != "" and selectedPopulation2 != "":
                i = int(selectedPopulation1)
                i = int(selectedPopulation2)
                selectedPopulation1 = "\'" + selectedPopulation1 + "\'"
                selectedPopulation2 = "\'" + selectedPopulation2 + "\'"
                populationString = " AND CountryPopulation BETWEEN %s AND %s" % (selectedPopulation1, selectedPopulation2)
            elif selectedPopulation1 == "" and selectedPopulation2 != "":
                i = int(selectedPopulation2)
                selectedPopulation2 = "\'" + selectedPopulation2 + "\'"
                populationString = " AND CountryPopulation < " + selectedPopulation2
            elif selectedPopulation2 == "" and selectedPopulation1 != "":
                i = int(selectedPopulation1)
                selectedPopulation1 = "\'" + selectedPopulation1 + "\'"
                populationString = " AND CountryPopulation > " + selectedPopulation1
        except:
            error = messagebox.showerror("Error", "Enter Valid Integers for Population")

        languageString = ""

        if len(selectedLanguages) != 0:
            languageString = " AND (CountryLanguage = \'" + selectedLanguages[0] + "\'"
            for i in range(1, len(selectedLanguages)):
                languageString = languageString + " OR CountryLanguage = \'" + selectedLanguages[i] + "\'"
            languageString = languageString + ")"

        countryList = self.connect(sql % (countryString, populationString, languageString), "Return List")
        countryList = self.processList(countryList, [1, 3])

        if len(countryList) == 1:
            self.displayACountry(countryList[0])
        else:
            self.displayCountries(countryList)

        self.dCountry.set("")
        self.displayLanguage.clear()
        self.sCountrySearchPopulation1.set("")
        self.sCountrySearchPopulation2.set("")

    def displayCountries(self, countryList):

        self.countriesWin = Toplevel(self.loginWin)
        self.countriesWin.title("Countries")

        f = Frame(self.countriesWin)
        Label(f, text = "Countries", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.countriesWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "Country", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Capital City", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Population", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Languages", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        self.displayList(f, countryList, [])
        f.pack()

        f = Frame(self.countriesWin)
        Button(f, text = "Select A Country", command = lambda : self.displayACountry(countryList[self.selection.get()])).pack(side = TOP)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.countriesWin)).pack(side = LEFT)
        f.pack(side = LEFT)

    def displayACountry(self, aCountry):
        ### Country
        self.countryWin = Toplevel(self.loginWin)
        self.countryWin.title("Country")

        f = Frame(self.countryWin)
        Label(f, text = "Country", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.countryWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        Label(f, text = aCountry[0]).grid(row = 0, column = 1)
        Label(f, text = "Capital City").grid(row = 0, column = 2)
        Label(f, text = aCountry[1]).grid(row = 0, column = 3)
        Label(f, text = "Population").grid(row = 1, column = 0)
        Label(f, text = aCountry[2]).grid(row = 1, column = 1)
        Label(f, text = "Languages").grid(row = 1, column = 2)
        Label(f, text = aCountry[3]).grid(row = 1, column = 3)
        Label(f, text = "Cities").grid(row = 2, column = 0, columnspan = 4)
        f.pack()

        f = Frame(self.countryWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "City", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Population", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Languages", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Avg.Score", font = ("Times", 15, "bold")).grid(row = 0, column = 4)

        countryname = "\'" + aCountry[0] + "\'"
        sql = "SELECT CityName, CityPopulation, CityLanguage, AVG(Score) FROM ((CITY NATURAL JOIN CITY_LANGUAGE) LEFT OUTER JOIN REVIEW ON CITY.ReviewableID = REVIEW.ReviewableID) WHERE CountryName = %s GROUP BY CityName, CityPopulation, CityLanguage" % countryname
        cityList = self.connect(sql, "Return List", [3])

        cityList = self.processList(cityList, [2])
        self.displayList(f, cityList, [])
        f.pack()

        f = Frame(self.countryWin)
        Button(f, text = "Select City", command = lambda: self.displayACity(cityList[self.selection.get()][0])).pack(side = TOP)
        Button(f, text = "Go Back", command = lambda: self.returnTo(self.countryWin)).pack(side = LEFT)
        f.pack(side = LEFT)

###################################################### City Search, Display Cities, Display A City

    def citySearch(self):


        # City Search Window Initiation
        self.citySearchWin = Toplevel(self.loginWin)
        self.citySearchWin.title("City Search")

        f = Frame(self.citySearchWin)
        Label(f, text = "City Search", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.citySearchWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        # dropdown menu displaying city names
        OPTIONS = self.connect("SELECT DISTINCT CityName FROM CITY", "Return Single Item")
        self.dCity = StringVar()
        dropdown = OptionMenu(f, self.dCity, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 0, column = 1)

        Label(f, text = "Country").grid(row = 1, column = 0)
        # dropdown menu displaying country names
        OPTIONS = self.connect("SELECT CountryName FROM Country", "Return Single Item")
        self.dCountryCity = StringVar()
        dropdown = OptionMenu(f, self.dCountryCity, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 1, column = 1)

        Label(f, text = "Population").grid(row = 2, column = 0)
        self.sCitySearchPopulation1 = StringVar()
        Entry(f, textvariable = self.sCitySearchPopulation1).grid(row = 2, column = 1)
        Label(f, text = "to").grid(row = 2, column = 2)
        self.sCitySearchPopulation2 = StringVar()
        Entry(f, textvariable = self.sCitySearchPopulation2).grid(row = 2, column = 3)


        Label(f, text = "Language").grid(row = 3, column = 0)
        # language display
        languages = self.connect("SELECT * FROM LANGUAGE", "Return Single Item")
        self.displayLanguage = CheckBar(f, languages)
        self.displayLanguage.grid(row = 3, column = 1)

        Label(f, text = "Highest Rated?").grid(row = 4, column = 0)
        self.displayHighestRated = IntVar()
        self.displayHighestRated.set(0)
        Radiobutton(f, text = "YES", variable = self.displayHighestRated, value = 1).grid(row = 4, column = 1)
        Radiobutton(f, text = "NO", variable = self.displayHighestRated, value = 0).grid(row = 4, column = 2)
        f.pack()

        f = Frame(self.citySearchWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.citySearchWin, self.selectWin)).pack(side = LEFT)
        Button(f, text = "Search", command = self.searchCity).pack(side = RIGHT)
        f.pack()

    def searchCity(self):
        selectedLanguages = self.displayLanguage.checked()
        selectedCity = self.dCity.get()
        selectedCountry = self.dCountryCity.get()
        selectedPopulation1 = self.sCitySearchPopulation1.get()
        selectedPopulation2 = self.sCitySearchPopulation2.get()
        displayHighest = self.displayHighestRated.get()

        citySQL = ""
        if displayHighest == 0:
            citySQL = "SELECT CityName, CountryName, CityPopulation, CityLanguage, AVG(Score) FROM ((CITY NATURAL JOIN CITY_LANGUAGE) LEFT OUTER JOIN REVIEW ON CITY.ReviewableID = REVIEW.ReviewableID) %s GROUP BY CityName, CountryName, CityPopulation, CityLanguage ORDER BY CityName ASC"
        else:
            citySQL = "SELECT CityName, CountryName, CityPopulation, CityLanguage, AVG(Score) FROM CITY NATURAL LEFT JOIN CITY_LANGUAGE NATURAL LEFT JOIN REVIEW GROUP BY CityName, CityLanguage, CountryName, CityPopulation HAVING ROUND (AVG(Score), 4) = (SELECT ROUND (MAX(s.AScore), 4)FROM (SELECT CityName, CountryName, CityPopulation, CityLanguage, AVG(Score) AS AScore FROM (CITY NATURAL JOIN REVIEW NATURAL JOIN CITY_LANGUAGE) %s GROUP BY CityName, CountryName, CityPopulation, CityLanguage) AS s)"

        string = ""

        if selectedCity == "" and selectedCountry == "" and selectedPopulation1 == "" and selectedPopulation2 == "" and len(selectedLanguages) == 0:
            string = ""
        else:
            string = " WHERE"

        i = 0
        if selectedCountry != "":
            if i != 0:
                string = string + " AND"
            string = string + " CountryName = \'" + selectedCountry + "\'"
            i = i + 1

        if selectedCity != "":
            if i != 0:
                string = string + " AND"
            string = string + " CityName = \'" + selectedCity + "\'"
            i = i + 1

        try:
            if i != 0 and selectedPopulation1 != "" and selectedPopulation2 != "":
                string = string + " AND"
            if selectedPopulation1 != "" and selectedPopulation2 != "":
                i = int(selectedPopulation1)
                i = int(selectedPopulation2)
                selectedPopulation1 = "\'" + selectedPopulation1 + "\'"
                selectedPopulation2 = "\'" + selectedPopulation2 + "\'"
                string = string + " CityPopulation BETWEEN %s AND %s" % (selectedPopulation1, selectedPopulation2)
                i = i + 1
            elif selectedPopulation1 == "" and selectedPopulation2 != "":
                i = int(selectedPopulation2)
                selectedPopulation2 = "\'" + selectedPopulation2 + "\'"
                string = string + " CityPopulation < " + selectedPopulation2
                i = i + 1
            elif selectedPopulation2 == "" and selectedPopulation1 != "":
                i = int(selectedPopulation1)
                selectedPopulation1 = "\'" + selectedPopulation1 + "\'"
                string = string + " CityPopulation > " + selectedPopulation1
                i = i + 1
        except:
            error = messagebox.showerror("Error", "Enter Valid Integers for Population")

        if len(selectedLanguages) != 0:
            if i != 0:
                string = string + " AND"
            string = string + " (CityLanguage = \'" + selectedLanguages[0] + "\'"
            for i in range(1, len(selectedLanguages)):
                string = string + " OR CityLanguage = \'" + selectedLanguages[i] + "\'"
            string = string + ")"

        cityList = self.connect(citySQL % string, "Return List")
        cityList = self.processList(cityList, [3])

        cityList = self.connect(citySQL % string, "Return List")
        cityList = self.processList(cityList, [3])

        if len(cityList) == 1:
            self.displayACity(cityList[0][0])
        else:
            self.displayCities(cityList)

        self.displayLanguage.clear()
        self.dCity.set("")
        self.dCountryCity.set("")
        self.sCitySearchPopulation1.set("")
        self.sCitySearchPopulation2.set("")
        self.displayHighestRated.set(0)

    def displayCities(self, cityList):
        # Initiation of Cities Window
        self.citiesWin = Toplevel(self.loginWin)
        self.citiesWin.title("Cities")

        f = Frame(self.citiesWin)
        Label(f, text = "Cities", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.citiesWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "City Name", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Country", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Population", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Languages", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        Label(f, text = "Average Score", font = ("Times", 15, "bold")).grid(row = 0, column = 5)

        self.displayList(f, cityList, [])
        f.pack()

        f = Frame(self.citiesWin)
        Button(f, text = "Select A City", command = lambda : self.displayACity(cityList[self.selection.get()][0])).pack(side = TOP)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.citiesWin)).pack(side = LEFT)
        f.pack(side = LEFT)

    def displayACity(self, cityName):
        # Initiation of City Window
        self.selection.set(1000)
        self.cityWin = Toplevel(self.loginWin)
        self.cityWin.title("City")

        f = Frame(self.cityWin)
        Label(f, text = "City", font = ("Helvetica", 20)).pack()
        f.pack()

        sql = "SELECT CityName, CountryName, Latitude, Longitude, CityPopulation, CityLanguage, CITY.ReviewableID, AVG(Score) FROM ((CITY NATURAL JOIN CITY_LANGUAGE) LEFT OUTER JOIN REVIEW ON CITY.ReviewableID = REVIEW.ReviewableID) WHERE CityName = \'%s\' GROUP BY CityName, CountryName, Latitude, Longitude, CityPopulation, CityLanguage, CITY.ReviewableID" % cityName
        cityInfo = self.connect(sql, "Return List")
        cityInfo = self.processList(cityInfo, [5])[0]

        f = Frame(self.cityWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        Label(f, text = cityInfo[0]).grid(row = 0, column = 1)
        Label(f, text = "Country").grid(row = 0, column = 2)
        Label(f, text = cityInfo[1]).grid(row = 0, column = 3)
        Label(f, text = "GPS").grid(row = 1, column = 0)
        Label(f, text = cityInfo[2] + cityInfo[3]).grid(row = 1, column = 1)
        Label(f, text = "Population").grid(row = 1, column = 2)
        Label(f, text = cityInfo[4]).grid(row = 1, column = 3)
        Label(f, text = "Languages").grid(row = 2, column = 0)
        Label(f, text = cityInfo[5]).grid(row = 2, column = 1)
        Label(f, text = "Average Review Score").grid(row = 2, column = 2)
        Label(f, text = cityInfo[7]).grid(row = 2, column = 3)
        f.pack()

        f = Frame(self.cityWin)
        Label(f, text = "Locations within").grid(row = 0, column = 0)
        f.pack()

        f = Frame(self.cityWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "Location Name", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "City", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Category", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Cost", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        Label(f, text = "Avg.Score", font = ("Times", 15, "bold")).grid(row = 0, column = 5)

        locationsInCitySQL = "SELECT LocationName, LocationAddress, CityName, CountryName, LocationCategory, LocationCost, AVG(Score) FROM (LOCATION LEFT OUTER JOIN REVIEW ON LOCATION.ReviewableID = REVIEW.ReviewableID) WHERE CityName = \'%s\' GROUP BY LocationName, CityName, LocationCategory, LocationCost, LocationAddress, CountryName" % cityName
        locationsInCity = self.connect(locationsInCitySQL, "Return List")
        self.displayList(f, locationsInCity, [1, 3])
        f.pack()

        f = Frame(self.cityWin)
        Button(f, text = "Select Location", command = lambda : self.displayALocation(locationsInCity[self.selection.get()])).pack()
        Label(f, text = "Reviews").pack()
        f.pack()

        f = Frame(self.cityWin)
        Label(f, text = "Username", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Score", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Description", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        cityReviewSQL = "SELECT Username, ReviewDate, Score, Review FROM (CITY NATURAL JOIN REVIEW) WHERE CityName = \'%s\'" % cityName
        cityReviews = self.connect(cityReviewSQL, "Return List")
        self.displayList(f, cityReviews, "Review")
        f.pack()


        f = Frame(self.cityWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.cityWin)).pack(side = LEFT)
        Button(f, text = "Write Review", command = lambda : self.writeReview(cityInfo[6])).pack(side = RIGHT)
        f.pack(side = LEFT)

###################################################### Add City

    # def addProject(self):
    #     self.addCityWin = Toplevel(self.loginWin)
    #     self.addCityWin.title("City")

    #     f = Frame(self.addCityWin)
    #     Label(f, text = "City").pack()
    #     f.pack()

    #     f = Frame(self.addCityWin)
    #     Label(f, text = "Name").grid(row = 0, column = 0)
    #     self.sAddCityName = StringVar()
    #     Entry(f, textvariable = self.sAddCityName).grid(row = 0, column = 1, columnspan = 2)

    #     Label(f, text = "Country").grid(row = 1, column = 0)
    #     # Display Country Names Dropdown Menu
    #     OPTIONS = self.connect("SELECT CountryName FROM Country", "Return Single Item")
    #     self.dCountry = StringVar()
    #     dropdown = OptionMenu(f, self.dCountry, *OPTIONS)
    #     dropdown.config(width = 15, padx = 15, pady = 5)
    #     dropdown.grid(row = 1, column = 1)

    #     Label(f, text = "Population").grid(row = 2, column = 0)
    #     self.sAddCityPopulation = StringVar()
    #     Entry(f, textvariable = self.sAddCityPopulation).grid(row = 2, column = 1, columnspan = 2)

    #     Label(f, text = "GPS").grid(row = 3, column = 0)
    #     self.sAddCityLatitude = StringVar()
    #     Entry(f, textvariable = self.sAddCityLatitude).grid(row = 3, column = 1)
    #     self.sAddCityLongitude = StringVar()
    #     Entry(f, textvariable = self.sAddCityLongitude).grid(row = 3, column = 2)

    #     Label(f, text = "Latitude(e.g. 3 24 N or 12 11 S)").grid(row = 4, column = 1)
    #     Label(f, text = "Longitude(e.g. 3 24 E or 12 23 W)").grid(row = 4, column = 2)

    #     Label(f, text = "Is Capital?").grid(row = 5, column = 0)
    #     self.cityIsCapital = IntVar()
    #     self.cityIsCapital.set(1)
    #     Radiobutton(f, text = "YES", variable = self.cityIsCapital, value = 1).grid(row = 5, column = 1)
    #     Radiobutton(f, text = "NO", variable = self.cityIsCapital, value = 0).grid(row = 5, column = 2)

    #     Label(f, text = "Languages").grid(row = 6, column = 0)
    #     languages = self.connect("SELECT * FROM LANGUAGE", "Return Single Item")
    #     self.displayLanguage = CheckBar(f, languages)
    #     self.displayLanguage.grid(row = 6, column = 1, columnspan = 2)

    #     f.pack()

    #     f = Frame(self.addCityWin)
    #     Button(f, text = "Go Back", command = self.addCityWin.destroy).pack(side = LEFT)
    #     Button(f, text = "Submit", command = self.addACity).pack(side = RIGHT)
    #     f.pack()

    def addACity(self):
        cityName = self.sAddCityName.get()
        countryName = self.dCountry.get()
        population = self.sAddCityPopulation.get()
        isCapital = self.cityIsCapital.get()
        latitude = self.sAddCityLatitude.get()
        longitude = self.sAddCityLongitude.get()
        languages = self.displayLanguage.checked()
        latitudeFormat = re.compile("\d{1,2}\s\d{1,2}\s(N|S)")
        longitudeFormat = re.compile("\d{1,2}\s\d{1,2}\s(E|W)")

        if cityName == "" or countryName == "" or population == "" or latitude == "" or longitude == "" or len(languages) == 0:
            error = messagebox.showerror("Error", "Fill in ALL Blanks")
        elif latitudeFormat.match(latitude) == None or longitudeFormat.match(longitude) == None:
                error = messagebox.showerror("Error", "Incorrect Format for Longitute/Latitude")
                self.sAddCityLatitude.set("")
                self.sAddCityLongitude.set("")
        else:
            num = self.connect("SELECT CityName, CountryName FROM CITY WHERE CityName = \'%s\' AND CountryName = \'%s\'" % (cityName, countryName), "Return Execution Number")
            if num != 0:
                error = messagebox.showerror("Error", "City Already Existed")
            else:
                reviewableID = self.connect("INSERT INTO REVIEWABLE(Reviewable) VALUES (\'%s\')" % cityName, "Insertion")
                reviewableID = self.connect("SELECT ReviewableID FROM REVIEWABLE WHERE Reviewable = \'%s\'" % cityName, "Return Single Item")
                added = self.connect("INSERT INTO CITY VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (cityName, countryName, population, longitude, latitude, str(isCapital), reviewableID[0]), "Insertion")
                message = messagebox.showinfo("Congratulations", "City Added")
                self.sAddCityName.set("")
                self.dCountry.set("")
                self.sAddCityPopulation.set("")
                self.cityIsCapital.set(1)
                self.sAddCityLatitude.set("")
                self.sAddCityLongitude.set("")
                self.displayLanguage.clear()

###################################################### Location Search, Display Locations, Display A Location

    def locationSearch(self):
        ## initiation of Location Window
        self.locationSearchWin = Toplevel(self.loginWin)
        self.locationSearchWin.title("Location Search")

        f = Frame(self.locationSearchWin)
        Label(f, text = "Location Search", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.locationSearchWin)

        # dropdown menu for location names
        Label(f, text = "Name").grid(row = 0, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT LocationName FROM Location", "Return Single Item")
        self.dLocation = StringVar()
        dropdown = OptionMenu(f, self.dLocation, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 0, column = 1)

        # dropdown menu for location address
        Label(f, text = "Address").grid(row = 1, column = 0)
        OPTIONS = self.connect("SELECT LocationAddress FROM Location", "Return Single Item")
        self.dLocationAddress = StringVar()
        dropdown = OptionMenu(f, self.dLocationAddress, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 1, column = 1)

        # dropdown menu for City names
        Label(f, text = "City").grid(row = 2, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT CityName FROM Location", "Return Single Item")
        self.dLocationCity = StringVar()
        dropdown = OptionMenu(f, self.dLocationCity, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 2, column = 1)

        Label(f, text = "Country").grid(row = 3, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT CountryName FROM Location", "Return Single Item")
        self.dLocationCountry = StringVar()
        dropdown = OptionMenu(f, self.dLocationCountry, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 3, column = 1)

        Label(f, text = "Cost").grid(row = 4, column = 0)
        self.sLocationSearchCost1 = StringVar()
        Entry(f, textvariable = self.sLocationSearchCost1).grid(row = 4, column = 1)
        Label(f, text = " TO ").grid(row = 4, column = 2)
        self.sLocationSearchCost2 = StringVar()
        Entry(f, textvariable = self.sLocationSearchCost2).grid(row = 4, column = 3)

        Label(f, text = "Category").grid(row = 5, column = 0)
        categories = self.connect("SELECT * FROM LOCATION_CATEGORY", "Return Single Item")
        self.displayCategory = CheckBar(f, categories)
        self.displayCategory.grid(row = 5, column = 1)

        Label(f, text = "Sort By:").grid(row = 6, column = 0)
        self.displaySortBy = IntVar()
        self.displaySortBy.set(0)
        Radiobutton(f, text = "None", variable = self.displaySortBy, value = 0).grid(row = 6, column = 1)
        Radiobutton(f, text = "Lowest Rated", variable = self.displaySortBy, value = 1).grid(row = 6, column = 2)
        Radiobutton(f, text = "Category", variable = self.displaySortBy, value = 2).grid(row = 6, column = 3)

        f.pack()

        f = Frame(self.locationSearchWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.locationSearchWin, self.selectWin)).pack(side = LEFT)
        Button(f, text = "Search", command = self.searchLocation).pack(side = RIGHT)
        f.pack()

    def searchLocation(self):
        name = self.dLocation.get()
        address = self.dLocationAddress.get()
        cityName = self.dLocationCity.get()
        countryName = self.dLocationCountry.get()
        cost1 = self.sLocationSearchCost1.get()
        cost2 = self.sLocationSearchCost2.get()
        category = self.displayCategory.checked()
        sortBy = self.displaySortBy.get()

        locationSQL = ""
        if sortBy == 0:
            locationSQL = "SELECT LocationName, LocationAddress, CityName, CountryName, LocationCategory, LocationCost, AVG(Score) FROM (LOCATION LEFT OUTER JOIN REVIEW ON LOCATION.ReviewableID = REVIEW.ReviewableID) %s GROUP BY LocationAddress, LocationName, CityName, CountryName, LocationCategory, LocationCost"
        elif sortBy == 1:
            locationSQL = "SELECT LocationName, LocationAddress, CityName, CountryName, LocationCategory, LocationCost, AVG(Score) FROM LOCATION NATURAL JOIN REVIEW %s GROUP BY LocationName, LocationAddress, CityName, CountryName, LocationCategory, LocationCost HAVING ROUND(AVG(Score), 4) = (SELECT ROUND(MIN(s.AScore),4) FROM (SELECT LocationName, CityName, CountryName, AVG(Score) AS AScore FROM (LOCATION NATURAL JOIN REVIEW) %s GROUP BY LocationName, CityName, CountryName) AS s)"
        else:
            locationSQL = "SELECT LocationName, LocationAddress, CityName, CountryName, LocationCategory, LocationCost, AVG(Score) FROM (LOCATION LEFT OUTER JOIN REVIEW ON LOCATION.ReviewableID = REVIEW.ReviewableID) %s GROUP BY LocationAddress, LocationName, CityName, CountryName, LocationCategory, LocationCost ORDER BY LocationCategory ASC"

        string = ""

        if name == "" and cityName == "" and countryName == "" and cost1 == "" and cost2 == "" and len(category) == 0:
            string = ""
        else:
            string = " WHERE"

        i = 0
        if name != "":
            if i != 0:
                string = string + " AND"
            name = "\"" + name + "\""
            string = string + " LocationName = " + name
            i = i + 1

        if address != "":
            if i != 0:
                string = string + " AND"
            address = "\"" + address + "\""
            string = string + " LocationAddress = " + address
            i = i + 1

        if cityName != "":
            if i != 0:
                string = string + " AND"
            string = string + " CityName = \'" + cityName + "\'"
            i = i + 1

        if countryName != "":
            if i != 0:
                string = string + " AND"
            string = string + " CountryName = \'" + countryName + "\'"
            i = i + 1

        try:
            if i != 0 and cost1 != "" and cost2 != "":
                string = string + " AND"
            if cost1 != "" and cost2 != "":
                j = int(cost1)
                j = int(cost2)
                cost1 = "\'" + cost1 + "\'"
                cost2 = "\'" + cost2 + "\'"
                string = string + " LocationCost BETWEEN %s AND %s" % (cost1, cost2)
                i = i + 1
            elif cost1 == "" and cost2 != "":
                j = int(cost2)
                cost2 = "\'" + cost2 + "\'"
                string = string + " LocationCost < " + cost2
                i = i + 1
            elif cost2 == "" and cost1 != "":
                j = int(cost1)
                cost1 = "\'" + cost1 + "\'"
                string = string + " LocationCost > " + cost1
                i = i + 1
        except:
            error = messagebox.showerror("Error", "Enter Valid Integers for Population")

        if len(category) != 0:
            if i != 0:
                string = string + " AND"
            string = string + " (LocationCategory = \'" + category[0] + "\'"
            for i in range(1, len(category)):
                string = string + " OR LocationCategory = \'" + category[i] + "\'"
            string = string + ")"

        if sortBy == 1:
            print(locationSQL % (string, string))
            locationList = self.connect(locationSQL % (string, string), "Return List")
        else:
            locationList = self.connect(locationSQL % string, "Return List")

        if len(locationList) == 1:
            self.displayALocation(locationList[0])
        else:
            self.displayLocations(locationList)

        self.dLocation.set("")
        self.dLocationCity.set("")
        self.dLocationCountry.set("")
        self.sLocationSearchCost1.set("")
        self.sLocationSearchCost2.set("")
        self.displayCategory.clear()
        self.dLocationAddress.set("")


    def displayALocation(self, locationList):

        #Initiation of A Location Window
        self.locationWin = Toplevel(self.loginWin)
        self.locationWin.title("Location")

        f = Frame(self.locationWin)
        Label(f, text = "Location", font = ("Helvetica", 20)).pack()
        f.pack()

        locationAddress = locationList[1]
        cityName = locationList[2]
        countryName = locationList[3]

        sql = "SELECT LocationName, LocationAddress, CityName, CountryName, LocationCost, LocationStudentDiscount, LocationCategory, LOCATION.ReviewableID, AVG(Score) FROM (LOCATION LEFT OUTER JOIN REVIEW ON LOCATION.ReviewableID = REVIEW.ReviewableID) %s GROUP BY LocationName, LocationAddress, CityName, CountryName, LocationCost, LocationStudentDiscount, LocationCategory, LOCATION.ReviewableID"
        string = "WHERE LocationAddress = \'%s\' AND CityName = \'%s\' AND CountryName = \'%s\'" % (locationAddress, cityName, countryName)
        locationInfo = self.connect(sql % string, "Return List")[0]

        f = Frame(self.locationWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        Label(f, text = locationInfo[0]).grid(row = 0, column = 1)
        Label(f, text = "Address").grid(row = 0, column = 2)
        Label(f, text = locationInfo[1]).grid(row = 0, column = 3)
        Label(f, text = "City").grid(row = 1, column = 0)
        Label(f, text = locationInfo[2]).grid(row = 1, column = 1)
        Label(f, text = "Country").grid(row = 1, column = 2)
        Label(f, text = locationInfo[3]).grid(row = 1, column = 3)
        Label(f, text = "Cost").grid(row = 2, column = 0)
        Label(f, text = locationInfo[4]).grid(row = 2, column = 1)
        Label(f, text = "Student Discount?").grid(row = 2, column = 2)
        if locationInfo[5] == "0":
            locationInfo[5] = "NO"
        elif locationInfo[5] == "1":
            locationInfo[5] = "YES"
        Label(f, text = locationInfo[5]).grid(row = 2, column = 3)
        Label(f, text = "Category").grid(row = 3, column = 0)
        Label(f, text = locationInfo[6]).grid(row = 3, column = 1)
        Label(f, text = "Average Review Score").grid(row = 3, column = 2)
        Label(f, text = locationInfo[8]).grid(row = 3, column = 3)
        f.pack()

        f = Frame(self.locationWin)
        Label(f, text = "Events").grid(row = 0, column = 0)
        f.pack()

        f = Frame(self.locationWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "Event", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "StartTime", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Category", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        Label(f, text = "Avg.Score", font = ("Times", 15, "bold")).grid(row = 0, column = 5)
        locationEventSQL = "SELECT EventName, LocationAddress, CityName, CountryName, EventDate, StartTime, EventCategory, AVG(Score) FROM (EVENT LEFT OUTER JOIN REVIEW ON EVENT.ReviewableID = REVIEW.ReviewableID) %s GROUP BY EventName, EventDate, StartTime, EventCategory, LocationAddress, CityName, CountryName"
        string = "WHERE LocationAddress = \'%s\' AND CityName = \'%s\' AND CountryName = \'%s\'" % (locationInfo[1], locationInfo[2], locationInfo[3])
        locationEvents = self.connect(locationEventSQL % string, "Return List")
        self.displayList(f, locationEvents, [1, 2, 3])
        f.pack()

        f = Frame(self.locationWin)
        Button(f, text = "Select Event", command = lambda : self.displayAnEvent(locationEvents[self.selection.get()])).pack()
        Label(f, text = "Review").pack()
        f.pack()

        f = Frame(self.locationWin)
        Label(f, text = "Username", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Score", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Description", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        locationReviewSQL = "SELECT Username, ReviewDate, Score, Review FROM (LOCATION NATURAL JOIN REVIEW) WHERE ReviewableID = \'%s\'" % locationInfo[7]
        locationReviews = self.connect(locationReviewSQL, "Return List")
        self.displayList(f, locationReviews, "Review")
        f.pack()

        f = Frame(self.locationWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.locationWin)).pack(side = LEFT)
        Button(f, text = "Write Review", command = lambda : self.writeReview(locationInfo[7])).pack(side = RIGHT)
        f.pack(side = LEFT)

    def displayLocations(self, locationList):

        ### Initiation of Locations Win
        self.locationsWin = Toplevel(self.loginWin)
        self.locationsWin.title("Locations")

        f = Frame(self.locationsWin)
        Label(f, text = "Locations", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.locationsWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "Location Name", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Location Address", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "City", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Country", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        Label(f, text = "Category", font = ("Times", 15, "bold")).grid(row = 0, column = 5)
        Label(f, text = "Cost", font = ("Times", 15, "bold")).grid(row = 0, column = 6)
        Label(f, text = "Average Score", font = ("Times", 15, "bold")).grid(row = 0, column = 7)
        self.displayList(f, locationList, [])
        f.pack()

        f = Frame(self.locationsWin)
        Button(f, text = "Select A Location", command = lambda : self.displayALocation(locationList[self.selection.get()])).pack(side = TOP)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.locationsWin)).pack(side = LEFT)
        f.pack(side = LEFT)

###################################################### Event Search, Display Event, Display An Event

    def eventSearch(self):
        ## Initiation of Event Search Window
        self.eventSearchWin = Toplevel(self.loginWin)
        self.eventSearchWin.title("Event Search")

        f = Frame(self.eventSearchWin)
        Label(f, text = "Event Search", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.eventSearchWin)

        # Dropdown for Event Name
        Label(f, text = "Name").grid(row = 0, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT EventName FROM EVENT", "Return Single Item")
        self.dEvent = StringVar()
        dropdown = OptionMenu(f, self.dEvent, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 0, column = 1)

        # Dropdown for Location Name
        Label(f, text = "Location Address").grid(row = 1, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT LocationAddress FROM EVENT", "Return Single Item")
        self.dEventLocation = StringVar()
        dropdown = OptionMenu(f, self.dEventLocation, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 1, column = 1)

        # Dropdown for City Name
        Label(f, text = "City Name").grid(row = 2, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT CityName FROM EVENT", "Return Single Item")
        self.dEventCity = StringVar()
        dropdown = OptionMenu(f, self.dEventCity, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 2, column = 1)

        # Dropdown for Country Name
        Label(f, text = "Country Name").grid(row = 3, column = 0)
        OPTIONS = self.connect("SELECT DISTINCT CountryName FROM EVENT", "Return Single Item")
        self.dEventCountry = StringVar()
        dropdown = OptionMenu(f, self.dEventCountry, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 3, column = 1)

        # Event Date
        Label(f, text = "Date").grid(row = 4, column = 0)
        self.sEventDate = StringVar()
        Entry(f, textvariable = self.sEventDate).grid(row = 4, column = 1)

        # Range for Cost
        Label(f, text = "Cost").grid(row = 5, column = 0)
        self.sEventSearchCost1 = StringVar()
        Entry(f, textvariable = self.sEventSearchCost1).grid(row = 5, column = 1)
        Label(f, text = " TO ").grid(row = 5, column = 2)
        self.sEventSearchCost2 = StringVar()
        Entry(f, textvariable = self.sEventSearchCost2).grid(row = 5, column = 3)

        # Checkbox for Categories
        Label(f, text = "Category").grid(row = 6, column = 0)
        categories = self.connect("SELECT * FROM EVENT_CATEGORY", "Return Single Item")
        self.displayEventCategory = CheckBar(f, categories)
        self.displayEventCategory.grid(row = 6, column = 1)

        ## QUERY Radio Buttons for student discounts and Events
        Label(f, text = "Sort By:").grid(row = 7, column = 0)
        self.displaySortByEvent = IntVar()
        self.displaySortByEvent.set(0)
        Radiobutton(f, text = "None", variable = self.displaySortByEvent, value = 0).grid(row = 7, column = 1)
        Radiobutton(f, text = "Highest Rated Events", variable = self.displaySortByEvent, value = 1).grid(row = 7, column = 2)

        f.pack()

        f = Frame(self.eventSearchWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.eventSearchWin, self.selectWin)).pack(side = LEFT)
        Button(f, text = "Search", command = self.searchEvent).pack(side = RIGHT)
        f.pack()

    def searchEvent(self):
        eventName = self.dEvent.get()
        eventLocation = self.dEventLocation.get()
        eventCity = self.dEventCity.get()
        eventCountry = self.dEventCountry.get()
        cost1 = self.sEventSearchCost1.get()
        cost2 = self.sEventSearchCost2.get()
        category = self.displayEventCategory.checked()
        sortEvent = self.displaySortByEvent.get()
        date = self.sEventDate.get()

        if sortEvent == 0 :
            eventSQL = "SELECT EventName, LocationAddress, CityName, CountryName, EventDate, StartTime, EventCost, EventCategory, AVG(Score) FROM (EVENT LEFT OUTER JOIN REVIEW ON EVENT.ReviewableID = REVIEW.ReviewableID) %s GROUP BY EventName, LocationAddress, CityName, CountryName, EventDate, StartTime, EventCost, EventCategory"
        else:
            eventSQL = "SELECT EventName, LocationAddress, CityName, CountryName, EventDate, StartTime, EventCost, EventCategory, AVG(Score) FROM EVENT NATURAL JOIN REVIEW %s GROUP BY EventName, LocationAddress, CityName, CountryName, EventDate, StartTime, EventCost, EventCategory HAVING ROUND(AVG(Score), 4) = (SELECT ROUND(MAX(s.AScore),4) FROM (SELECT EventName, CityName, CountryName, AVG(Score) AS AScore FROM (EVENT NATURAL LEFT JOIN REVIEW) %s GROUP BY EventName, CityName, CountryName) AS s)"

        string = ""

        if eventName == "" and eventLocation == "" and eventCity == "" and eventCountry == "" and cost1 == "" and cost2 == "" and len(category) == 0 and date == "":
            string = ""
        else:
            string = " WHERE"

        i = 0
        if eventName != "":
            if i != 0:
                string = string + " AND"
            string = string + " EventName = \'" + eventName + "\'"
            i = i + 1

        if date != "":
            if i != 0:
                string = string + " AND"
            string = string + " EventDate = \'" + date + "\'"
            i = i + 1

        if eventLocation != "":
            if i != 0:
                string = string + " AND"
            string = string + " LocationAddress = \'" + eventLocation + "\'"
            i = i + 1

        if eventCity != "":
            if i != 0:
                string = string + " AND"
            string = string + " CityName = \'" + eventCity + "\'"
            i = i + 1

        if eventCountry != "":
            if i != 0:
                string = string + " AND"
            string = string + " CountryName = \'" + eventCountry + "\'"
            i = i + 1

        try:
            if i != 0 and cost1 != "" and cost2 != "":
                string = string + " AND"
            if cost1 != "" and cost2 != "":
                j = int(cost1)
                j = int(cost2)
                cost1 = "\'" + cost1 + "\'"
                cost2 = "\'" + cost2 + "\'"
                string = string + " EventCost BETWEEN %s AND %s" % (cost1, cost2)
                i = i + 1
            elif cost1 == "" and cost2 != "":
                j = int(cost2)
                cost2 = "\'" + cost2 + "\'"
                string = string + " EventCost < " + cost2
                i = i + 1
            elif cost2 == "" and cost1 != "":
                j = int(cost1)
                cost1 = "\'" + cost1 + "\'"
                string = string + " EventCost > " + cost1
                i = i + 1
        except:
            error = messagebox.showerror("Error", "Enter Valid Integers for Population")

        if len(category) != 0:
            if i != 0:
                string = string + " AND"
            string = string + " (EventCategory = \'" + category[0] + "\'"
            for i in range(1, len(category)):
                string = string + " OR EventCategory = \'" + category[i] + "\'"
            string = string + ")"

        if sortEvent == 0:
            eventList = self.connect(eventSQL % string, "Return List")
        else:
            eventList = self.connect(eventSQL % (string, string), "Return List")

        if len(eventList) == 1:
            self.displayAnEvent(eventList[0])
        else:
            self.displayEvents(eventList)

    def displayAnEvent(self, eventList):
        eventName = eventList[0]
        eventAddress = eventList[1]
        cityName = eventList[2]
        countryName = eventList[3]
        eventDate = eventList[4]
        eventStartTime = eventList[5]

        sql = "SELECT EventName, LocationAddress, CityName, CountryName, EventDate, EventCost, StartTime, EndTime, EventCategory, EventStudentDiscount, EventDescription, ReviewableID FROM EVENT %s"
        string = "WHERE EventName = \'%s\' AND LocationAddress = \'%s\' AND CityName = \'%s\' AND CountryName = \'%s\' AND EventDate = \'%s\' AND StartTime = \'%s\'" % (eventName, eventAddress, cityName, countryName, eventDate, eventStartTime)
        eventInfo = self.connect(sql % string, "Return List")[0]

        ## Initiation of An Event Window
        self.eventWin = Toplevel(self.loginWin)
        self.eventWin.title("Event")

        f = Frame(self.eventWin)
        Label(f, text = "Event", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.eventWin)
        Label(f, text = "Name").grid(row = 0, column = 0)
        Label(f, text = eventInfo[0]).grid(row = 0, column = 1)
        Label(f, text = "Address").grid(row = 0, column = 2)
        Label(f, text = eventInfo[1]).grid(row = 0, column = 3)

        Label(f, text = "City").grid(row = 1, column = 0)
        Label(f, text = eventInfo[2]).grid(row = 1, column = 1)
        Label(f, text = "Country").grid(row = 1, column = 2)
        Label(f, text = eventInfo[3]).grid(row = 1, column = 3)

        Label(f, text = "Date").grid(row = 2, column = 0)
        Label(f, text = eventInfo[4]).grid(row = 2, column = 1)
        Label(f, text = "Cost").grid(row = 2, column = 2)
        Label(f, text = eventInfo[5]).grid(row = 2, column = 3)

        Label(f, text = "Start Time").grid(row = 3, column = 0)
        Label(f, text = eventInfo[6]).grid(row = 3, column = 1)
        Label(f, text = "End Time").grid(row = 3, column = 2)
        Label(f, text = eventInfo[7]).grid(row = 3, column = 3)

        Label(f, text = "Category").grid(row = 4, column = 0)
        Label(f, text = eventInfo[8]).grid(row = 4, column = 1)
        Label(f, text = "Student Discount?").grid(row = 4, column = 2)
        Label(f, text = eventInfo[9]).grid(row = 4, column = 3)

        Label(f, text = "Description").grid(row = 5, column = 0)
        Label(f, text = eventInfo[10], wraplength=250).grid(row = 5, column = 1, columnspan = 3)

        f.pack()

        f = Frame(self.eventWin)
        Label(f, text = "Reviews").grid(row = 0, column = 0)
        f.pack()

        f = Frame(self.eventWin)
        Label(f, text = "Username", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Score", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Description", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        eventReviewSQL = "SELECT Username, ReviewDate, Score, Review FROM (EVENT NATURAL JOIN REVIEW) WHERE ReviewableID = \'%s\'" % eventInfo[11]
        eventReviews = self.connect(eventReviewSQL, "Return List")
        self.displayList(f, eventReviews, "Review")
        f.pack()

        f = Frame(self.eventWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.eventWin)).pack(side = LEFT)
        Button(f, text = "Write Review", command = lambda : self.writeReview(eventInfo[11])).pack(side = RIGHT)
        f.pack(side = LEFT)

    def displayEvents(self, eventList):

        self.eventsWin = Toplevel(self.loginWin)
        self.eventsWin.title("Events")

        f = Frame(self.eventsWin)
        Label(f, text = "Events", font = ("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.eventsWin)
        Label(f, text = "Name", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Address", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "City", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Country", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 5)
        Label(f, text = "Start Time", font = ("Times", 15, "bold")).grid(row = 0, column = 6)
        Label(f, text = "Cost", font = ("Times", 15, "bold")).grid(row = 0, column = 7)
        Label(f, text = "Category", font = ("Times", 15, "bold")).grid(row = 0, column = 8)
        Label(f, text = "Average Score", font = ("Times", 15, "bold")).grid(row = 0, column = 9)
        self.displayList(f, eventList, [])
        f.pack()

        f = Frame(self.eventsWin)
        Button(f, text = "Select An Event", command = lambda : self.displayAnEvent(eventList[self.selection.get()])).pack(side = TOP)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.eventsWin)).pack(side = LEFT)
        f.pack(side = LEFT)

###################################################### Write Review, See Review, Update Review

    def writeReview(self, reviewableID):
        ## Initiation of Write Review Window
        print(reviewableID, "****************")
        self.writeReviewWin = Toplevel(self.loginWin)
        self.writeReviewWin.title("Write a Review")

        f = Frame(self.writeReviewWin)
        Label(f, text = "Write a Review").pack()
        f.pack()

        f = Frame(self.writeReviewWin)
        Label(f, text = "Subject").grid(row = 0, column = 0)
        self.sWriteReviewSubject = StringVar()
        Entry(f, textvariable = self.sWriteReviewSubject).grid(row = 0, column = 1)
        Label(f, text = "Date").grid(row = 1, column = 0)
        self.sReviewDate = StringVar()
        Entry(f, textvariable = self.sReviewDate).grid(row = 1, column = 1)
        # display calendar
        Label(f, text = "Score").grid(row = 2, column = 0)
        self.sReviewScore = Scale(f, from_= 0, to = 9, orient= HORIZONTAL)
        self.sReviewScore.grid(row = 2, column = 1)
        Label(f, text = "Description").grid(row = 3, column = 0)
        self.tReviewDescription = Text(f, height = 5, width = 30)
        self.tReviewDescription.grid(row = 3, column = 1)
        f.pack()

        f = Frame(self.writeReviewWin)
        Button(f, text = "Go Back", command = lambda : self.returnTo(self.writeReviewWin)).pack(side = LEFT)
        Button(f, text = "Submit", command = lambda : self.review(reviewableID)).pack(side = RIGHT)
        f.pack()

    def review(self, reviewableID):
        date = self.sReviewDate.get()
        subject = self.sWriteReviewSubject.get()
        score = self.sReviewScore.get()
        description = self.tReviewDescription.get("1.0", END)

        if date == "" or subject == "" or score == "" or description == "":
            error = messagebox.showerror("Error", "Fill in All Blanks")
        else:
            sql = "SELECT * FROM REVIEW WHERE Username = \'%s\' AND ReviewableID = \'%s\' AND ReviewDate = \'%s\'" % (self.user, reviewableID, date)
            num = self.connect(sql, "Return Execution Number")
            if num > 0:
                error = messagebox.showerror("Error", "Already Reviewed")
            else:
                sql = "INSERT INTO REVIEW(Username, ReviewDate, Subject, Score, Review, ReviewableID) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (self.user, date, subject, score, description, reviewableID)
                self.connect(sql, "Insertion")
                message = messagebox.showinfo("Congratulations!", "Review Added!")
            self.sReviewDate.set("")
            self.sWriteReviewSubject.set("")
            self.tReviewDescription.delete("1.0", END)
            self.sReviewScore.set(0)

    def seePreviousReview(self):
        ### See Previous Reviews
        self.seeReviewWin = Toplevel(self.loginWin)
        self.seeReviewWin.title("Reviews")

        f = Frame(self.seeReviewWin)
        Label(f, text = "Reviews").pack()
        f.pack()

        f = Frame(self.seeReviewWin)
        Label(f, text = "Select", font = ("Times", 15, "bold")).grid(row = 0, column = 0)
        Label(f, text = "Username", font = ("Times", 15, "bold")).grid(row = 0, column = 1)
        Label(f, text = "Date", font = ("Times", 15, "bold")).grid(row = 0, column = 2)
        Label(f, text = "Score", font = ("Times", 15, "bold")).grid(row = 0, column = 3)
        Label(f, text = "Description", font = ("Times", 15, "bold")).grid(row = 0, column = 4)
        # display reviews
        userReviews = self.connect("SELECT Username, ReviewDate, Score, Review, ReviewableID FROM REVIEW WHERE Username = \'%s\'" % self.user, "Return List")
        self.displayList(f, userReviews, [4])

        f.pack()

        f = Frame(self.seeReviewWin)
        Button(f, text = "Go Back", command = lambda: self.returnTo(self.seeReviewWin)).pack(side = LEFT)
        Button(f, text = "Update", command = lambda : self.updateReview(userReviews[self.selection.get()])).pack(side = RIGHT)
        f.pack()

    def updateReview(self, reviewInfo):
        ## Initiation of Update Review Window
        print(reviewInfo)
        self.updateReviewWin = Toplevel(self.loginWin)
        self.updateReviewWin.title("Update Review")

        f = Frame(self.updateReviewWin)
        Label(f, text = "Update Review").pack()
        f.pack()

        f = Frame(self.updateReviewWin)
        Label(f, text = "Subject").grid(row = 0, column = 0)
        self.sUpdateSubject = StringVar()
        Entry(f, textvariable = self.sUpdateSubject).grid(row = 0, column = 1)
        Label(f, text = "Date").grid(row = 1, column = 0)
        self.sUpdateDate = StringVar()
        Entry(f, textvariable = self.sUpdateDate).grid(row = 1, column = 1)
        # display calendar
        Label(f, text = "Score").grid(row = 2, column = 0)
        self.sUpdateScore = Scale(f, from_= 0, to = 9, orient= HORIZONTAL)
        self.sUpdateScore.grid(row = 2, column = 1)
        Label(f, text = "Description").grid(row = 3, column = 0)
        self.tUpdateDescription = Text(f, height = 5, width = 30)
        self.tUpdateDescription.grid(row = 3, column = 1)
        f.pack()

        f = Frame(self.updateReviewWin)
        Button(f, text = "Go Back", command = lambda: self.returnTo(self.updateReviewWin)).pack(side = LEFT)
        Button(f, text = "Submit", command = lambda : self.update(reviewInfo)).pack(side = RIGHT)
        f.pack()

    def update(self, reviewInfo):
        date = self.sUpdateDate.get()
        subject = self.sUpdateSubject.get()
        score = self.sUpdateScore.get()
        description = str(self.tUpdateDescription.get("1.0", END))

        if date == "" or subject == "" or description == "" or score == "":
            error = messagebox.showerror("Error", "Fill in All Blanks")
        else:
            sql = "UPDATE REVIEW SET ReviewDate = \'%s\', Subject = \'%s\', Review = \'%s\', Score = \'%s\' WHERE Username = \'%s\' AND ReviewDate = \'%s\' AND ReviewableID = \'%s\'" % (date, subject, description, score, reviewInfo[0], reviewInfo[1], reviewInfo[4])
            self.connect(sql, "Insertion")
            message = messagebox.showinfo("Congratulations!", "Review Updated!")
            self.sUpdateDate.set("")
            self.sUpdateSubject.set("")
            self.sUpdateScore.set(0)
            self.tUpdateDescription.delete("1.0", END)
            self.seeReviewWin.destroy()
            self.seePreviousReview()

###################################################### General Methods

    ## Display a given list into a given frame, with buttons direted to specific info page (country, city, locaton, event)
    def displayList(self, frame, aList, discardColumns=None):
        newList = []
        if discardColumns != None and "Review" not in discardColumns:
            for row in aList:
                temp = []
                for columns in range(len(row)):
                    if columns not in discardColumns:
                        temp.append(row[columns])
                newList.append(temp)
            aList = newList
        if len(aList) > 0:
            rows = len(aList)
            columns = len(aList[0])
            for i in range(rows):
                if "Review" not in discardColumns:
                    Radiobutton(frame, text="", variable = self.selection, value = i).grid(row = i + 1, column = 0)
                for j in range(columns):
                    l = Label(frame, text = aList[i][j]).grid(row = i + 1, column = j + 1)
        else:
            l = Label(frame, text = "No Content in Table")
            l.grid(row = 1, column = 0, columnspan = 4)

    ## Merge duplicates, change format
    def processList(self, aList, columnsToChange):
        existed = []
        result = []
        j = 0
        for i in range(len(aList)):
            if j > 0:
                if aList[i][0] in existed:
                    for k in columnsToChange:
                        if aList[i][k] not in result[existed.index(aList[i][0])][k]:
                            result[existed.index(aList[i][0])][k] = result[existed.index(aList[i][0])][k] + " / " + aList[i][k]
                else:
                    result.append(aList[i])
                    existed.append(aList[i][0])
                    j = j + 1
            else:
                result.append(aList[i])
                existed.append(aList[i][0])
                j = j + 1

        return result

    ## Return to returnTo window while destroy window
    def returnTo(self, window, returnTo=None):
        window.destroy()
        if returnTo != None:
            returnTo.deiconify()

    def processDescription(self, description):
        returned = ""
        lines = int(len(description) / 100) + 1
        for i in range(lines):
            if i == 0:
                if lines == 1:
                    returned = description
                else:
                    returned = returned + description[0 : 100] + "\n"
            elif i == lines - 1:
                returned = returned + description[100*i+1:]
            else:
                returned = returned + description[100*i+1: 100*i+100] + "\n"
        return returned


###################################################### Connect to Database

    def connect(self, sql, commandName, parameters = None):
        db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_68", passwd = "L7zcpxeU", db = "cs4400_Team_68")
        cursor = db.cursor()
        returned = None

        try:
            if commandName == "Return Execution Number":
                returned = cursor.execute(sql)

            elif commandName == "Return Single Item":
                cursor.execute(sql)
                returned = []
                for (row) in cursor.fetchall():
                    row = re.sub("[,]", "", str(row))
                    returned.append(str(row)[1:-1][1:-1])

            elif commandName == "Return List":
                cursor.execute(sql)
                returned = []
                for row in cursor.fetchall():
                    aList = list(row)
                    temp = []
                    for element in aList:
                        if element == None:
                            element = "/"
                        else:
                            element = str(element)
                        temp.append(element)
                    returned.append(temp)

            elif commandName == "Insertion":
                print(sql)
                cursor.execute(sql)

        except Exception as e:
            print(str(e))
            error = messagebox.showerror("Error", "SQL Connection Failed")

        cursor.close()
        db.commit()
        db.close()
        return returned

window = Tk()
app = version2(window)
window.mainloop()
