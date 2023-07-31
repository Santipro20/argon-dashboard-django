# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from jsonfield import JSONField

# Create your models here.

class AccessTokens(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    value = models.CharField(max_length=255)
    user_id = models.IntegerField()
    expiration = models.DateTimeField()
    refresh_token = models.CharField(max_length=255)
    refresh_token_expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'access_tokens'

class AreaTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    coordinates = models.TextField(blank=True, null=True)  # This field type is a guess.
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    polygon = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_admin = models.BooleanField(blank=True, null=True)
    multipolygon = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'area_team'


class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    zipcodes = JSONField(blank=True, null=True)
    auto_assign = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cities'


class Codes(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    value = models.CharField(max_length=255)
    redirect_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    user_id = models.IntegerField()
    expiration = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'codes'



class Courses(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    devis = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    merchant = models.ForeignKey('Merchants', models.PROTECT, blank=True, null=True)
    updated_by = models.ForeignKey('Users', models.PROTECT, db_column='updated_by', blank=True, null=True,  related_name='Courses_updated_by')
    created_by = models.ForeignKey('Users', models.PROTECT, db_column='created_by', blank=True, null=True, related_name='Courses_created_by')
    package_types = models.ForeignKey('PackageTypes', models.PROTECT, blank=True, null=True)
    food = models.CharField(max_length=255, blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    coursier = models.ForeignKey('Coursier', models.PROTECT, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    order_admin = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    order_0 = models.ForeignKey('Orders', models.PROTECT, db_column='order_id', blank=True, null=True)  # Field renamed because of name conflict.
    insurance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    nb_bon = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rejected_teams = JSONField(blank=True, null=True)
    pallet_is_one_entity = models.BooleanField(blank=True, null=True)
    complete_to_validate = models.BooleanField(blank=True, null=True)
    attribution_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class Coursier(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.PROTECT, blank=True, null=True)
    availability = models.BooleanField(blank=True, null=True)
    availability_not_show = models.BooleanField(blank=True, null=True)
    vehicle_type = models.ForeignKey('VehicleTypes', models.PROTECT, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursier'


class DefaultPackage(models.Model):
    id = models.IntegerField(primary_key=True)
    package = models.ForeignKey('Packages', models.PROTECT)
    merchant = models.ForeignKey('Merchants', models.PROTECT, blank=True, null=True)
    recipient = models.ForeignKey('Recipients', models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_package'


class DeliveryStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_status'

class Dispatchers(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.PROTECT, blank=True, null=True)
    bank_id = models.CharField(db_column='bank_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matriculation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispatchers'

class Geolocation(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    task = models.ForeignKey('Tasks', models.PROTECT)
    coursier = models.ForeignKey(Coursier, models.PROTECT)
    coordinates = models.TextField(blank=True, null=True)  # This field type is a guess.
    timestamp = models.DateTimeField()
    coordinates_extra = models.TextField()  # This field type is a guess.
    is_moving = models.BooleanField()
    event = models.CharField(max_length=255, blank=True, null=True)
    odometer = models.FloatField()
    activity = models.TextField()  # This field type is a guess.
    battery = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'geolocation'


class Groups(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    locale = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class HubUsers(models.Model):
    id = models.IntegerField(primary_key=True)
    hub = models.ForeignKey('Hubs', models.PROTECT, blank=True, null=True)
    user = models.ForeignKey('Users', models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hub_users'


class Hubs(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hubs'


class Invoice(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    number = models.IntegerField(blank=True, null=True)
    merchant = models.ForeignKey('Merchants', models.PROTECT, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    validate_by = models.ForeignKey('Users', models.PROTECT, db_column='validate_by', blank=True, null=True)
    validate_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    payment_deadline = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(Dispatchers, models.PROTECT, db_column='created_by', blank=True, null=True,  related_name='Invoice_created_by')
    created_by_admin = models.ForeignKey('Users',models.PROTECT, db_column='created_by_admin', blank=True, null=True, related_name='Invoice_created_by_admin')

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceCourses(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(Courses, models.PROTECT, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_courses'


class InvoicePdfs(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=1000)
    merchant = models.ForeignKey('Merchants', models.PROTECT, blank=True, null=True)
    dispatcher = models.ForeignKey(Dispatchers, models.PROTECT, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.PROTECT, blank=True, null=True)
    loid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_pdfs'


class Merchants(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.PROTECT, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    is_contractor = models.BooleanField(blank=True, null=True)
    package_types = models.ForeignKey('PackageTypes', models.PROTECT, blank=True, null=True)
    food = models.CharField(max_length=255, blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    matriculation = models.CharField(max_length=255, blank=True, null=True)
    taxe = models.CharField(max_length=255, blank=True, null=True)
    bank_id = models.CharField(db_column='bank_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    payment_deadline = models.IntegerField(blank=True, null=True)
    created_by_admin = models.BooleanField(blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    group_0 = models.ForeignKey(Groups, models.PROTECT, db_column='group_id', blank=True, null=True)  # Field renamed because of name conflict.
    price_bon = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pallet_is_one_entity = models.BooleanField(blank=True, null=True)
    complete_to_validate = models.BooleanField(blank=True, null=True)
    is_price_visible = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'merchants'


class Migrations(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)
    migration_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migrations'


class MigrationsLock(models.Model):
    index = models.AutoField(primary_key=True)
    is_locked = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'migrations_lock'


class Orders(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    delivery_status = models.ForeignKey(DeliveryStatus, models.PROTECT)
    hub = models.ForeignKey(Hubs, models.PROTECT, blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class PackageKinds(models.Model):
    id = models.IntegerField(primary_key=True)
    kind = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_kinds'


class PackageTypeReceiver(models.Model):
    id = models.IntegerField(primary_key=True)
    package_type = models.ForeignKey('PackageTypes', models.PROTECT)
    receiver_merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    receiver_recipient = models.ForeignKey('Recipients', models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_type_receiver'


class PackageTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    icon_fa = JSONField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_types'


class PackageTypesTeam(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    package_types = models.ForeignKey(PackageTypes, models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_types_team'


class Packages(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    weight = models.FloatField(blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    kind = models.ForeignKey(PackageKinds,models.PROTECT, blank=True, null=True)
    task = models.ForeignKey('Tasks', models.PROTECT, blank=True, null=True,  related_name='Packages_task')
    delivery_status = models.ForeignKey(DeliveryStatus, models.PROTECT)
    order = models.ForeignKey(Orders, models.PROTECT, blank=True, null=True)
    pallet = models.ForeignKey('Pallets', models.PROTECT, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    pickup = models.ForeignKey('Tasks', models.PROTECT, blank=True, null=True)
    delivery = models.ForeignKey('Tasks',models.PROTECT, blank=True, null=True,  related_name='Packages_delivery')
    package_type = models.ForeignKey(PackageTypes, models.PROTECT, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    declared_value = models.FloatField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    externaldata = JSONField(db_column='externalData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'packages'



class Pallets(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(Orders,models.PROTECT, blank=True, null=True)
    delivery_status = models.ForeignKey(DeliveryStatus, models.PROTECT)
    uid = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pallets'


class Pricing(models.Model):
    id = models.IntegerField(primary_key=True)
    team = models.ForeignKey('Teams', models.PROTECT, blank=True, null=True)
    isadmin = models.BooleanField(db_column='isAdmin', blank=True, null=True)  # Field name made lowercase.
    base = models.FloatField(blank=True, null=True)
    overcost = JSONField(blank=True, null=True)
    discount = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pricing'


class ReceiptPdfs(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=1000)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    recipient = models.ForeignKey('Recipients', models.PROTECT, blank=True, null=True)
    course = models.ForeignKey(Courses, models.PROTECT, blank=True, null=True)
    loid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receipt_pdfs'


class Recipients(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey('Teams',models.PROTECT, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('Users', models.PROTECT, db_column='created_by', blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    client_number = models.CharField(max_length=255, blank=True, null=True)
    sign = models.CharField(max_length=255, blank=True, null=True)
    opening_hours = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipients'



class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class Tasks(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    nb_bon = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    order_coursier = models.IntegerField(blank=True, null=True)
    coursier = models.ForeignKey(Coursier, models.PROTECT, blank=True, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    volumn = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sign_filename = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    ready_to_pick_up = models.BooleanField(blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Courses, models.PROTECT, blank=True, null=True)
    history = JSONField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    rate_note = models.TextField(blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    recipient = models.ForeignKey(Recipients, models.PROTECT, blank=True, null=True)
    hub = models.ForeignKey(Hubs, models.PROTECT, blank=True, null=True)
    co2 = JSONField(blank=True, null=True)
    start_interval = models.IntegerField(blank=True, null=True)
    cycling = JSONField(blank=True, null=True)
    driving = JSONField(blank=True, null=True)
    altitudes = JSONField(blank=True, null=True)
    total_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_volumn = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_packages = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class Teams(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    team_id = models.CharField(db_column='team_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    dispatch_rate = models.IntegerField(blank=True, null=True)
    zipcode = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'


class UsGaz(models.Model):
    id = models.IntegerField(primary_key=True)
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_gaz'


class UsLex(models.Model):
    id = models.IntegerField(primary_key=True)
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_lex'


class UsRules(models.Model):
    id = models.IntegerField(primary_key=True)
    rule = models.TextField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_rules'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255)
    renew_pwd = models.BooleanField()
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(Teams, models.PROTECT, blank=True, null=True)
    address = JSONField(blank=True, null=True)
    new_user = models.BooleanField()
    picture_name = models.CharField(max_length=255, blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.PROTECT, blank=True, null=True)
    push_token = models.TextField(blank=True, null=True)
    push_os = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class VehicleTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(Teams, models.PROTECT)
    volumn = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_types'


class ZonePricing(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    zone = models.ForeignKey(AreaTeam, models.PROTECT, blank=True, null=True)
    pricing = JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zone_pricing'

class PolygonFrance(models.Model):
    id = models.AutoField(primary_key=True)
    code_postal_1 = models.TextField(blank=True, null=True)
    geometry = JSONField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'polygon_france'



     