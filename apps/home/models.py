# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccessTokens(models.Model):
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


class AddDf(models.Model):
    v1 = models.TextField(db_column='V1', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'add_df'


class Addr(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fromhn = models.CharField(max_length=12, blank=True, null=True)
    tohn = models.CharField(max_length=12, blank=True, null=True)
    side = models.CharField(max_length=1, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    plus4 = models.CharField(max_length=4, blank=True, null=True)
    fromtyp = models.CharField(max_length=1, blank=True, null=True)
    totyp = models.CharField(max_length=1, blank=True, null=True)
    fromarmid = models.IntegerField(blank=True, null=True)
    toarmid = models.IntegerField(blank=True, null=True)
    arid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addr'


class Addrfeat(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    statefp = models.CharField(max_length=2)
    aridl = models.CharField(max_length=22, blank=True, null=True)
    aridr = models.CharField(max_length=22, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    lfromhn = models.CharField(max_length=12, blank=True, null=True)
    ltohn = models.CharField(max_length=12, blank=True, null=True)
    rfromhn = models.CharField(max_length=12, blank=True, null=True)
    rtohn = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    edge_mtfcc = models.CharField(max_length=5, blank=True, null=True)
    parityl = models.CharField(max_length=1, blank=True, null=True)
    parityr = models.CharField(max_length=1, blank=True, null=True)
    plus4l = models.CharField(max_length=4, blank=True, null=True)
    plus4r = models.CharField(max_length=4, blank=True, null=True)
    lfromtyp = models.CharField(max_length=1, blank=True, null=True)
    ltotyp = models.CharField(max_length=1, blank=True, null=True)
    rfromtyp = models.CharField(max_length=1, blank=True, null=True)
    rtotyp = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'addrfeat'


class AreaTeam(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    coordinates = models.TextField(blank=True, null=True)  # This field type is a guess.
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    polygon = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_admin = models.BooleanField(blank=True, null=True)
    multipolygon = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'area_team'


class Bg(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    bg_id = models.CharField(primary_key=True, max_length=12)
    namelsad = models.CharField(max_length=13, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bg'


class Cities(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    zipcodes = models.JSONField(blank=True, null=True)
    auto_assign = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cities'


class Codes(models.Model):
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


class County(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    countyns = models.CharField(max_length=8, blank=True, null=True)
    cntyidfp = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'county'


class CountyLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'county_lookup'
        unique_together = (('st_code', 'co_code'),)


class CountysubLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countysub_lookup'
        unique_together = (('st_code', 'co_code', 'cs_code'),)


class Courses(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    devis = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey('Merchants', models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='updated_by', blank=True, null=True)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    package_types = models.ForeignKey('PackageTypes', models.DO_NOTHING, blank=True, null=True)
    food = models.CharField(max_length=255, blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    coursier = models.ForeignKey('Coursier', models.DO_NOTHING, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    order_admin = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    order_0 = models.ForeignKey('Orders', models.DO_NOTHING, db_column='order_id', blank=True, null=True)  # Field renamed because of name conflict.
    insurance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    nb_bon = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    rejected_teams = models.JSONField(blank=True, null=True)
    pallet_is_one_entity = models.BooleanField(blank=True, null=True)
    complete_to_validate = models.BooleanField(blank=True, null=True)
    attribution_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'courses'


class Coursier(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    availability = models.BooleanField(blank=True, null=True)
    availability_not_show = models.BooleanField(blank=True, null=True)
    vehicle_type = models.ForeignKey('VehicleTypes', models.DO_NOTHING, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coursier'


class Cousub(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    cousubns = models.CharField(max_length=8, blank=True, null=True)
    cosbidfp = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    awater = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cousub'


class CrmShop(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crm_shop'


class DataFinalCafe(models.Model):
    id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    devis = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    team_id = models.IntegerField(blank=True, null=True)
    merchant_id = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    package_types_id = models.IntegerField(blank=True, null=True)
    food = models.TextField(blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    coursier_id = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    order_admin = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    identifier = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    insurance = models.FloatField(blank=True, null=True)
    nb_bon = models.FloatField(blank=True, null=True)
    rejected_teams = models.TextField(blank=True, null=True)
    id_1 = models.IntegerField(db_column='id.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    created_at_1 = models.DateTimeField(db_column='created_at.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    updated_at_1 = models.DateTimeField(db_column='updated_at.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    company = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    nb_bon_1 = models.TextField(db_column='nb_bon.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    notes = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    state_1 = models.IntegerField(db_column='state.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    email = models.TextField(blank=True, null=True)
    order_1 = models.IntegerField(db_column='order.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    order_coursier = models.IntegerField(blank=True, null=True)
    coursier_id_1 = models.IntegerField(db_column='coursier_id.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    weight = models.FloatField(blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    sign_filename = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    ready_to_pick_up = models.BooleanField(blank=True, null=True)
    uid = models.TextField(blank=True, null=True)
    course_id = models.IntegerField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    rate_note = models.TextField(blank=True, null=True)
    merchant_id_1 = models.IntegerField(db_column='merchant_id.1', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    recipient_id = models.IntegerField(blank=True, null=True)
    hub_id = models.IntegerField(blank=True, null=True)
    add = models.TextField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    nc_depart = models.TextField(blank=True, null=True)
    nc = models.TextField(blank=True, null=True)
    m = models.TextField(db_column='M', blank=True, null=True)  # Field name made lowercase.
    s = models.TextField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    m_b = models.TextField(db_column='M_b', blank=True, null=True)  # Field name made lowercase.
    s_b = models.TextField(db_column='S_b', blank=True, null=True)  # Field name made lowercase.
    task_id_done = models.IntegerField(blank=True, null=True)
    km = models.FloatField(blank=True, null=True)
    two = models.FloatField(blank=True, null=True)
    three = models.FloatField(blank=True, null=True)
    diff_livra = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_final_cafe'


class DataSfASummary(models.Model):
    a = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_sf_a_summary'


class DataSfASummaryZ1(models.Model):
    a = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_sf_a_summary_z_1'


class DataSfASummaryZ2(models.Model):
    a = models.TextField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_sf_a_summary_z_2'


class DefaultPackage(models.Model):
    package = models.ForeignKey('Packages', models.DO_NOTHING)
    merchant = models.ForeignKey('Merchants', models.DO_NOTHING, blank=True, null=True)
    recipient = models.ForeignKey('Recipients', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'default_package'


class DeliveryStatus(models.Model):
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'delivery_status'


class DirectionLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direction_lookup'


class Dispatchers(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    bank_id = models.CharField(db_column='bank_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matriculation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispatchers'


class Edges(models.Model):
    gid = models.AutoField(primary_key=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    tfidl = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tfidr = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    smid = models.CharField(max_length=22, blank=True, null=True)
    lfromadd = models.CharField(max_length=12, blank=True, null=True)
    ltoadd = models.CharField(max_length=12, blank=True, null=True)
    rfromadd = models.CharField(max_length=12, blank=True, null=True)
    rtoadd = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    featcat = models.CharField(max_length=1, blank=True, null=True)
    hydroflg = models.CharField(max_length=1, blank=True, null=True)
    railflg = models.CharField(max_length=1, blank=True, null=True)
    roadflg = models.CharField(max_length=1, blank=True, null=True)
    olfflg = models.CharField(max_length=1, blank=True, null=True)
    passflg = models.CharField(max_length=1, blank=True, null=True)
    divroad = models.CharField(max_length=1, blank=True, null=True)
    exttyp = models.CharField(max_length=1, blank=True, null=True)
    ttyp = models.CharField(max_length=1, blank=True, null=True)
    deckedroad = models.CharField(max_length=1, blank=True, null=True)
    artpath = models.CharField(max_length=1, blank=True, null=True)
    persist = models.CharField(max_length=1, blank=True, null=True)
    gcseflg = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    tnidf = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tnidt = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'edges'


class Faces(models.Model):
    gid = models.AutoField(primary_key=True)
    tfid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    statefp00 = models.CharField(max_length=2, blank=True, null=True)
    countyfp00 = models.CharField(max_length=3, blank=True, null=True)
    tractce00 = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce00 = models.CharField(max_length=1, blank=True, null=True)
    blockce00 = models.CharField(max_length=4, blank=True, null=True)
    cousubfp00 = models.CharField(max_length=5, blank=True, null=True)
    submcdfp00 = models.CharField(max_length=5, blank=True, null=True)
    conctyfp00 = models.CharField(max_length=5, blank=True, null=True)
    placefp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhce00 = models.CharField(max_length=4, blank=True, null=True)
    comptyp00 = models.CharField(max_length=1, blank=True, null=True)
    trsubfp00 = models.CharField(max_length=5, blank=True, null=True)
    trsubce00 = models.CharField(max_length=3, blank=True, null=True)
    anrcfp00 = models.CharField(max_length=5, blank=True, null=True)
    elsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    scsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    unsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    uace00 = models.CharField(max_length=5, blank=True, null=True)
    cd108fp = models.CharField(max_length=2, blank=True, null=True)
    sldust00 = models.CharField(max_length=3, blank=True, null=True)
    sldlst00 = models.CharField(max_length=3, blank=True, null=True)
    vtdst00 = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce00 = models.CharField(max_length=5, blank=True, null=True)
    tazce00 = models.CharField(max_length=6, blank=True, null=True)
    ugace00 = models.CharField(max_length=5, blank=True, null=True)
    puma5ce00 = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    submcdfp = models.CharField(max_length=5, blank=True, null=True)
    conctyfp = models.CharField(max_length=5, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp = models.CharField(max_length=5, blank=True, null=True)
    aiannhce = models.CharField(max_length=4, blank=True, null=True)
    comptyp = models.CharField(max_length=1, blank=True, null=True)
    trsubfp = models.CharField(max_length=5, blank=True, null=True)
    trsubce = models.CharField(max_length=3, blank=True, null=True)
    anrcfp = models.CharField(max_length=5, blank=True, null=True)
    ttractce = models.CharField(max_length=6, blank=True, null=True)
    tblkgpce = models.CharField(max_length=1, blank=True, null=True)
    elsdlea = models.CharField(max_length=5, blank=True, null=True)
    scsdlea = models.CharField(max_length=5, blank=True, null=True)
    unsdlea = models.CharField(max_length=5, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    cd111fp = models.CharField(max_length=2, blank=True, null=True)
    sldust = models.CharField(max_length=3, blank=True, null=True)
    sldlst = models.CharField(max_length=3, blank=True, null=True)
    vtdst = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce = models.CharField(max_length=5, blank=True, null=True)
    tazce = models.CharField(max_length=6, blank=True, null=True)
    ugace = models.CharField(max_length=5, blank=True, null=True)
    puma5ce = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    lwflag = models.CharField(max_length=1, blank=True, null=True)
    offset = models.CharField(max_length=1, blank=True, null=True)
    atotal = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'faces'


class Featnames(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    predirabrv = models.CharField(max_length=15, blank=True, null=True)
    pretypabrv = models.CharField(max_length=50, blank=True, null=True)
    prequalabr = models.CharField(max_length=15, blank=True, null=True)
    sufdirabrv = models.CharField(max_length=15, blank=True, null=True)
    suftypabrv = models.CharField(max_length=50, blank=True, null=True)
    sufqualabr = models.CharField(max_length=15, blank=True, null=True)
    predir = models.CharField(max_length=2, blank=True, null=True)
    pretyp = models.CharField(max_length=3, blank=True, null=True)
    prequal = models.CharField(max_length=2, blank=True, null=True)
    sufdir = models.CharField(max_length=2, blank=True, null=True)
    suftyp = models.CharField(max_length=3, blank=True, null=True)
    sufqual = models.CharField(max_length=2, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    paflag = models.CharField(max_length=1, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'featnames'


class GeocodeSettings(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings'


class GeocodeSettingsDefault(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings_default'


class Geolocation(models.Model):
    uid = models.CharField(max_length=255)
    task = models.ForeignKey('Tasks', models.DO_NOTHING)
    coursier = models.ForeignKey(Coursier, models.DO_NOTHING)
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
    name = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    locale = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class HubUsers(models.Model):
    hub = models.ForeignKey('Hubs', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hub_users'


class Hubs(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hubs'


class Invoice(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    number = models.IntegerField(blank=True, null=True)
    merchant = models.ForeignKey('Merchants', models.DO_NOTHING, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    validate_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='validate_by', blank=True, null=True)
    validate_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    payment_deadline = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(Dispatchers, models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_by_admin = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by_admin', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceCourses(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(Courses, models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_courses'


class InvoicePdfs(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=1000)
    merchant = models.ForeignKey('Merchants', models.DO_NOTHING, blank=True, null=True)
    dispatcher = models.ForeignKey(Dispatchers, models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, models.DO_NOTHING, blank=True, null=True)
    loid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_pdfs'


class LoaderLookuptables(models.Model):
    process_order = models.IntegerField()
    lookup_name = models.TextField(primary_key=True)
    table_name = models.TextField(blank=True, null=True)
    single_mode = models.BooleanField()
    load = models.BooleanField()
    level_county = models.BooleanField()
    level_state = models.BooleanField()
    level_nation = models.BooleanField()
    post_load_process = models.TextField(blank=True, null=True)
    single_geom_mode = models.BooleanField(blank=True, null=True)
    insert_mode = models.CharField(max_length=1)
    pre_load_process = models.TextField(blank=True, null=True)
    columns_exclude = models.TextField(blank=True, null=True)  # This field type is a guess.
    website_root_override = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_lookuptables'


class LoaderPlatform(models.Model):
    os = models.CharField(primary_key=True, max_length=50)
    declare_sect = models.TextField(blank=True, null=True)
    pgbin = models.TextField(blank=True, null=True)
    wget = models.TextField(blank=True, null=True)
    unzip_command = models.TextField(blank=True, null=True)
    psql = models.TextField(blank=True, null=True)
    path_sep = models.TextField(blank=True, null=True)
    loader = models.TextField(blank=True, null=True)
    environ_set_command = models.TextField(blank=True, null=True)
    county_process_command = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_platform'


class LoaderVariables(models.Model):
    tiger_year = models.CharField(primary_key=True, max_length=4)
    website_root = models.TextField(blank=True, null=True)
    staging_fold = models.TextField(blank=True, null=True)
    data_schema = models.TextField(blank=True, null=True)
    staging_schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_variables'


class Merchants(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    is_contractor = models.BooleanField(blank=True, null=True)
    package_types = models.ForeignKey('PackageTypes', models.DO_NOTHING, blank=True, null=True)
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
    group_0 = models.ForeignKey(Groups, models.DO_NOTHING, db_column='group_id', blank=True, null=True)  # Field renamed because of name conflict.
    price_bon = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pallet_is_one_entity = models.BooleanField(blank=True, null=True)
    complete_to_validate = models.BooleanField(blank=True, null=True)
    is_price_visible = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'merchants'


class Migrations(models.Model):
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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    delivery_status = models.ForeignKey(DeliveryStatus, models.DO_NOTHING)
    hub = models.ForeignKey(Hubs, models.DO_NOTHING, blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class PackageKinds(models.Model):
    kind = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_kinds'


class PackageTypeReceiver(models.Model):
    package_type = models.ForeignKey('PackageTypes', models.DO_NOTHING)
    receiver_merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    receiver_recipient = models.ForeignKey('Recipients', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_type_receiver'


class PackageTypes(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    icon_fa = models.JSONField(blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_types'


class PackageTypesTeam(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    package_types = models.ForeignKey(PackageTypes, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package_types_team'


class Packages(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    weight = models.FloatField(blank=True, null=True)
    volumn = models.FloatField(blank=True, null=True)
    fragile = models.BooleanField(blank=True, null=True)
    kind = models.ForeignKey(PackageKinds, models.DO_NOTHING, blank=True, null=True)
    task = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    delivery_status = models.ForeignKey(DeliveryStatus, models.DO_NOTHING)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    pallet = models.ForeignKey('Pallets', models.DO_NOTHING, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    pickup = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    delivery = models.ForeignKey('Tasks', models.DO_NOTHING, blank=True, null=True)
    package_type = models.ForeignKey(PackageTypes, models.DO_NOTHING, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    declared_value = models.FloatField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    externaldata = models.JSONField(db_column='externalData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'packages'


class PagcGaz(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_gaz'


class PagcLex(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_lex'


class PagcRules(models.Model):
    rule = models.TextField(blank=True, null=True)
    is_custom = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagc_rules'


class Pallets(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    delivery_status = models.ForeignKey(DeliveryStatus, models.DO_NOTHING)
    uid = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pallets'


class Place(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    placens = models.CharField(max_length=8, blank=True, null=True)
    plcidfp = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    cpi = models.CharField(max_length=1, blank=True, null=True)
    pcicbsa = models.CharField(max_length=1, blank=True, null=True)
    pcinecta = models.CharField(max_length=1, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'place'


class PlaceLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    pl_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place_lookup'
        unique_together = (('st_code', 'pl_code'),)


class Pricing(models.Model):
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    isadmin = models.BooleanField(db_column='isAdmin', blank=True, null=True)  # Field name made lowercase.
    base = models.FloatField(blank=True, null=True)
    overcost = models.JSONField(blank=True, null=True)
    discount = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pricing'


class ReceiptPdfs(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=1000)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    recipient = models.ForeignKey('Recipients', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Courses, models.DO_NOTHING, blank=True, null=True)
    loid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receipt_pdfs'


class Recipients(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey('Teams', models.DO_NOTHING, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    client_number = models.CharField(max_length=255, blank=True, null=True)
    sign = models.CharField(max_length=255, blank=True, null=True)
    opening_hours = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipients'


class SecondaryUnitLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secondary_unit_lookup'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class State(models.Model):
    gid = models.AutoField(unique=True)
    region = models.CharField(max_length=2, blank=True, null=True)
    division = models.CharField(max_length=2, blank=True, null=True)
    statefp = models.CharField(primary_key=True, max_length=2)
    statens = models.CharField(max_length=8, blank=True, null=True)
    stusps = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'state'


class StateLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=40, blank=True, null=True)
    abbrev = models.CharField(unique=True, max_length=3, blank=True, null=True)
    statefp = models.CharField(unique=True, max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state_lookup'


class StatisticsTable(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    n_in = models.TextField(blank=True, null=True)
    n_in_2 = models.TextField(blank=True, null=True)
    deliveries_done = models.FloatField(blank=True, null=True)
    table_1 = models.TextField(blank=True, null=True)
    km_done = models.FloatField(blank=True, null=True)
    table_ges = models.TextField(blank=True, null=True)
    table_ges_km = models.TextField(blank=True, null=True)
    table_ges_vehi = models.TextField(blank=True, null=True)
    deliveries_on_checklist = models.IntegerField(blank=True, null=True)
    deliveries_in_process = models.IntegerField(blank=True, null=True)
    ts_termine = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics_table'


class StatisticsTableMall(models.Model):
    user_code = models.TextField(blank=True, null=True)
    nc_a = models.TextField(blank=True, null=True)
    clients_info = models.TextField(blank=True, null=True)
    deliveries_done = models.IntegerField(blank=True, null=True)
    co2_saved = models.FloatField(blank=True, null=True)
    co2_saved_kg = models.FloatField(blank=True, null=True)
    km_saved = models.FloatField(blank=True, null=True)
    table_ges = models.TextField(blank=True, null=True)
    table_5 = models.TextField(blank=True, null=True)
    table_ges_km = models.TextField(blank=True, null=True)
    table_ges_vehi = models.TextField(blank=True, null=True)
    table_es = models.TextField(blank=True, null=True)
    table_time_vehi = models.TextField(blank=True, null=True)
    km_final = models.TextField(blank=True, null=True)
    km_percentage_field = models.FloatField(db_column='km_percentage_', blank=True, null=True)  # Field renamed because it ended with '_'.
    table_1 = models.TextField(blank=True, null=True)
    table_2 = models.TextField(blank=True, null=True)
    table_6 = models.TextField(blank=True, null=True)
    n_in = models.TextField(blank=True, null=True)
    n_in_3 = models.TextField(blank=True, null=True)
    mean_duration = models.TextField(blank=True, null=True)
    km_mean = models.TextField(blank=True, null=True)
    service_rate = models.TextField(blank=True, null=True)
    mean_rate = models.FloatField(blank=True, null=True)
    df = models.TextField(blank=True, null=True)
    cloud = models.TextField(blank=True, null=True)
    ts_termine = models.TextField(blank=True, null=True)
    week_ts_termine = models.TextField(db_column='Week_ts_termine', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    time_final = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics_table_mall'


class StreetTypeLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    abbrev = models.CharField(max_length=50, blank=True, null=True)
    is_hw = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'street_type_lookup'


class Tabblock(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    tabblock_id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    ur = models.CharField(max_length=1, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tabblock'


class Tasks(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    nb_bon = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    order_coursier = models.IntegerField(blank=True, null=True)
    coursier = models.ForeignKey(Coursier, models.DO_NOTHING, blank=True, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    volumn = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    sign_filename = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    ready_to_pick_up = models.BooleanField(blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    course = models.ForeignKey(Courses, models.DO_NOTHING, blank=True, null=True)
    history = models.JSONField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    rate_note = models.TextField(blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    recipient = models.ForeignKey(Recipients, models.DO_NOTHING, blank=True, null=True)
    hub = models.ForeignKey(Hubs, models.DO_NOTHING, blank=True, null=True)
    co2 = models.JSONField(blank=True, null=True)
    start_interval = models.IntegerField(blank=True, null=True)
    cycling = models.JSONField(blank=True, null=True)
    driving = models.JSONField(blank=True, null=True)
    altitudes = models.JSONField(blank=True, null=True)
    total_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_volumn = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_packages = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class Teams(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)
    team_id = models.CharField(db_column='team_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    dispatch_rate = models.IntegerField(blank=True, null=True)
    zipcode = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams'


class Tract(models.Model):
    gid = models.AutoField()
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    tract_id = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=7, blank=True, null=True)
    namelsad = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tract'


class UsGaz(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_gaz'


class UsLex(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_lex'


class UsRules(models.Model):
    rule = models.TextField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'us_rules'


class Users(models.Model):
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
    team = models.ForeignKey(Teams, models.DO_NOTHING, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    new_user = models.BooleanField()
    picture_name = models.CharField(max_length=255, blank=True, null=True)
    merchant = models.ForeignKey(Merchants, models.DO_NOTHING, blank=True, null=True)
    push_token = models.TextField(blank=True, null=True)
    push_os = models.TextField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class VehicleTypes(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(Teams, models.DO_NOTHING)
    volumn = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_types'


class Zcta5(models.Model):
    gid = models.AutoField(unique=True)
    statefp = models.CharField(max_length=2)
    zcta5ce = models.CharField(primary_key=True, max_length=5)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    partflg = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'zcta5'
        unique_together = (('zcta5ce', 'statefp'),)


class ZipLookup(models.Model):
    zip = models.IntegerField(primary_key=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup'


class ZipLookupAll(models.Model):
    zip = models.IntegerField(blank=True, null=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_all'


class ZipLookupBase(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    state = models.CharField(max_length=40, blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    city = models.CharField(max_length=90, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_base'


class ZipState(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_state'
        unique_together = (('zip', 'stusps'),)


class ZipStateLoc(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    place = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'zip_state_loc'
        unique_together = (('zip', 'stusps', 'place'),)


class ZonePricing(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    zone = models.ForeignKey(AreaTeam, models.DO_NOTHING, blank=True, null=True)
    pricing = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zone_pricing'
# Create your models here.
