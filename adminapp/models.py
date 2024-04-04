from django.db import models

class Major(models.Model):
    MajorID = models.AutoField(primary_key=True,null= False)
    MajorName = models.CharField(max_length=50,null= False)
    Description = models.TextField()
    MajorCode = models.CharField(max_length=50,null= False) 

    def __str__(self):
        return self.name

class Academic_Year(models.Model):
    AcademicYearID = models.AutoField(primary_key=True)
    Year = models.CharField(max_length=50,null= False)

    def __str__(self):
        return self.name

class Academic_Program(models.Model):
    ProgramID = models.AutoField(primary_key=True)
    ProgramName = models.CharField(max_length=50,null= False)
    ProgramCode = models.CharField(max_length=50,null= False,default='0')
    ModeofStudy = models.CharField(max_length=50,null= False)
    DurationOfTraning = models.CharField(max_length=50,null= False)
    Description = models.TextField()
    MajorID = models.ForeignKey(Major,on_delete = models.CASCADE, to_field = 'MajorID' )
    def __str__(self):
        return self.name

class Year_Based_Academic_Program(models.Model):
    YBAP_ID = models.AutoField(primary_key=True)
    AcademicYearID  = models.ForeignKey(Academic_Year,on_delete = models.CASCADE, to_field = 'AcademicYearID')
    ProgramID = models.ForeignKey(Academic_Program,on_delete = models.CASCADE, to_field = 'ProgramID')

    def __str__(self):
        return self.name  

class Student(models.Model):
    StudentID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50,null=False)
    LastName = models.CharField(max_length=50,null=False)
    Gender = models.BooleanField(null=False)
    DateOfBirth = models.DateField(null=False)
    Address = models.CharField(max_length=50,null=False)
    Nation = models.CharField(max_length=50,null=False)
    Nationality = models.CharField(max_length=50,null=False)
    PhoneNumber = models.CharField(max_length=50,null = True)
    Email = models.EmailField(max_length=50,null = True)
    MSSV = models.CharField(max_length=50, null= False)
    YearOfAdmission = models.CharField(max_length=50,null= False)
    ## YBAP_ID = models.ForeignKey(Year_Based_Academic_Program, on_delete = models.CASCADE, to_field = 'YBAP_ID')

    def __str__(self):
        return self.name
    

class Degree_Book(models.Model):
    DegreeBookID = models.AutoField(primary_key=True)
    NumberOfGraduationDecision = models.CharField(max_length=50,null= False)
    GraduationDecisionDate = models.DateField(null= False)
    NumberInTheDegreeBook = models.CharField(max_length=50,null= False)
    StudentID = models.ForeignKey(Student, on_delete = models.CASCADE, to_field = 'StudentID')

    def __str__(self):
        return self.name
    
class Degree_Infomation(models.Model):
    DegreeID = models.AutoField(primary_key=True)
    Classification = models.CharField(max_length=50,null= False)
    YearOfGraduation = models.CharField(max_length=50,null= False)
    SerialNumber = models.CharField(max_length=50,null= False)
    DegreeBookID = models.OneToOneField(Degree_Book, on_delete = models.CASCADE, to_field = 'DegreeBookID')

    def __str__(self):
        return self.name
    
    


