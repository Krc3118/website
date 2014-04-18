from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Candidate(models.Model):
    user = models.OneToOneField(User)
    family = models.CharField(max_length=200)
    committee = models.CharField(max_length=200)
    
    def get_progress(self):
        pass
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Officer(User):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('FH', 'Fifth Year'),
        ('MA', 'Masters Student'),
        ('PH', 'Ph.D. Student'),
    )
    OFFICER_POSITION_CHOICES = (
        (1, 'President'),
        (2, 'Vice President'),
        (3, 'Secretary'),
        (4, 'Treasurer'),
        (5, 'Professional Development'),
        (6, 'Industrial Relations'),
        (7, 'Social'),
        (8, 'Publicity'),
        (9, 'Technology'),
    )

    position_dict = dict(OFFICER_POSITION_CHOICES)

    year_in_school = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES, default='FR')
    phone_number = models.IntegerField(max_length=10)
    position = models.IntegerField(max_length=1, choices=OFFICER_POSITION_CHOICES, default=1)
    photo = models.ImageField(upload_to='images/officers/')
    office_hours = models.ManyToManyField('OfficeHour')
    classes_taken = models.ManyToManyField('BerkeleyClass', through='OfficerClass')

    def __str__(self):
        return self.username

    def name(self):
        return self.first_name + " " + self.last_name

    def positionname(self):
        return self.position_dict[self.position]

    def schedule(self):
        slots = sorted(self.office_hours.all(), key=lambda x: x.day_of_week * 100 + x.hour)
        str = ""
        if len(slots) > 0:
            str += slots[0].name()
        for i in range(1, len(slots)):
            str += ", " + slots[i].name()
        return str

    def experience(self):
        classes = sorted(self.classes_taken.all(), key=lambda x: x.class_name)
        str = ""
        if len(classes) > 0:
            str += classes[0].name()
        for i in range(1, len(classes)):
            str += ", " + classes[i].name()
        return str

class OfficerClass(models.Model):
    berkeley_class = models.ForeignKey('BerkeleyClass')
    officer = models.ForeignKey('Officer')

class OfficeHour(models.Model):
    DAY_OF_WEEK_CHOICES = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
    )
    TIME_OF_DAY_CHOICES = (
        (11, '11 AM'),
        (12, '12 PM'),
        (13, '1 PM'),
        (14, '2 PM'),
        (15, '3 PM'),
        (16, '4 PM'),
        (17, '5 PM'),
    )

    day_dict = dict(DAY_OF_WEEK_CHOICES)
    time_dict = dict(TIME_OF_DAY_CHOICES)

    day_of_week = models.IntegerField(max_length=1, choices=DAY_OF_WEEK_CHOICES, default=1)
    hour = models.IntegerField(max_length=2, choices=TIME_OF_DAY_CHOICES, default=11)
    officer_username = models.CharField(max_length=30,
        help_text='Please enter a valid officer username as this is used for website queries.')

    def __str__(self):
        return self.name() + " " + self.officer_username

    def name(self):
        return self.day_dict[self.day_of_week] + " " + self.time_dict[self.hour]

class BerkeleyClass(models.Model):
    CLASS_CHOICES = (
        (10100, 'CS 10'),
        (10610, 'CS 61A'),
        (10611, 'CS 61AS'),
        (10612, 'CS 61B/L'),
        (10613, 'CS 61C'),
        (10700, 'CS 70'),
        (11490, 'CS 149'),
        (11500, 'CS 150'),
        (11600, 'CS 160'),
        (11610, 'CS 161'),
        (11620, 'CS 162'),
        (11640, 'CS 164'),
        (11690, 'CS 169'),
        (11700, 'CS 170'),
        (11720, 'CS 172'),
        (11740, 'CS 174'),
        (11760, 'CS 176'),
        (11840, 'CS 184'),
        (11860, 'CS 186'),
        (11880, 'CS 188'),
        (11890, 'CS 189'),
        (11945, 'CS 194-5'),
        (11948, 'CS 194-8'),
        (11950, 'CS 195'),
        (20200, 'EE 20'),
        (20400, 'EE 40'),
        (21050, 'EE 105'),
        (21170, 'EE 117'),
        (21180, 'EE 118'),
        (21200, 'EE 120'),
        (21210, 'EE 121'),
        (21220, 'EE 122'),
        (21230, 'EE 123'),
        (21250, 'EE 125'),
        (21260, 'EE 126'),
        (21270, 'EE 127'),
        (21280, 'EE 128'),
        (21300, 'EE 130'),
        (21340, 'EE 134'),
        (21370, 'EE 137A'),
        (21371, 'EE 137B'),
        (21400, 'EE 140'),
        (21410, 'EE 141'),
        (21420, 'EE 142'),
        (21430, 'EE 143'),
        (21440, 'EE 144'),
        (21451, 'EE 145B'),
        (21470, 'EE 147'),
        (21490, 'EE 149'),
        (21500, 'EE 150'),
        (21920, 'EE 192'),
        (30010, 'Math 1A'),
        (30011, 'Math 1B'),
        (30530, 'Math 53'),
        (30540, 'Math 54'),
        (31040, 'Math 104'),
        (31100, 'Math 110'),
        (31130, 'Math 113'),
        (31280, 'Math 128A'),
        (31850, 'Math 185'),
    )

    class_dict = dict(CLASS_CHOICES)
    class_name = models.IntegerField(max_length=5, choices=CLASS_CHOICES)
    officers = models.ManyToManyField('Officer', through='OfficerClass')

    def __str__(self):
        return self.class_dict[self.class_name]

    def name(self):
        return self.class_dict[self.class_name]

class Requirement(models.Model):    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    candidates = models.ManyToManyField('Candidate', through='Completion')
    REQUIREMENT_TYPE = (
        ('SOC', 'Social'),
        ('PRO', 'Professional'),
        ('IND', 'Individual'),
        ('FAM', 'Family'),
        ('ACM', 'ACM Payment'),
        ('INI', 'Initiation Attendance'),
        ('GM', 'General Meetings')
    )
    req_dict = dict(REQUIREMENT_TYPE)
    req_type = models.CharField(max_length=3, choices=REQUIREMENT_TYPE, default='SOC')

    def __str__(self):
        return self.req_dict[self.req_type]

class Completion(models.Model):
    candidate = models.ForeignKey(Candidate)
    requirement = models.ForeignKey(Requirement)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(default = date.today)
    