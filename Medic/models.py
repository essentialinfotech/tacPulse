import builtins
from typing import Set
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.deletion import SET_NULL
from django.db.models.enums import Choices
from django.views.generic.base import TemplateView
from Accounts.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from Accounts.models import User
# Create your models here.


class Panic(models.Model):
    emergency_contact = models.CharField(max_length=40, blank=True, null=True)
    panic_sender = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, blank=False, null=False)
    place = models.CharField(max_length=2000, blank=True, null=True)
    lat = models.CharField(max_length=200, blank=True, null=True)
    lng = models.CharField(max_length=200, blank=True, null=True)
    assigned = models.BooleanField(default=False)
    # is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.panic_sender.first_name


class Rating(models.Model):
    rated_value = models.IntegerField(blank=True, null=True, default=0)
    all_time_rated_value_store = models.IntegerField(
        blank=True, null=True, default=0)
    count = models.IntegerField(blank=True, null=True, default=0)
    avg_rating = models.FloatField(blank=True, null=True, default=0.0)

    def __str__(self):
        return str(self.avg_rating)


class Feedback(models.Model):
    author = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    feedback_text = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def name(self):
        user = self.author.first_name
        if user != '':
            return user
        else:
            user = self.author.username
            return user


class Occurrence(models.Model):
    REASON_FOR_REPORT = [
        ('Property Issue', 'Property Issue'),
        ('Operational Issue', 'Operational Issue'),
        ('Employee Issue', 'Employee Issue'),
        ('Conditions in Work Place', 'Conditions in Work Place'),
        ('Health & Safety Concern / Issue', 'Health & Safety Concern / Issue'),
        ('Vehicle Issue', 'Vehicle Issue'),
        ('Customer Compliment', 'Customer Compliment'),
        ('Customer Complaint', 'Customer Complaint'),
    ]

    DEPARTMENT = [
        ('Emergency Medical Dispatching Centre', 'Emergency Medical Dispatching Centre'),
        ('Stock Issue (Consumable Stock)', 'Stock Issue (Consumable Stock)'),
        ('Operations', 'Operations'),
    ]

    occurrence_giver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    occurrence_id = models.CharField(max_length=30000,blank=True, null=True)
    reason_for_report = models.CharField(max_length=100,blank=True, null=True,choices=REASON_FOR_REPORT)
    department = models.CharField(max_length = 100, choices = DEPARTMENT,blank=True, null=True)
    occurrence_date = models.DateField(blank=True, null=True)
    incident_report = models.TextField(blank=True, null=True)
    signature = models.CharField(blank=True, null=True,max_length=100)
    image = models.ImageField(upload_to = 'occurrence', blank=True, null=True)
    captured_phote = models.ImageField(upload_to = 'occurrence', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return str(self.occurrence_id)

    @property
    def imagesURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return str(self.occurrence_id)


# dispatch incident
class Senior(models.Model):
    senior_name = models.CharField(max_length=500,blank=False,null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.senior_name

class Scribe(models.Model):
    scribe_name = models.CharField(max_length=500,blank=False,null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.scribe_name

class Assist01(models.Model):
    a1_name = models.CharField(max_length=500,blank=False,null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.a1_name

class Assist02(models.Model):
    a2_name = models.CharField(max_length=500,blank=False,null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.a2_name

class AmbulanceModel(models.Model):
    INCIDENT = [
        ('Primary','Primary'),
        ('IHT','IHT'),
        ('RAF IHT','RAF IHT'),
        ('Non-Emergency','Non-Emergency'),
    ]

    PPE_LEVEL = [
        ('A','A'),
        ('A+CHAMBER','A+CHAMBER'),
        ('B','B'),
        ('C','C'),
    ]

    BILLING_TYPE = [
        ('MEDICAL AID / INSURANCE','MEDICAL AID / INSURANCE'),
        ('RAF','RAF'),
        ('WCA','WCA'),
        ('PRIVATE (CASH)','PRIVATE (CASH)'),
        ('FIXED RATE TRANSFER','FIXED RATE TRANSFER'),
        ('STATE (DoH)','STATE (DoH)'),
        ('MEMBERSHIP','MEMBERSHIP'),
        ('COMMUNITY INITIATIVE','COMMUNITY INITIATIVE'),
        ('HELIVAC / CIMS','HELIVAC / CIMS'),
    ]

    BILLING_SOURCE = [
        ('21st CENTURY LIFE >> EASA INSURANCE (PRE-AUTH!!)','21st CENTURY LIFE >> EASA INSURANCE (PRE-AUTH!!)'),
        ('ADCORP>> EASA INSURANCE (PRE-AUTH)','ADCORP>> EASA INSURANCE (PRE-AUTH)'),
        ('ADT Security >> ER24 INSURANCE PACK - PRE-AUTH!!!','ADT Security >> ER24 INSURANCE PACK - PRE-AUTH!!!'),
        ('AECI MEDICAL AID - VALUE OPTION > ER24','AECI MEDICAL AID - VALUE OPTION > ER24'),
        ('AECI MEDICAL AID > ER24','AECI MEDICAL AID > ER24'),
        ('AFFINITY HEALTH >> ER24 INSURANCE PACK - PRE-AUTH!!','AFFINITY HEALTH >> ER24 INSURANCE PACK - PRE-AUTH!!'),
        ('AFRICAN UNITY HEALTH / PSG >> ER24 INSURANCE PACK - PRE-AUTH!!','AFRICAN UNITY HEALTH / PSG >> ER24 INSURANCE PACK - PRE-AUTH!!'),
        ('AFRICAN UNITY>> EASA INSURANCE (PRE-AUTH!!)','AFRICAN UNITY>> EASA INSURANCE (PRE-AUTH!!)'),
        ('ALLIANCE MIDMED MEDICAL SCHEME >> EASA','ALLIANCE MIDMED MEDICAL SCHEME >> EASA'),
        ('ANGLO MEDICAL SCHEME >> NTC911','ANGLO MEDICAL SCHEME >> NTC911'),
        ('ANGLOVAAL MEDICAL SCHEME >> Discovery','ANGLOVAAL MEDICAL SCHEME >> Discovery'),
        ('ASTERIO HEALTH >> AFRICA ASSIST (PRE-AUTH!!)','ASTERIO HEALTH >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('BANKMED MEDICAL AID>> NTC911','BANKMED MEDICAL AID>> NTC911'),
        ('BARLOW WORLD MEDICAL SCHEME>> NTC911','BARLOW WORLD MEDICAL SCHEME>> NTC911'),
        ('BEMAS (BMW EMPLOYEES MEDICAL AID) >> NTC911','BEMAS (BMW EMPLOYEES MEDICAL AID) >> NTC911'),
        ('BESTMED MEDICAL SCHEME> ER24','BESTMED MEDICAL SCHEME> ER24'),
        ('BONITAS MEDICAL AID SCHEME> ER24','BONITAS MEDICAL AID SCHEME> ER24'),
        ('BP MEDICAL SCHEME (BPMAS)','BP MEDICAL SCHEME (BPMAS)'),
        ('BUILDERS & CONSTRUCTION INDUSTRY (BCIMA) MEDICAL AID >> INDEPENDENT','BUILDERS & CONSTRUCTION INDUSTRY (BCIMA) MEDICAL AID >> INDEPENDENT'),
        ('BUILDING INDUSTRY MEDICAL AID FUND (BIBC / BIMAF) >> NTC911','BUILDING INDUSTRY MEDICAL AID FUND (BIBC / BIMAF) >> NTC911'),
        ('CAMAF SA & NAMIBIA >> NTC911','CAMAF SA & NAMIBIA >> NTC911'),
        ('CAPE MEDICAL PLAN>> INDEPENDENT','CAPE MEDICAL PLAN>> INDEPENDENT'),
        ('COMPCARE WELLNESS MEDICAL SCHEME >> NTC911','COMPCARE WELLNESS MEDICAL SCHEME >> NTC911'),
        ('COVISION LIFE>> EASA INSURANCE (PRE-AUTH!!)','COVISION LIFE>> EASA INSURANCE (PRE-AUTH!!)'),
        ('CRISIS ON CALL>> EASA INSURANCE (PRE-AUTH!!)','CRISIS ON CALL>> EASA INSURANCE (PRE-AUTH!!)'),
        ('DAY 1 HEALTH>> ER24 INSURANCE PACK- PRE-AUTH!!','DAY 1 HEALTH>> ER24 INSURANCE PACK- PRE-AUTH!!'),
        ('DE BEERS BENEFIT SOCIETY> ER24','DE BEERS BENEFIT SOCIETY> ER24'),
        ('DIMARU HEALTH >> AFRICA ASSIST (PRE-AUTH!!)','DIMARU HEALTH >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('DISCOVERY HEALTH MEDICAL SCHEME >> DISCOVERY','DISCOVERY HEALTH MEDICAL SCHEME >> DISCOVERY'),
        ('ENGEN MEDICAL SCHEME> ER24','ENGEN MEDICAL SCHEME> ER24'),
        ('EQUIPAGE>> ER24 INSURANCE PACK-PRE-AUTH!!','EQUIPAGE>> ER24 INSURANCE PACK-PRE-AUTH!!'),
        ('ESSENTIAL EMPLOYEE BENEFITS>>AFRICA ASSIST(PRE-AUTH!!)','ESSENTIAL EMPLOYEE BENEFITS>>AFRICA ASSIST(PRE-AUTH!!)'),
        ('ESSENTIAL MED >> AFRICA ASSIST (PRE-AUTH!!)','ESSENTIAL MED >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('FEDHEALTH INDUSTRY SCHEME >> EASA','FEDHEALTH INDUSTRY SCHEME >> EASA'),
        ('FISHING INDUSTRY MEDICAL SCHEME (FISH-MED)>> INDEPENDENT','FISHING INDUSTRY MEDICAL SCHEME (FISH-MED)>> INDEPENDENT'),
        ('FMS - 1 LIFE>> AFRICA ASSIST (PRE-AUTH!!)','FMS - 1 LIFE>> AFRICA ASSIST (PRE-AUTH!!)'),
        ('FMS-EMERALD WEALTH MANAGEMENT>> AFRICA ASSIST (PRE-AUTH!!)','FMS-EMERALD WEALTH MANAGEMENT>> AFRICA ASSIST (PRE-AUTH!!)'),
        ('FMS 1 LIFE ONLY (MUST RECEIVE CALL FROM ER24)>> ER24 INSURANCE PACK - PRE-AUTH!!','FMS 1 LIFE ONLY (MUST RECEIVE CALL FROM ER24)>> ER24 INSURANCE PACK - PRE-AUTH!!'),
        ('FOOD WORKERS MEDICAL BENEFIT FUND >> INDEPENDENT','FOOD WORKERS MEDICAL BENEFIT FUND >> INDEPENDENT'),
        ('FURNITURE BEDDING & UPHOLSTERY INDUSTRY BAGAINING COUNCIL (FURNMED)>> NTC911','FURNITURE BEDDING & UPHOLSTERY INDUSTRY BAGAINING COUNCIL (FURNMED)>> NTC911'),
        ('GEMS>>EASA','GEMS>>EASA'),
        ('GENESIS MEDICAL AID> ER24','GENESIS MEDICAL AID> ER24'),
        ('GET SAVVI HEALTH >> NTC911(INSURANCE PRODUCT> PRE-AUTH)','GET SAVVI HEALTH >> NTC911(INSURANCE PRODUCT> PRE-AUTH)'),
        ('GLENCORE MEDICAL AID SCHEME >> EASA','GLENCORE MEDICAL AID SCHEME >> EASA'),
        ('GOLDEN ARROW >> NTC911','GOLDEN ARROW >> NTC911'),
        ('GRINTEK ELECTRONICS MEDICAL AID SCHEME>ER24','GRINTEK ELECTRONICS MEDICAL AID SCHEME>ER24'),
        ('HEALTH SQUARED MEDICAL SCHEME(RESOLUTION & SPECTEAMED MERGER)>> NTC911','HEALTH SQUARED MEDICAL SCHEME(RESOLUTION & SPECTEAMED MERGER)>> NTC911'),
        ('HOLLARD FENOMINAL WOMEN>> EASA INSURANCE(PRE-AUTH!!)','HOLLARD FENOMINAL WOMEN>> EASA INSURANCE(PRE-AUTH!!)'),
        ('HORIZON MEDICAL SCHEME>ER24','HORIZON MEDICAL SCHEME>ER24'),
        ('HOSMED MEDICAL AID> ER24','HOSMED MEDICAL AID> ER24'),
        ('IMPALA MEDICAL PLAN>> INDEPENDENT','IMPALA MEDICAL PLAN>> INDEPENDENT'),
        ('IMPERIAL GROUP MEDICAL SCHEME>> EASA','IMPERIAL GROUP MEDICAL SCHEME>> EASA'),
        ('INDEPENDENT MEDICAL SCHEME / INSURANCE PRODUCT (SPECIFY)','INDEPENDENT MEDICAL SCHEME / INSURANCE PRODUCT (SPECIFY)'),
        ('INFUSION FINANCIAL SERVICES>>EASA INSURANCE(PRE-AUTH!!)','INFUSION FINANCIAL SERVICES>>EASA INSURANCE(PRE-AUTH!!)'),
        ('KARDIOFIT>>ER24 INSURANCE PACK - PRE-AUTH!!','KARDIOFIT>>ER24 INSURANCE PACK - PRE-AUTH!!'),
        ('KEYHEALTH >>NTC911','KEYHEALTH >>NTC911'),
        ('KGA LIFE>> EASA INSURANCE(PRE-AUTH!!)','KGA LIFE>> EASA INSURANCE(PRE-AUTH!!)'),
        ('LA HEALTH >> DISCOVERY','LA HEALTH >> DISCOVERY'),
        ('LIBCARE MEDICAL SCHEME >> NTC911','LIBCARE MEDICAL SCHEME >> NTC911'),
        ('LIBERTY MEDICAL LIFESTYLE PLUS>>EASA INSURANCE (PRE-AUTH!!)','LIBERTY MEDICAL LIFESTYLE PLUS>>EASA INSURANCE (PRE-AUTH!!)'),
        ('LONMIN MEDICAL SCHEME >> DISCOVERY','LONMIN MEDICAL SCHEME >> DISCOVERY'),
        ('M-MED >> DISCOVERY','M-MED >> DISCOVERY'),
        ('MAKOTI (COMPREHENSIVE OPTIONS) >> LIFEMED','MAKOTI (COMPREHENSIVE OPTIONS) >> LIFEMED'),
        ('MAKOTI (PRIMARY OPTIONS) >> LIFEMED','MAKOTI (PRIMARY OPTIONS) >> LIFEMED'),
        ('MALCOR (OPTION D ONLY)>> LIFEMED','MALCOR (OPTION D ONLY)>> LIFEMED'),
        ('MALCOR MEDICAL AID SCHEME>> DISCOVERY','MALCOR MEDICAL AID SCHEME>> DISCOVERY'),
        ('MAMOTH MEDICAL SCHEME> ER24','MAMOTH MEDICAL SCHEME> ER24'),
        ('MBMED (Mercedes Benz Medical Aid)>ER24','MBMED (Mercedes Benz Medical Aid)>ER24'),
        ('Medibond >> AFRICA ASSIST (PRE-AUTH!!)','Medibond >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('Medicall >> AFRICA ASSIST (PRE-AUTH!!)','Medicall >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('MEDIHELP MEDICAL SCHEME >> NTC911','MEDIHELP MEDICAL SCHEME >> NTC911'),
        ('MEDIMED MEDICAL SCHEME> ER24','MEDIMED MEDICAL SCHEME> ER24'),
        ('MEDIPOS MEDICAL SCHEME>> INDEPENDENT','MEDIPOS MEDICAL SCHEME>> INDEPENDENT'),
        ('Medpro >> AFRICA ASSIST (PRE-AUTH!!)','Medpro >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('MEDSHIELD MEDICAL SCHEME>> NTC911','MEDSHIELD MEDICAL SCHEME>> NTC911'),
        ('METROPOLITAN MEDICAL SCHEME>> INDEPENDENT','METROPOLITAN MEDICAL SCHEME>> INDEPENDENT'),
        ('MOMENTUM HEALTH>> NTC911','MOMENTUM HEALTH>> NTC911'),
        ('MOTO HEALTH MEDICAL SCHEME>> EASA','MOTO HEALTH MEDICAL SCHEME>> EASA'),
        ('MY STROKE>> ER24 INSURANCE PACK - PRE-AUTH!!','MY STROKE>> ER24 INSURANCE PACK - PRE-AUTH!!'),
        ('NASPERS>> DISCOVERY','NASPERS>> DISCOVERY'),
        ('NATIONAL DEFENSE FORCE MEDICAL SCHEME','NATIONAL DEFENSE FORCE MEDICAL SCHEME'),
        ('NBCRFLI Sick Fund >> AFRICA ASSIST (PRE-AUTH!!)','NBCRFLI Sick Fund >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('NEDGROUP MEDICAL AID SCHEME> ER24','NEDGROUP MEDICAL AID SCHEME> ER24'),
        ('NEDLIFE>> EASA INSURANCE (PRE-AUTH!!)','NEDLIFE>> EASA INSURANCE (PRE-AUTH!!)'),
        ('NETCARE MEDICAL AID SCHEME >> NTC911','NETCARE MEDICAL AID SCHEME >> NTC911'),
        ('MEW APOSTOLIC CHURCH>> EASA INSURANCE (PRE-AUTH)','MEW APOSTOLIC CHURCH>> EASA INSURANCE (PRE-AUTH)'),
        ('NUFASWA>> NTC911','NUFASWA>> NTC911'),
        ('OLD MUTUAL FAMILY SUPPORT SERVICES>> EASA INSURANCE (PRE-AUTH!!)','OLD MUTUAL FAMILY SUPPORT SERVICES>> EASA INSURANCE (PRE-AUTH!!)'),
        ('OLD MUTUAL MORE 4 U>> EASA INSURANCE(PRE-AUTH)','OLD MUTUAL MORE 4 U>> EASA INSURANCE(PRE-AUTH)'),
        ('OLD MUTUAL STAFF MEDICAL AID FUND> ER24','OLD MUTUAL STAFF MEDICAL AID FUND> ER24'),
        ('OPTIMUM MEDICAL SCHEME (OPMED)> ER24','OPTIMUM MEDICAL SCHEME (OPMED)> ER24'),
        ('PARMED MEDICAL AID >> NTC911','PARMED MEDICAL AID >> NTC911'),
        ('PG GROUP HEALTH>> NTC911','PG GROUP HEALTH>> NTC911'),
        ('PICK N PAY MEDICAL SCHEME>ER24','PICK N PAY MEDICAL SCHEME>ER24'),
        ('PLATINUM HEALTH >> EASA','PLATINUM HEALTH >> EASA'),
        ('POLMED MEDICAL SCHEME>> ER24 (POSY-AUTH<72H)','POLMED MEDICAL SCHEME>> ER24 (POSY-AUTH<72H)'),
        ('PROFMED >> NTC911','PROFMED >> NTC911'),
        ('QUANTUM >> DISCOVERY','QUANTUM >> DISCOVERY'),
        ('RAND WATER MEDICAL SCHEME>> NTC911','RAND WATER MEDICAL SCHEME>> NTC911'),
        ('REMEDI MEDICAL SCHEME> ER24','REMEDI MEDICAL SCHEME> ER24'),
        ('RETAIL MEDICAL SCHEME>> DISCOVERY','RETAIL MEDICAL SCHEME>> DISCOVERY'),
        ('RHODES UNIVERSITY MEDICAL SCHEME (RUMED)>ER24','RHODES UNIVERSITY MEDICAL SCHEME (RUMED)>ER24'),
        ('SABC MEDICAL AID SCHEME>> NTC911','SABC MEDICAL AID SCHEME>> NTC911'),
        ('SABMAS >> NTC911','SABMAS >> NTC911'),
        ('SAMWUMED >> NTC911','SAMWUMED >> NTC911'),
        ('SASOLMED> ER24','SASOLMED> ER24'),
        ('SISONKE HEALTH MEDICAL SCHEME >> NTC911','SISONKE HEALTH MEDICAL SCHEME >> NTC911'),
        ('SIZWE MEDICAL FUND>> EASA','SIZWE MEDICAL FUND>> EASA'),
        ('SUREMED HEALTH (SOUTH AFRICA)> ER24','SUREMED HEALTH (SOUTH AFRICA)> ER24'),
        ('SUREMED MOZAMBIQUE> ER24','SUREMED MOZAMBIQUE> ER24'),
        ('THE FOSCHINI GROUP (TFG) >> DISCOVERY','THE FOSCHINI GROUP (TFG) >> DISCOVERY'),
        ('THEBEMED MEDICAL SCHEME >> NTC911','THEBEMED MEDICAL SCHEME >> NTC911'),
        ('TIGER BRANDS MEDICAL SCHEME> ER24','TIGER BRANDS MEDICAL SCHEME> ER24'),
        ('TRANSMED MEDICAL FUND >> EASA','TRANSMED MEDICAL FUND >> EASA'),
        ('TSOGO SUN MEDICAL SCHEME >> DISCOVERY','TSOGO SUN MEDICAL SCHEME >> DISCOVERY'),
        ('UMVUZO HEALTH(ULTRA)','UMVUZO HEALTH(ULTRA)'),
        ('UNITY HEALTH>> ER24 INSURANCE PACK- PRE-AUTH!!','UNITY HEALTH>> ER24 INSURANCE PACK- PRE-AUTH!!'),
        ('UNIVERSITY OF KWAZULU NATAL MEDICAL SCHEME> ER24','UNIVERSITY OF KWAZULU NATAL MEDICAL SCHEME> ER24'),
        ('UNIVERSITY OF WITWATERSRAND (WITS MED)>> DISCOVERY','UNIVERSITY OF WITWATERSRAND (WITS MED)>> DISCOVERY'),
        ('Wesmart >> AFRICA ASSIST (PRE-AUTH!!)','Wesmart >> AFRICA ASSIST (PRE-AUTH!!)'),
        ('WITBANK COALFIELDS MEDICAL AID SCHEME(WCMAS)> ER24','WITBANK COALFIELDS MEDICAL AID SCHEME(WCMAS)> ER24'),
        ('WOOLTRU MEDICAL AID>> NTC911','WOOLTRU MEDICAL AID>> NTC911'),
        ('XELUS / MY HEALTH>> ER24 INSURANCE PACK-PRE-AUTH!!','XELUS / MY HEALTH>> ER24 INSURANCE PACK-PRE-AUTH!!'),

    ]

    CREW_OPERATIONAL_STATUS = [
        ('On Duty','On Duty'),
        ('Active Standby','Active Standby'),
        ('off_Duty Call','off_Duty Call'),
    ]

    HOW_MANY_UNITS_DISPATCHED = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
    
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=100, blank=False, null=False)
    chief_complain = models.TextField(blank=True,null=True)
    incident_category = models.CharField(max_length=100, blank=False, null=False,choices=INCIDENT)
    ppe_lvl = models.CharField(max_length = 100, blank=True,null=True,choices=PPE_LEVEL)
    pick_up_address = models.CharField(max_length=500,blank=False,null=False)
    billing_type = models.CharField(max_length = 300,choices=BILLING_TYPE)
    billing_source = models.CharField(max_length=10000,blank=True,null=True,choices=BILLING_SOURCE)
    amount_quoted = models.PositiveIntegerField(blank=True,null=True)
    authorization_number = models.CharField(max_length=1000)
    caller_name = models.CharField(max_length=200)
    caller_number = models.CharField(max_length=50)
    caller_company = models.CharField(max_length=200)
    call_received_time = models.TimeField()
    time_call_posted_to_crew_on_whatsapp = models.TimeField()
    crew_operational_status = models.CharField(max_length=200,choices=CREW_OPERATIONAL_STATUS)
    how_many_units_dispatched = models.CharField(max_length=50,choices=HOW_MANY_UNITS_DISPATCHED)
    
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class DispatchIncidentCrewAndVehicle(models.Model):

    ASSIGNED_UNIT = [
        ('SDO1','SDO1'),
        ('L01','L01'),
        ('RV03','RV03'),
        ('TP07','TP07'),
        ('TP09','TP09'),
        ('TP08','TP08'),
        ('RV01','RV01'),
        ('TP02','TP02'),
        ('TP05','TP05'),
        ('TP03','TP03'),
        ('RM01','RM01'),
        ('TP11','TP11'),
        ('TP10','TP10'),
    ]

    VEHICLE = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]

    LOC = [
        ('Patient Transport','Patient Transport'),
        ('Basic Life Support','Basic Life Support'),
        ('Intermediate Life Support','Intermediate Life Support'),
        ('Advanced Life Support','Advanced Life Support'),
        ('Mobile ICU','Mobile ICU'),
    ]

    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    assigned_unit = models.CharField(max_length=100,choices=ASSIGNED_UNIT)
    vehicle_total = models.CharField(max_length=50,choices=VEHICLE)
    unit_reg = models.CharField(max_length=30,default='BH 17WM GP')
    senior = models.ForeignKey(Senior,on_delete=SET_NULL,null=True)
    assist01 = models.ForeignKey(Assist01,on_delete=SET_NULL,null=True)
    assist02 = models.ForeignKey(Assist02,on_delete=SET_NULL,null=True)
    loc = models.CharField(max_length=200,choices=LOC)


class DispatchIncidentServiceNotes(models.Model):
    SERVICE_NOTES = [
        ('RESPONSE DELAY','RESPONSE DELAY'),
        ('ON SCENE DELAY','ON SCENE DELAY'),
        ('TRANSPORTING NOTES','TRANSPORTING NOTES'),
        ('HANDOVER DELAY','HANDOVER DELAY'),
        ('SPECIAL RECORD','SPECIAL RECORD'),
    ]
    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    service_notes = models.CharField(max_length=100,choices=SERVICE_NOTES)
    scribe = models.ForeignKey(Scribe,on_delete=SET_NULL,blank=True,null=True)
    service_note_time = models.TimeField(blank=True,null=True)
    service_note_description = models.TextField(blank=True,null=True)


class DispatchIncidentLocationDetails(models.Model):

    ASSIGNED_UNIT = [
        ('SDO1','SDO1'),
        ('L01','L01'),
        ('RV03','RV03'),
        ('TP07','TP07'),
        ('TP09','TP09'),
        ('TP08','TP08'),
        ('RV01','RV01'),
        ('TP02','TP02'),
        ('TP05','TP05'),
        ('TP03','TP03'),
        ('RM01','RM01'),
        ('TP11','TP11'),
        ('TP10','TP10'),
    ]

    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    unit = models.CharField(blank=True,null=True,max_length=200,choices=ASSIGNED_UNIT)
    responding_address = models.CharField(max_length=100,blank=True,null=True)
    scene_address = models.CharField(max_length=100,blank=True,null=True)
    facility_address = models.CharField(max_length=100,blank=True,null=True)
    end_address = models.CharField(max_length=100,blank=True,null=True)


# travel details
class Vehicles_count_with_info_for_ambulance_request(models.Model):
    ASSIGNED_UNIT = [
        ('SDO1','SDO1'),
        ('L01','L01'),
        ('RV03','RV03'),
        ('TP07','TP07'),
        ('TP09','TP09'),
        ('TP08','TP08'),
        ('RV01','RV01'),
        ('TP02','TP02'),
        ('TP05','TP05'),
        ('TP03','TP03'),
        ('RM01','RM01'),
        ('TP11','TP11'),
        ('TP10','TP10'),
    ]
    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    unit = models.CharField(blank=True,null=True,max_length=200,choices=ASSIGNED_UNIT)
    vehicle_no = models.CharField(max_length=40,blank=True,null=True)
    responding = models.TimeField(blank=True,null=True)
    odo01 = models.PositiveIntegerField(null=True)
    on_scene = models.TimeField(null=True)
    odo2 = models.PositiveIntegerField(null=True)
    depart_scene = models.TimeField(null=True)
    arrive_fac = models.TimeField(null=True)
    odo3 = models.PositiveIntegerField(null=True)
    hand_over = models.TimeField(null=True)
    depart = models.TimeField(null=True)
    end_standing_free = models.TimeField(null=True)
    odo04 = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.parent.id)


class DispatchIncidentPatientInformation(models.Model):

    PATIENT = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),
        ('G','G'),
        ('H','H'),
        ('I','I'),
        ('J','J'),
        ('K','K'),
        ('L','L'),
        ('M','M'),
        ('N','N'),
        ('O','O'),
        ('P','P'),
        ('Q','Q'),
        ('R','R'),
        ('S','S'),
        ('T','T'),
        ('U','U'),
        ('V','V'),
        ('w','W'),
        ('X','X'),
        ('Y','Y'),
        ('Z','Z'),
    ]

    P_PRIORITY = [
        ('P1','P1'),
        ('P2','P2'),
        ('P3','P3'),
        ('P4','P4'),
        ('RHTT','RHTT'),
    ]

    P_LEVEL_OF_CARE = [
        ('BLS','BLS'),
        ('ILS','ILS'),
        ('ALS','ALS'),
        ('MICU','MICU'),
        ('DOA','DOA'),
    ]

    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    patient = models.CharField(max_length=50,choices=PATIENT)
    p_priority = models.CharField(max_length=100,blank=True,null=True,choices=P_PRIORITY)
    p_lvl_of_care = models.CharField(max_length=100,blank=True,null=True,choices=P_LEVEL_OF_CARE)
    p_name = models.CharField(max_length=50,blank=True,null=True)
    p_medical_aid_plan_option = models.CharField(max_length=50,blank=True,null=True)
    p_medical_aid = models.CharField(max_length=50,blank=True,null=True)


class DispatchIncidentPhotos(models.Model):
    ITEM = [
        ('Other Document','Other Document'),
        ('Scene Photo','Scene Photo'),
        ('Unknown Person','Unknown Person'),
        ('Other','Other')
    ]
    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    photos_and_other_choices = models.CharField(max_length=50,blank=True,null=True,choices=ITEM)
    photo = models.FileField(upload_to='Ambulance',blank=True,null=True)
    document = models.FileField(upload_to='Ambulance',blank=True,null=True)

class DispatchIncidentNameOfDispatcher(models.Model):
    dispatcher_name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dispatcher_name

class DispatchIncidentDispatcherCertification(models.Model):

    WAS_THE_CALL_HANDED_OVER = [
        ('YES','YES'),
        ('NO','NO'),
    ]

    parent = models.ForeignKey(AmbulanceModel,on_delete=models.CASCADE,blank=True,null=True)
    senior_practitioner_csn = models.CharField(max_length=50,blank=True,null=True)
    name_of_dispatcher = models.ForeignKey(DispatchIncidentNameOfDispatcher,blank=True,null=True,on_delete=SET_NULL,related_name='dispatcher')
    other_dispatcher = models.ForeignKey(DispatchIncidentNameOfDispatcher,blank=True,null=True,on_delete=SET_NULL,related_name='other_dispatcher')
    was_the_call_handed_over_to_another_dispatcher = models.CharField(max_length=20,blank=True,null=True,choices=WAS_THE_CALL_HANDED_OVER)
    dispatch_special_notes = models.TextField(blank=True,null=True)
    signature = models.FileField(upload_to='Signature',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

# dispatch incident ends
class AmbulanceRequestModel(models.Model):
    pass


class AmbulanceNoti(models.Model):
    noti_for = models.ForeignKey(AmbulanceRequestModel,on_delete=models.CASCADE)
    text = models.CharField(max_length=50,default='Ambulance request')

    accepted_text = models.CharField(max_length=50,default='Your request was accepted')
    is_accepted = models.BooleanField(default=False)

    is_declined = models.BooleanField(default=False)
    declined_text = models.CharField(max_length=50,default='Your request was cancelled')

    mark_read_admin = models.BooleanField(default=False)
    mark_read_user = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=AmbulanceRequestModel)
def create_ambulance_noti(sender, instance=None, created=False, **kwargs):
    if created:
        AmbulanceNoti.objects.create(noti_for=instance)


class PanicNoti(models.Model):
    panic = models.ForeignKey(
        Panic, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=100, default='has sent a panic request')
    is_seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.panic.panic_sender.first_name


class PropertyTools(models.Model):
    CONDITION = [
        ('NEW', 'NEW'),
        ('USED', 'USED'),
    ]
    STATUS = [
        ('PAID', 'PAID'),
        ('DUE', 'DUE'),
    ]
    TYPE = [
        ('FURNITURE', 'FURNITURE'),
        ('HARDWARE', 'HARDWARE'),
        ('ELECTRICAL', 'ELECTRICAL'),
        ('SOFTWARE', 'SOFTWARE'),
        ('AMBULANCE', 'AMBULANCE'),
        ('OXYGEN CYLINDER', 'OXYGEN CYLINDER'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    to_user = models.CharField(max_length=80, blank=True, null=True)
    to_user_mobile = models.CharField(max_length=80, blank=True, null=True)
    property_type = models.CharField(
        max_length=30, blank=True, null=True, choices=TYPE)
    equipement_name = models.CharField(max_length=40, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=300, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    condition = models.CharField(
        max_length=30, blank=True, null=True, choices=CONDITION)
    status = models.CharField(
        max_length=30, blank=True, null=True, choices=STATUS)
    invoice_id = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    vat = models.IntegerField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.invoice_id


class FAQ(models.Model):
    author = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    img = models.ImageField(upload_to='FAQ', blank=True, null=True)
    ques = models.CharField(max_length=500, blank=True, null=True)
    ans = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ques


class CaseNote(models.Model):
    creator = models.ForeignKey(User,on_delete=SET_NULL,blank=True, null=True)
    case_panic = models.ForeignKey(Panic,on_delete=models.CASCADE,blank=True, null=True)
    case_no = models.TextField(blank=True, null=True)
    case_note = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.case_no)


@receiver(post_save, sender=Panic)
def create_panic_noti(sender, instance=None, created=False, **kwargs):
    if created:
        PanicNoti.objects.create(panic=instance)


class HospitalTransferModel(models.Model):
    transfer_type = [
        ('Emergency', 'Emergency'),
        ('Normally', 'Normally')
    ]

    priority_type = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transfer_speed = models.CharField(max_length=100, choices=transfer_type, blank=False, null=False, default='Emergency')
    reason = models.CharField(max_length=100, blank=False, null=False)
    priority = models.CharField(max_length=100, choices=priority_type, blank=True, null=True, default='Low')
    current_hos = models.CharField(max_length=200, blank=False, null=False)
    current_add = models.CharField(max_length=200, blank=False, null=False)
    target_hos = models.CharField(max_length=200, blank=False, null=False)
    target_add = models.CharField(max_length=200, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Transferred to {self.target_hos}"


class HospitalTransferNoti(models.Model):
    noti_for = models.ForeignKey(HospitalTransferModel,on_delete=models.CASCADE)
    text = models.CharField(max_length=50,default='Hospital transfer request')

    accepted_text = models.CharField(max_length=50,default='Your request was accepted')
    is_accepted = models.BooleanField(default=False)

    is_declined = models.BooleanField(default=False)
    declined_text = models.CharField(max_length=50,default='Your request was cancelled')

    mark_read_admin = models.BooleanField(default=False)
    mark_read_user = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=HospitalTransferModel)
def create_h_transfer_noti(sender, instance=None, created=False, **kwargs):
    if created:
        HospitalTransferNoti.objects.create(noti_for=instance)


class Blog(models.Model):
    author = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True,null=True)
    post = models.TextField()
    image = models.FileField(upload_to='Blogs',blank=True,null=True)
    publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class FormBuilder(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    json = models.TextField(blank=True,null=True)


class FormData(models.Model):
    date = models.DateField(auto_now=True)
    form = models.ForeignKey(FormBuilder,on_delete=models.CASCADE)
    data = models.TextField()



class CallSign(models.Model):
    CALLSIGN = [
        ('L02','L02'),
        ('SDO1','SDO1'),
        ('L01','L01'),
        ('RV03','RV03'),
        ('TP07','TP07'),
        ('TP09','TP09'),
        ('TP08','TP08'),
        ('RV01','RV01'),
        ('TP02','TP02'),
        ('TP05','TP05'),
        ('TP03','TP03'),
        ('RM01','RM01'),
        ('TP11','TP11'),
        ('TP10','TP10'),
    ]
    call_sign = models.CharField(choices=CALLSIGN,max_length=10)
    registration = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    vin = models.CharField(max_length=100)
    yofr = models.CharField(max_length=100)
    petrolium = models.CharField(max_length=100)
    service_interval = models.CharField(max_length=100)
    dot = models.CharField(max_length=100)

    def __str__(self):
        return self.call_sign



class VehicleProfile(models.Model):
    PERFORMANCE=[
        ('Yes','Yes'),
        ('No','No')
    ]
    THIRDPARTY=[
         ('Yes','Yes'),
        ('No','No'),
        ('Not Applicable','Not Applicable')
    ]
    CONTINGENTLIABILITY=[
         ('Yes','Yes'),
        ('No','No'),
        ('Not Applicable','Not Applicable')
    ]
    ROADASSISTANCE=[
         ('Yes','Yes'),
        ('No','No'),
        ('Not Applicable','Not Applicable')
    ]
    PASSENGERLIABILITY=[
         ('Yes','Yes'),
        ('No','No'),
        ('Not Applicable','Not Applicable')
    ]
    PASSENGERLIABILITYMaxPerPerson=[
        ('R1 000 000.00 (One Million Rand,alone)','R1 000 000.00 (One Million Rand,alone)'),
        ('R3 000 000.00 (One Million Rand,alone)','R3 000 000.00 (One Million Rand,alone)'),
        ('R5 000 000.00 (One Million Rand,alone)','R5 000 000.00 (One Million Rand,alone)'),
        ('R10 000 000.00 (One Million Rand,alone)','R10 000 000.00 (One Million Rand,alone)'),
        ('Not Applicable/Not Covered','Not Applicable/Not Covered')
    ]
    call_sign = models.ForeignKey(CallSign,on_delete=models.CASCADE)
    performance = models.CharField(choices=PERFORMANCE,max_length=10)
    odo = models.IntegerField()
    company = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    cover = models.CharField(max_length=100)
    thirdparty_cover = models.CharField(choices=THIRDPARTY,max_length=100)
    passenger_liability = models.CharField(choices=PASSENGERLIABILITY,max_length=500)
    passenger_liabilitycover_maxpp = models.CharField(choices=PASSENGERLIABILITYMaxPerPerson,max_length=500)
    contingent_liability = models.CharField(choices=CONTINGENTLIABILITY,max_length=100)
    road_assistance = models.CharField(choices=ROADASSISTANCE,max_length=100)
    assignedbase_address = models.TextField()
    assignedbase_gps = models.TextField()
    driving_licensingcode = models.TextField()
    classification_type = models.TextField()
    classification_levelofcare = models.TextField()
    subclassification_special = models.CharField(max_length=100)
    maximum_crewcount = models.IntegerField()
    maximum_patientcount = models.IntegerField()
    mifi = models.CharField(max_length=100)
    bst = models.BooleanField(default=False)
    ht = models.BooleanField(default=False)
    lfbr = models.BooleanField(default=False)
    cp = models.BooleanField(default=False)
    none = models.BooleanField(default=False)
    dcro = models.BooleanField(default=False)
    dcrodc = models.BooleanField(default=False)
    dcbv = models.BooleanField(default=False)
    icdc = models.BooleanField(default=False)
    icpc = models.BooleanField(default=False)
    none_installed = models.BooleanField(default=False)
    navigation_system = models.CharField(max_length=100)
    tracking_recovery_system = models.CharField(max_length=100)
    company_installation_cn = models.CharField(max_length=100)
    transponder_installation_date = models.DateField()
    pcd = models.DateField()
    signature = models.ImageField(upload_to='signature',blank=True,null=True)



class DateOfPicture(models.Model):
    vehicle_profile = models.ForeignKey(VehicleProfile,on_delete=models.CASCADE)
    date_of_image = models.DateField()
    description = models.TextField()
    photograph = models.ImageField(upload_to='dateofpicture/')


class Category(models.Model):
    CATEGORY = [
        ('Distress Signaling','Distress Signaling'),
        ('Patient Treatment','Patient Treatment'),
        ('Scene Safety','Scene Safety'),
        ('Vehicle Safety','Vehicle Safety'),
        ('Other','Other')
    ]
    vehicle_profile = models.ForeignKey(VehicleProfile,on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY,max_length=100)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField()



class FleetPreventiveManagement(models.Model):
    SECONDARY_BATTERY = [
        ('Yes','Yes'),
        ('No','No')
    ]
    SECONDARY_INVERTER= [
        ('Yes','Yes'),
        ('No','No')
    ]
    date = models.DateField()
    call_sign = models.ForeignKey(CallSign,on_delete=models.CASCADE)
    location = models.TextField()
    expiry = models.DateField()
    current_odo = models.IntegerField(blank=True,null=True)
    secondary_battery = models.CharField(choices=SECONDARY_BATTERY,max_length=100,blank=True,null=True)
    secondary_inverter = models.CharField(choices=SECONDARY_INVERTER,max_length=100,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    signature = models.ImageField(upload_to='technician/',blank=True,null=True)
    certification_date = models.DateField(blank=True,null=True)
    certification_time = models.TimeField(blank=True,null=True)


class Battery(models.Model):
    STATUS = [
        ('Good','Good'),
        ('Repair Required','Repair Required'),
        ('Damaged/Replace','Damaged/Replace'),
        ('N/A','N/A')
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)


class Inverter(models.Model):
    STATUS = [
        ('Good','Good'),
        ('Repair Required','Repair Required'),
        ('Damaged/Replace','Damaged/Replace'),
        ('N/A','N/A')
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)


class BodyBranding(models.Model):
    STATUS = [
        ('Good','Good'),
        ('Damaged','Damaged'),
        ('Dents','Dents'),
        ('Scratches','Scratches'),
        ('Repair Required','Repair Required'),
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)


class FluidInspection(models.Model):
    STATUS = [
        ('1/4','1/4'),
        ('2/4','2/4'),
        ('3/4','3/4'),
        ('4/4','4/4'),
        ('Good','Good'),
        ('Master Cylinder Leakage','Master Cylinder Leakage'),
        ('Front LT Leak','Front LT Leak'),
        ('Front RT Leak','Front RT Leak'),
        ('Back LT Leak','Back LT Leak'),
        ('Back RT Leak','Back RT Leak'),
        ('Repair Required','Repair Required'),
        ('N/A','N/A')
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)


class InternalSystem(models.Model):
    STATUS = [
        ('Good','Good'),
        ('Repair Required','Repair Required'),
        ('Damaged/Replace','Damaged/Replace'),
        ('N/A','N/A')
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)


class Light(models.Model):
    STATUS = [
        ('Good','Good'),
        ('Repair Required','Repair Required'),
        ('Damaged/Replace','Damaged/Replace'),
        ('N/A','N/A')
    ]
    fleet_preventive = models.ForeignKey(FleetPreventiveManagement,on_delete=models.CASCADE)
    elements = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)
    notes = models.TextField()
    photo = models.ImageField(upload_to='fleet/',blank=True,null=True)