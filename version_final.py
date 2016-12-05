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
        root.geometry('{}x{}'.format(300, 300))
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
                message = messagebox.showinfo("Congratulations", "Login Successfully")

                if isAdmin != 0:
                    self.operation()
                else:
                    self.chooseFunctionality()

###################################################### Student Functionalities

    def operation(self):
        ### Select Operation Window Initiation
        self.selectWin = Toplevel(self.loginWin)
        self.selectWin.title("Main Page")

        f = Frame(self.selectWin)
        Label(f, text = "Main Page", font=("Helvetica", 20)).pack()
        Button(f, text = "Me", command = self.mePage).pack()
        Button(f, text = "Project Serach", command = self.projectSearch).pack()
        Button(f, text = "Course Search", command = self.courseSearch).pack()
        # Button(f, text = "Project Filter", command = self.eventSearch).pack()
        # Button(f, text = "See Past Reviews", command = self.seePreviousReview).pack()
        f.pack()

    def mePage(self):
        self.mePageWin = Toplevel(self.loginWin)
        self.mePageWin.title("Me")
        f = Frame(self.mePageWin)
        Label(f, text = "Me", font=("Helvetica", 20)).pack()
        Button(f, text = "Edit Profile", command = self.editProfile).pack()
        Button(f, text = "My Application", command = self.myApplication).pack()
        f.pack()

    def editProfile(self):
        self.editProfileWin = Toplevel(self.loginWin)
        self.editProfileWin.title("My Profile")
        f = Frame(self.editProfileWin)
        Label(f, text = "Edit Profile", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.editProfileWin)
        Label(f, text = "Major", font=("Helvetica", 20)).grid(row = 0, column = 0)
        OPTIONS = self.connect("SELECT Name FROM Major", "Return Single Item")
        self.dMajor = StringVar()
        dropdown = OptionMenu(f, self.dMajor, *OPTIONS)
        dropdown.config(width = 15, padx = 15, pady = 5)
        dropdown.grid(row = 0, column = 1)
        username = self.sLoginUser.get()
        sMajor = self.connect("SELECT Major FROM User WHERE Username = \'%s\'" % username, "Return Single Item")
        self.dMajor.set(sMajor[0])
        Label(f, text = "Year", font=("Helvetica", 20)).grid(row = 1, column = 0)
        OPTIONS = ['freshman', 'sophomore', 'Junior', 'senior']
        self.dYear = StringVar()
        dropdown = OptionMenu(f, self.dYear, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 1, column = 1)
        self.dYear.set(self.connect("SELECT Year FROM User WHERE Username = \'%s\'" % username, "Return Single Item")[0])
        Label(f, text = "Department", font=("Helvetica", 20)).grid(row = 2, column = 0)
        major = self.dMajor.get()
        if major != 'NULL':
            OPTION = self.connect("SELECT Dept_Name FROM Major WHERE Name = \'%s\'" % major, "Return Single Item")
        else:
            OPTION = ['']
        Label(f, text = OPTION, font=("Helvetica", 20)).grid(row = 2, column = 1)
        f.pack()

        f = Frame(self.editProfileWin)
        Button(f, text = "Back", command = self.update).pack()
        f.pack()

    def update(self):
        sql = "UPDATE User SET Major = \'%s\', Year = \'%s\' WHERE Username = \'%s\'" % (self.dMajor.get(), self.dYear.get(), self.sLoginUser.get())
        self.connect(sql, "Insertion")
        self.returnTo(self.editProfileWin, self.mePageWin)

    def myApplication(self):
        self.myApplicationWin = Toplevel(self.loginWin)
        self.myApplicationWin.title("View My Application")

        f = Frame(self.myApplicationWin)
        Label(f, text = "My Application", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.myApplicationWin)
        Label(f, text = "Date", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = "Project Name", font=("Helvetica", 20)).grid(row = 0, column = 1)
        Label(f, text = "Status", font=("Helvetica", 20)).grid(row = 0, column = 2)
        f.pack()

        f = Frame(self.myApplicationWin)
        applicationList = self.connect("SELECT Date, Project_name, Status FROM Apply WHERE Student_name = \'%s\'" % self.sLoginUser.get(), "Return Single Item")
        for application in applicationList:
            Label(f, text = application[12:], font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.myApplicationWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.myApplicationWin, self.mePageWin)).pack()
        f.pack()

    def projectSearch(self):
        self.projectSearchWin = Toplevel(self.loginWin)
        self.projectSearchWin.title("View Project")

        f = Frame(self.projectSearchWin)
        Label(f, text = "Search Project", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.projectSearchWin)
        Label(f, text = "Title", font=("Helvetica", 20)).grid(row = 0, column = 0)
        self.sTitle = StringVar()
        Entry(f, textvariable = self.sTitle).grid(row = 0, column = 1)
        Label(f, text = "Designation", font=("Helvetica", 20)).grid(row = 1, column = 0)
        self.sDesignation = StringVar()
        OPTIONS = self.connect("SELECT Name FROM Designation", "Return Single Item")
        dropdown = OptionMenu(f, self.sDesignation, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 1, column = 1)
        Label(f, text = "Major", font=("Helvetica", 20)).grid(row = 2, column = 0)
        self.sMajor = StringVar()
        OPTIONS = self.connect("SELECT Name FROM Major", "Return Single Item")
        dropdown = OptionMenu(f, self.sMajor, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 2, column = 1)
        # Entry(f, textvariable = self.sMajor).grid(row = 2, column = 1)
        Label(f, text = "Year", font=("Helvetica", 20)).grid(row = 3, column = 0)
        self.sYear = StringVar()
        OPTIONS = ['freshman', 'sophomore', 'Junior', 'Senior']
        dropdown = OptionMenu(f, self.sYear, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 3, column = 1)
        # Entry(f, textvariable = self.sYear).grid(row = 3, column = 1)
        Label(f, text = "Category", font=("Helvetica", 20)).grid(row = 4, column = 0)
        OPTIONS = self.connect("SELECT Name FROM Category", "Return Single Item")
        self.dCategory = StringVar()
        dropdown = OptionMenu(f, self.dCategory, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 4, column = 1)
        Button(f, text = "Add a category", command = self.addCategory).grid(row = 4, column = 2)
        self.categorySet = set()
        f.pack()

        f = Frame(self.projectSearchWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.projectSearchWin, self.selectWin)).grid(row = 0, column = 0)
        Button(f, text = "Search", command = self.searchProject).grid(row = 0, column = 1)
        f.pack()

    def addCategory(self):
        self.categorySet.add(self.dCategory.get())

    def searchProject(self):
        self.searchProjectWin = Toplevel(self.loginWin)
        self.searchProjectWin.title("View Project")

        f = Frame(self.searchProjectWin)
        Label(f, text = "Project Result", font=("Helvetica", 20)).pack()
        f.pack()

        title = self.sTitle.get()
        designation = self.sDesignation.get()
        major = self.sMajor.get()
        year = self.sYear.get()
        icategorySet = self.categorySet
        numconstraints = 0
        sql = "SELECT Project.Name FROM Project LEFT OUTER JOIN Project_requirement ON Project.Name = Project_requirement.Name LEFT OUTER JOIN Project_is_category ON Project.Name = Project_is_category.Project_name"
        if title != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Project.Name LIKE '%%%s%%'" % title
        if designation != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Project.Designation = \'%s\'" % designation
        if major != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Project_requirement.Requirement LIKE '%%%s%%'" % major
        if year != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Project_requirement.Requirement LIKE '%%%s%%'" % year
        if len(icategorySet) != 0:
            for category in icategorySet:
                if numconstraints == 0:
                    sql = sql + " WHERE"
                    numconstraints = 1
                else:
                    sql = sql + " AND"
                sql = sql + " Project_is_category.Category_name = \'%s\'" % category

        f = Frame(self.searchProjectWin)
        sql = sql + " GROUP BY Project.Name"
        projectList = self.connect(sql, "Return Single Item")
        for iproject in projectList:
            Button(f, text = iproject, command = lambda iproject = iproject: self.viewProject(iproject)).pack()
        self.categorySet = set()
        f.pack()

    def viewProject(self, name):
        self.viewProjectWin = Toplevel(self.loginWin)
        self.viewProjectWin.title(name)

        f = Frame(self.viewProjectWin)
        Label(f, text = name, font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Advisor: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project WHERE Name = \'%s\'" % ("Advisor_name", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Description: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project WHERE Name = \'%s\'" % ("Description", name), "Return Single Item")[0], font=("Helvetica", 6)).grid(row = 1, column = 0)
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Designation: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project WHERE Name = \'%s\'" % ("Designation_name", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Category: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project_is_category WHERE Project_name = \'%s\'" % ("Category_name", name), "Return Single Item"), font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Requirements: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project_requirement WHERE Name = \'%s\'" % ("Requirement", name), "Return Single Item"), font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewProjectWin)
        Label(f, text = "Estimated number of students: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Project WHERE Name = \'%s\'" % ("NumStudent", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewProjectWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.viewProjectWin, self.searchProjectWin)).grid(row = 0, column = 0)
        Button(f, text = "Apply", command = lambda: self.applyProject(name)).grid(row = 0, column = 1)
        f.pack()

    def applyProject(self, name):
        major = self.dMajor.get()
        year = self.dYear.get()
        department = self.connect("SELECT Dept_Name FROM Major WHERE Name = \'%s\'" % major, "Return Single Item")[0]
        if len(self.connect("SELECT * FROM Project_requirement WHERE Type = 'Major'", "Return Single Item")) != 0:
            if len(self.connect("SELECT * FROM Project_requirement WHERE Requirement LIKE '%%%s%%' AND Type = 'Major'" % major, "Return Single Item")) == 0:
                error = messagebox.showerror("Error", "Your major does not fulfill the requirement")
                return
        if len(self.connect("SELECT * FROM Project_requirement WHERE Type = 'Year'", "Return Single Item")) != 0:
            if len(self.connect("SELECT * FROM Project_requirement WHERE Requirement LIKE '%%%s%%' AND Type = 'Year'" % year, "Return Single Item")) == 0:
                error = messagebox.showerror("Error", "Your year does not fulfill the requirement")
                return
        if len(self.connect("SELECT * FROM Project_requirement WHERE Type = 'Department'", "Return Single Item")) != 0:
            if len(self.connect("SELECT * FROM Project_requirement WHERE Requirement LIKE '%%%s%%' AND Type = 'Department'" % department, "Return Single Item")) == 0:
                error = messagebox.showerror("Error", "Your department does not fulfill the requirement")
                return
        import time
        parameter = (self.sLoginUser.get(), name, time.strftime("%Y-%m-%d"), "Pending")
        sql = "INSERT INTO Apply(Student_name, Project_name, Date, Status) VALUES (\'%s\' ,\'%s\', \'%s\', \'%s\')" % parameter
        self.connect(sql, "Insertion")

    def courseSearch(self):
        self.courseSearchWin = Toplevel(self.loginWin)
        self.courseSearchWin.title("View Course")

        f = Frame(self.courseSearchWin)
        Label(f, text = "Search Course", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.courseSearchWin)
        Label(f, text = "Title", font=("Helvetica", 20)).grid(row = 0, column = 0)
        self.sTitle = StringVar()
        Entry(f, textvariable = self.sTitle).grid(row = 0, column = 1)
        Label(f, text = "Designation", font=("Helvetica", 20)).grid(row = 1, column = 0)
        self.sDesignation = StringVar()
        OPTIONS = self.connect("SELECT Name FROM Designation", "Return Single Item")
        dropdown = OptionMenu(f, self.sDesignation, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 1, column = 1)
        # Entry(f, textvariable = self.sDesignation).grid(row = 1, column = 1)
        Label(f, text = "Category", font=("Helvetica", 20)).grid(row = 2, column = 0)
        OPTIONS = self.connect("SELECT Name FROM Category", "Return Single Item")
        self.dCategory = StringVar()
        dropdown = OptionMenu(f, self.dCategory, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 2, column = 1)
        Button(f, text = "Add a category", command = self.addCategory).grid(row = 2, column = 2)
        self.categorySet = set()
        f.pack()

        f = Frame(self.courseSearchWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.courseSearchWin, self.selectWin)).grid(row = 0, column = 0)
        Button(f, text = "Search", command = self.searchCourse).grid(row = 0, column = 1)
        f.pack()

    def searchCourse(self):
        self.searchCourseWin = Toplevel(self.loginWin)
        self.searchCourseWin.title("View Course")

        f = Frame(self.searchCourseWin)
        Label(f, text = "Course Result", font=("Helvetica", 20)).pack()
        f.pack()

        title = self.sTitle.get()
        designation = self.sDesignation.get()
        icategorySet = self.categorySet
        numconstraints = 0
        sql = "SELECT Course.Name FROM Course LEFT OUTER JOIN Course_is_category ON Course.Name = Course_is_category.Course_name"
        if title != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Course.Name LIKE '%%%s%%'" % title
        if designation != '':
            if numconstraints == 0:
                sql = sql + " WHERE"
                numconstraints = 1
            else:
                sql = sql + " AND"
            sql = sql + " Course.Designation = \'%s\'" % designation
        if len(icategorySet) != 0:
            for category in icategorySet:
                if numconstraints == 0:
                    sql = sql + " WHERE"
                    numconstraints = 1
                else:
                    sql = sql + " AND"
                sql = sql + " Course_is_category.Category_name = \'%s\'" % category

        f = Frame(self.searchCourseWin)
        sql = sql + " GROUP BY Course.Name"
        courseList = self.connect(sql, "Return Single Item")
        for icourse in courseList:
            Button(f, text = icourse, command = lambda icourse = icourse: self.viewCourse(icourse)).pack()
        self.categorySet = set()
        f.pack()

    def viewCourse(self, name):
        self.viewCourseWin = Toplevel(self.loginWin)
        self.viewCourseWin.title(name)

        f = Frame(self.viewCourseWin)

        Label(f, text = self.connect("SELECT %s FROM Course WHERE Name = \'%s\'" % ("Course_Number", name), "Return Single Item")[0], font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.viewCourseWin)
        Label(f, text = "Course Name: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = name, font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewCourseWin)
        Label(f, text = "Instructor: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Course WHERE Name = \'%s\'" % ("Instructor", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 1, column = 0)
        f.pack()

        f = Frame(self.viewCourseWin)
        Label(f, text = "Designation: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Course WHERE Name = \'%s\'" % ("Designation_name", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewCourseWin)
        Label(f, text = "Category: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Course_is_category WHERE Course_name = \'%s\'" % ("Category_name", name), "Return Single Item"), font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewCourseWin)
        Label(f, text = "Estimated number of students: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        Label(f, text = self.connect("SELECT %s FROM Course WHERE Name = \'%s\'" % ("NumStudent", name), "Return Single Item")[0], font=("Helvetica", 20)).grid(row = 0, column = 1)
        f.pack()

        f = Frame(self.viewCourseWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.viewCourseWin, self.searchCourseWin)).grid(row = 0, column = 0)
        f.pack()

###################################################### Admin Functionalities

    def chooseFunctionality(self):
        self.chooseFuncWin = Toplevel(self.loginWin)
        self.chooseFuncWin.geometry('{}x{}'.format(300, 300))
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
        self.viewAppsWin.geometry('{}x{}'.format(800, 500))
        self.viewAppsWin.title("View Applications")

        f = Frame(self.viewAppsWin)
        f.pack()
        Label(f, text = "View Applications", font=("Helvetica", 20)).pack()

        f = Frame(self.viewAppsWin)
        f.pack()
        Label(f, text = "Project", font=("Helvetica", 15)).grid(row = 0, column = 0, padx = 5, pady = 5)
        Label(f, text = "Applicant Major", font=("Helvetica", 15)).grid(row = 0, column = 1, sticky = W, padx = 10, pady = 5)
        Label(f, text = "Applicant Year", font=("Helvetica", 15)).grid(row = 0, column = 2, sticky = W, padx = 20, pady = 5)
        Label(f, text = "Status", font=("Helvetica", 15)).grid(row = 0, column = 3, sticky = W, padx = 10, pady = 5)


        numProj = self.connect("SELECT COUNT(Project_name) FROM Apply", "Return List")
        projects = self.connect("SELECT Project_name, Status, Student_name FROM Apply", "Return List")
        acceptRejectList = []

        userIdList = self.connect("SELECT Student_name FROM Apply", "Return Single Item")
        for num in range(1,int(numProj[0][0]) + 1):
            userId = userIdList[num - 1]
            appMajorYear = self.connect("SELECT Year, Major FROM User WHERE Username = \'%s\'" % userId, "Return List")
            self.projectName = projects[num - 1][0]
            self.currentStatus = projects[num - 1][1]
            self.studentName = projects[num - 1][2]
            Label(f, text = self.projectName).grid(row = num, column = 0, sticky = W)

            if self.currentStatus == 'Pending':
                self.projectName2 = projects[num - 1][0]
                self.currentStatus2 = projects[num - 1][1]
                self.studentName2 = projects[num - 1][2]
                OPTIONS = ['Accept', 'Pending', 'Reject']
                dProject = StringVar()
                dProject.set("Pending")
                dropdown = OptionMenu(f, dProject, *OPTIONS, command = self.callback)
                dropdown.config(width = 10)
                dropdown.grid(row = num, column = 3)

            else:
                Label(f, text = self.currentStatus).grid(row = num, column = 3, sticky = W)


            if appMajorYear is None :
                year = "N/A"
                major = "N/A"
            else:
                year = appMajorYear[0][1]
                major = appMajorYear[0][0]

            Label(f, text = year).grid(row = num, column = 1)
            Label(f, text = major).grid(row = num, column = 2)


        f = Frame(self.viewAppsWin)
        f.pack()
        Button(f, text = "Back", command = self.quitviewAppGotoFunc).grid(row = 0, column = 0)
        self.viewApplications

    def callback(self, value):
        if value != 'Pending':
            self.callbackWin = Toplevel(self.loginWin)
            self.callbackWin.geometry('{}x{}'.format(300, 200))
            self.callbackWin.title("Change Status")
            projectName = self.projectName2
            studentName = self.studentName2
            if value == 'Accept':
                sql = "UPDATE Apply SET Status = \'Accepted\' WHERE Project_name = \'%s\' AND Student_name = \'%s\'" % (projectName, studentName)
            elif value == 'Reject':
                sql = "UPDATE Apply SET Status = \'Rejected\' WHERE Project_name = \'%s\' AND Student_name = \'%s\'" % (projectName, studentName)

            f = Frame(self.callbackWin)
            f.pack()
            Label(f, text = "Are you sure? No changes can be done.").grid(row = 0, column = 0, columnspan = 2)
            Button(f, text = "Yes", command = lambda: self.changeStatus(sql)).grid(row = 1, column = 0)
            Button(f, text = "No", command = self.chooseFunctionality).grid(row = 1, column = 1)


    def changeStatus(self, sql):
        self.callbackWin.withdraw()
        self.connect(sql, "Insertion")
        self.viewApplications


    def viewPopularProjectReport(self):
        self.viewPopRptWin = Toplevel(self.loginWin)
        self.viewPopRptWin.geometry('{}x{}'.format(600, 400))
        self.viewPopRptWin.title("View popular project report")
        f = Frame(self.viewPopRptWin)
        f.pack()
        Label(f, text = "View Popular Project Report", font=("Helvetica", 20)).pack()

        f = Frame(self.viewPopRptWin)
        f.pack()
        Label(f, text = "Project Name").grid(row = 0, column = 0)
        Label(f, text = "Number of Students").grid(row = 0, column = 1)

        sql = "SELECT Name, NumStudent AS Number_of_Students FROM (Apply RIGHT OUTER JOIN Project ON Apply.Project_name = Project.Name) GROUP BY Name ORDER BY NumStudent DESC"
        popProjectList = self.connect(sql, "Return List")
        length = len(popProjectList)

        if length > 10:
            length = 10

        for i in range(1, length):
            Label(f, text = popProjectList[i][0]).grid(row = i, column = 0, sticky = W)
            Label(f, text = popProjectList[i][1]).grid(row = i, column = 1)

        f = Frame(self.viewPopRptWin)
        f.pack()
        Button(f, text = "Back", command = self.quitpopProjGotoFunc).grid(row = 0, column = 0)


    def viewApplicationReport(self):
        self.viewAppRptWin = Toplevel(self.loginWin)
        self.viewAppRptWin.geometry('{}x{}'.format(1000, 600))
        self.viewAppRptWin.title("View Application report")
        f = Frame(self.viewAppRptWin)
        f.pack()
        Label(f, text = "Application Report", font=("Helvetica", 20)).grid(row = 0, column = 0, columnspan = 4)

        Label(f, text = "Project").grid(row = 2, column = 0, padx = 5, pady = 5)
        Label(f, text = "# of Applicants").grid(row = 2, column = 1, sticky = W, padx = 10, pady = 5)
        Label(f, text = "Acceptance Rate").grid(row = 2, column = 2, sticky = W, padx = 20, pady = 5)
        Label(f, text = "Top 3 Majors").grid(row = 2, column = 3, sticky = W, padx = 10, pady = 5)

        projectList = self.connect("SELECT DISTINCT Project_name FROM Apply", "Return Single Item")
        totalCount = self.connect("SELECT COUNT(*) FROM Apply", "Return List")

        totalApplicants = 0
        totalAccepted = 0
        row_num = 3
        for element in projectList:

            numApp = self.connect("SELECT COUNT(Student_name) FROM Apply WHERE Project_name = \'%s\'" % element, "Return List")

            numAccepted = self.connect("SELECT COUNT(*) FROM Apply WHERE Project_name = \'%s\' AND Status = \'Accepted\'" % element, "Return List")
            findMajors = self.connect("SELECT DISTINCT Major FROM (User LEFT OUTER JOIN Apply ON User.Username = Apply.Student_name) WHERE Project_name = \'%s\'" % element, "Return Single Item")


            topThree = ''
            majorList = []
            numList = []

            for major in findMajors:
                sql = "SELECT COUNT(Username) Username FROM (User LEFT OUTER JOIN Apply ON User.Username = Apply.Student_name) WHERE Project_name = \'%s\' AND Major = \'%s\'" % (element, major)
                numMajors = self.connect(sql, "Return List")
                realNum = numMajors[0][0]
                numList.append(realNum)

            for i in range(3):
                max_value = max(numList)
                max_index = numList.index(max_value)
                if len(findMajors) >= i:
                    topMajor = findMajors.pop(max_index)
                    if topMajor != 'on':
                        topThree = topThree + topMajor + '/'


            numAccepted = int(numAccepted[0][0])
            numApp = int(numApp[0][0])
            acceptanceRate = numAccepted / numApp * 100
            acceptanceRate = str(acceptanceRate)
            acceptanceRate = acceptanceRate[:4] + "%"
            Label(f, text = element).grid(row = row_num, column = 0, padx = 5, sticky = W, pady = 5)
            Label(f, text = numApp).grid(row = row_num, column = 1, padx = 10, pady = 5)
            Label(f, text = acceptanceRate).grid(row = row_num, column = 2, padx = 20, pady = 5)
            Label(f, text = topThree).grid(row = row_num, column = 3, sticky = W, padx = 10, pady = 5)

            row_num = row_num + 1
            totalApplicants = int(totalApplicants) + numApp
            totalAccepted = totalAccepted + numAccepted
            textFormat = "%d Applications Total, %d accepted" % (totalApplicants, totalAccepted)
        Label(f, text = textFormat).grid(row = 1, column = 0, sticky = W, columnspan = 2)

        f = Frame(self.viewAppRptWin)
        f.pack()
        Button(f, text = "Back", command = self.quitAppRptGotoFunc).grid(row = 0, column = 0)


    def addProject(self):
        self.addProjectWin = Toplevel(self.loginWin)
        self.addProjectWin.title("Add a Project")

        f = Frame(self.addProjectWin)
        Label(f, text = "Add a New Project", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.addProjectWin)
        Label(f, text = "Project Name: ").grid(row = 0, column = 0)
        Label(f, text = "Advisor: ").grid(row = 1, column = 0)
        Label(f, text = "Advisor Email: ").grid(row = 2, column = 0)
        Label(f, text = "Description: ").grid(row = 3, column = 0)
        Label(f, text = "Estimated Num. Students: ").grid(row = 4, column = 0)
        self.sProjectName = StringVar()
        Entry(f, textvariable = self.sProjectName).grid(row = 0, column = 1)
        self.sAdvisor = StringVar()
        Entry(f, textvariable = self.sAdvisor).grid(row = 1, column = 1)
        self.sAdvisorEmail = StringVar()
        Entry(f, textvariable = self.sAdvisorEmail).grid(row = 2, column = 1)
        self.sDescription = StringVar()
        Entry(f, textvariable = self.sDescription).grid(row = 3, column = 1)
        self.sNumStudents = StringVar()
        Entry(f, textvariable = self.sNumStudents).grid(row = 4, column = 1)
        f.pack()

        f = Frame(self.addProjectWin)
        f.pack()
        Label(f, text = "Category: ").grid(row = 0, column = 0)
        OPTIONS1 = self.connect("SELECT DISTINCT Category_name FROM Project_is_category", "Return Single Item")
        self.dCategory = StringVar()
        dropdown1 = OptionMenu(f, self.dCategory, *OPTIONS1)
        dropdown1.config(width = 15, padx = 15, pady = 5)
        dropdown1.grid(row = 0, column = 1)
        Button(f, text = "Add a category", command = self.addCategory).grid(row = 0, column = 2)
        self.categorySet = set()

        Label(f, text = "Designation: ").grid(row = 1, column = 0)
        OPTIONS2 = self.connect("SELECT Name FROM Designation", "Return Single Item")
        self.dDesignation = StringVar()
        dropdown2 = OptionMenu(f, self.dDesignation, *OPTIONS2)
        dropdown2.config(width = 15, padx = 15, pady = 5)
        dropdown2.grid(row = 1, column = 1)

        Label(f, text = "Major Requirement: ").grid(row = 2, column = 0)
        OPTIONS3 = self.connect("SELECT Name FROM Major", "Return Single Item")
        self.dMjrRequirement = StringVar()
        dropdown3 = OptionMenu(f, self.dMjrRequirement, *OPTIONS3)
        dropdown3.config(width = 15, padx = 15, pady = 5)
        dropdown3.grid(row = 2, column = 1)

        Label(f, text = "Year Requirement: ").grid(row = 3, column = 0)
        OPTIONS4 = ['Only freshmen', 'Only sophomores', 'Only Juniors', 'Only seniors']
        self.dYrRequirement = StringVar()
        dropdown4 = OptionMenu(f, self.dYrRequirement, *OPTIONS4)
        dropdown4.config(width = 15, padx = 15, pady = 5)
        dropdown4.grid(row = 3, column = 1)

        Label(f, text = "Department Requirement: ").grid(row = 4, column = 0)
        OPTIONS5 = self.connect("SELECT Name FROM Department", "Return Single Item")
        self.dDptRequirement = StringVar()
        dropdown5 = OptionMenu(f, self.dDptRequirement, *OPTIONS5)
        dropdown5.config(width = 15, padx = 15, pady = 5)
        dropdown5.grid(row = 4, column = 1)

        f = Frame(self.addProjectWin)
        Button(f, text = "Submit", command = self.checkProject).pack()
        f.pack()

    def checkProject(self):
        projectName = self.sProjectName.get()
        advisor = self.sAdvisor.get()
        advisorEmail = self.sAdvisorEmail.get()
        description = self.sDescription.get()
        numStudent = self.sNumStudents.get()
        category = self.dCategory.get()

        count = 0
        requirementType = []
        requirementDesc = []
        if self.dMjrRequirement.get() != '':
            count = count + 1
            requirementType.append('Major')
            requirementDesc.append(self.dMjrRequirement.get())
        if self.dYrRequirement.get() != '':
            count = count + 1
            requirementType.append('Year')
            requirementDesc.append(self.dYrRequirement.get())
        if self.dDptRequirement.get() != '':
            count = count + 1
            requirementType.append('Department')
            requirementDesc.append(self.dDptRequirement.get())

        num1 = self.connect("SELECT * FROM Project WHERE Name = \'%s\'" % projectName, "Return Execution Number")
        #num2 = self.connect("SELECT * FROM User WHERE Email = \'%s\'" % email, "Return Execution Number")
        if num1 != 0:
            error = messagebox.showerror("Existed Project Name", "Pick Another Project Name")
        else:
            parameter1 = (projectName, description, self.dDesignation.get(), advisor, advisorEmail, numStudent)
            sql1 = "INSERT INTO Project(Name, Description, Designation_name, Advisor_name, Advisor_email, NumStudent) VALUES (\'%s\' ,\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % parameter1
            self.connect(sql1, "Insertion")

            for i in range(count):
                parameter2 = (projectName, requirementDesc[i], requirementType[i])
                sql2 = "INSERT INTO Project_requirement(Name,Requirement,Type) VALUES (\'%s\' ,\'%s\', \'%s\')" % parameter2
                self.connect(sql2, "Insertion")

            # parameter3 = (projectName, category)
            # sql3 = "INSERT INTO Project_is_category(Project_name,Category_name) VALUES (\'%s\' ,\'%s\', \'%s\')" % parameter3
            # self.connect(sql3, "Insertion")

            for category in self.categorySet:
                sql1 = "INSERT INTO Project_is_category(Project_name, Category_name) VALUES (\'%s\', \'%s\')" % (projectName, category)
                self.connect(sql1, "Insertion")

            message = messagebox.showinfo("Congratulations", "New Project Added!")
            self.addProjectWin.withdraw()


    def addCourse(self):
        self.addCourseWin = Toplevel(self.loginWin)
        self.addCourseWin.title("Add a Course")

        f = Frame(self.addCourseWin)
        Label(f, text = "Add a Course", font=("Helvetica", 20)).pack()
        f.pack()

        f = Frame(self.addCourseWin)
        Label(f, text = "Course Number: ", font=("Helvetica", 20)).grid(row = 0, column = 0)
        self.sCourseNum = StringVar()
        Entry(f, textvariable = self.sCourseNum).grid(row = 0, column = 1)
        Label(f, text = "Course Name: ", font=("Helvetica", 20)).grid(row = 1, column = 0)
        self.sCourseName = StringVar()
        Entry(f, textvariable = self.sCourseName).grid(row = 1, column = 1)
        Label(f, text = "Instructor: ", font=("Helvetica", 20)).grid(row = 2, column = 0)
        self.sInstructor = StringVar()
        Entry(f, textvariable = self.sInstructor).grid(row = 2, column = 1)
        Label(f, text = "Designation", font=("Helvetica", 20)).grid(row = 3, column = 0)
        self.sDesignation = StringVar()
        OPTIONS = self.connect("SELECT Name FROM Designation", "Return Single Item")
        dropdown = OptionMenu(f, self.sDesignation, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 3, column = 1)
        Label(f, text = "Category", font=("Helvetica", 20)).grid(row = 4, column = 0)
        OPTIONS = self.connect("SELECT Name FROM Category", "Return Single Item")
        self.dCategory = StringVar()
        dropdown = OptionMenu(f, self.dCategory, *OPTIONS)
        dropdown.config(width = 10)
        dropdown.grid(row = 4, column = 1)
        Button(f, text = "Add a category", command = self.addCategory).grid(row = 4, column = 2)
        self.categorySet = set()
        Label(f, text = "Estimated # of students: ", font=("Helvetica", 20)).grid(row = 5, column = 0)
        self.sNumStudent = IntVar()
        Entry(f, textvariable = self.sNumStudent).grid(row = 5, column = 1)
        f.pack()

        f = Frame(self.addCourseWin)
        Button(f, text = "Back", command = lambda: self.returnTo(self.addCourseWin, self.self.chooseFuncWin)).grid(row = 0, column = 0)
        Button(f, text = "Submit", command = self.addaCourse).grid(row = 0, column = 1)
        f.pack()

    def addaCourse(self):
        sql = "INSERT INTO Course(Name, Course_Number, Instructor, Designation_name, NumStudent) VALUES (\'%s\' ,\'%s\' ,\'%s\', \'%s\', \'%i\')" % (self.sCourseName.get(), self.sCourseNum.get(), self.sInstructor.get(), self.sDesignation.get(), int(self.sNumStudent.get()))
        self.connect(sql, "Insertion")

        for category in self.categorySet:
            sql1 = "INSERT INTO Course_is_category(Course_name, Category_name) VALUES (\'%s\', \'%s\')" % (self.sCourseName.get(), category)
            self.connect(sql1, "Insertion")
        self.returnTo(self.addCourseWin, self.chooseFuncWin)

###################################################### General Methods


    ## Return to returnTo window while destroy window
    def returnTo(self, window, returnTo=None):
        window.destroy()
        if returnTo != None:
            returnTo.deiconify()

    def quitviewAppGotoFunc(self):
        self.closeViewApp()
        self.chooseFunctionality

    def closeViewApp(self):
        self.viewAppsWin.withdraw()

    def quitpopProjGotoFunc(self):
        self.closePopProj()
        self.chooseFunctionality

    def closePopProj(self):
        self.viewPopRptWin.withdraw()

    def quitAppRptGotoFunc(self):
        self.closeAppRpt()
        self.chooseFunctionality

    def closeAppRpt(self):
        self.viewAppRptWin.withdraw()


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
