from __future__ import unicode_literals
from .base import APIClient


# App Manager Services
class app_manager(object):
    _application_name = 'AppManager'
    app = APIClient(
        application=_application_name,
        service_uri='app/')
    app_member = APIClient(
        application=_application_name,
        service_uri='app/{app_id}/member/')
    app_menu = APIClient(
        application=_application_name,
        service_uri='app/{app_id}/menu_item/')
    menu_item_user = APIClient(
        application=_application_name,
        service_uri='menu_item/user/{user_id}/')


# Asset
class asset(object):
    _application_name = 'Asset'
    asset = APIClient(
        application=_application_name,
        service_uri='Asset/')
    asset_transaction = APIClient(
        application=_application_name,
        service_uri='Asset/{idAsset}/Transaction/')
    depreciation_type = APIClient(
        application=_application_name,
        service_uri='DepreciationType/')
    off_rent = APIClient(
        application=_application_name,
        service_uri='OffRent/')
    off_test = APIClient(
        application=_application_name,
        service_uri='OffTest/')
    rent = APIClient(
        application=_application_name,
        service_uri='Rent/')
    # asset = APIClient(
    #     application=_application_name,
    #     service_uri='asset/')
    # asset_transaction = APIClient(
    #     application=_application_name,
    #     service_uri='asset/{asset_id}/transaction/')
    # depreciation_type = APIClient(
    #     application=_application_name,
    #     service_uri='depreciation_type/')
    # off_rent = APIClient(
    #     application=_application_name,
    #     service_uri='off_rent/')
    # off_test = APIClient(
    #     application=_application_name,
    #     service_uri='off_test/')
    # rent = APIClient(
    #     application=_application_name,
    #     service_uri='rent/')


# Circuit - will be deprecated for DCIM
class circuit(object):
    _application_name = 'Circuit'
    circuit = APIClient(
        application=_application_name,
        service_uri='circuit/')
    circuit_class = APIClient(
        application=_application_name,
        service_uri='circuit_class/')
    property_type = APIClient(
        application=_application_name,
        service_uri='property_type/')
    property_value = APIClient(
        application=_application_name,
        service_uri='property_value/{search_term}/')

# Contact Services
class contact(object):
    _application_name = 'Contact'
    activity = APIClient(
        application=_application_name,
        service_uri='activity/')
    activity_type = APIClient(
        application=_application_name,
        service_uri='activity_type/')
    auth = APIClient(
        application=_application_name,
        service_uri='{chatbot_name}/auth/')
    campaign = APIClient(
        application=_application_name,
        service_uri='campaign/')
    campaign_activity = APIClient(
        application=_application_name,
        service_uri='campaign/{campaign_id}/activity/')
    campaign_contact = APIClient(
        application=_application_name,
        service_uri='campaign/{campaign_id}/contact/')
    chatbot = APIClient(
        application=_application_name,
        service_uri='chatbot/')
    contact = APIClient(
        application=_application_name,
        service_uri='contact/')
    conversation = APIClient(
        application=_application_name,
        service_uri='{chatbot_name}/conversation/')
    corpus = APIClient(
        application=_application_name,
        service_uri='chatbot/{chatbot_id}/corpus/')
    group = APIClient(
        application=_application_name,
        service_uri='group/')
    group_contact = APIClient(
        application=_application_name,
        service_uri='group/{group_id}/contact/')
    opportunity = APIClient(
        application=_application_name,
        service_uri='opportunity/')
    opportunity_contact = APIClient(
        application=_application_name,
        service_uri='opportunity/{opportunity_id}/contact/')
    opportunity_history = APIClient(
        application=_application_name,
        service_uri='opportunity/{opportunity_id}/history/')
    q_and_a = APIClient(
        application=_application_name,
        service_uri='{chatbot_name}/conversation/{conversation_id}/q_and_a/')

# Contacts Services - To be Deprectaetd for Contact
class contacts(object):
    _application_name = 'Contacts'
    activity = APIClient(
        application=_application_name,
        service_uri='ActivityType/{idActivityType}/Activity/')
    activity_type = APIClient(
        application=_application_name,
        service_uri='ActivityType/')
    campaign_activity = APIClient(
        application=_application_name,
        service_uri='Campaign/{idCampaign}/Activity/')
    campaign = APIClient(
        application=_application_name,
        service_uri='Campaign/')
    campaign_contact = APIClient(
        application=_application_name,
        service_uri='Campaign/{idCampaign}/Contact/')
    contact = APIClient(
        application=_application_name,
        service_uri='Contact/')
    group = APIClient(
        application=_application_name,
        service_uri='Group/')
    group_contact = APIClient(
        application=_application_name,
        service_uri='Group/{idGroup}/Contact/')
    opportunity = APIClient(
        application=_application_name,
        service_uri='Opportunity/')
    opportunity_contact = APIClient(
        application=_application_name,
        service_uri='Opportunity/{idOpportunity}/Contact/')
    opportunity_history = APIClient(
        application=_application_name,
        service_uri='Opportunity/{idOpportunity}/History/')

# DCIM
class dcim(object):
    _application_name = 'DCIM'
    circuit = APIClient(
        application=_application_name,
        service_uri='circuit/')
    circuit_class = APIClient(
        application=_application_name,
        service_uri='circuit_class/')
    property_type = APIClient(
        application=_application_name,
        service_uri='property_type/')
    property_value = APIClient(
        application=_application_name,
        service_uri='property_value/{search_term}/')

# DNS Services.
class dns(object):
    _application_name = 'IAAS'
    allocation = APIClient(
        application=_application_name,
        service_uri='allocation/')
    asn = APIClient(
        application=_application_name,
        service_uri='asn/')
    attach = APIClient(
        application=_application_name,
        service_uri='attach/{resource_id}/parent/{parent_resource_id}/')
    backup = APIClient(
        application=_application_name,
        service_uri='backup/')
    backup_history = APIClient(
        application=_application_name,
        service_uri='backup_history/')
    blacklist = APIClient(
        application=_application_name,
        service_uri='cix_blacklist/')
    capacity = APIClient(
        application=_application_name,
        service_uri='capacity/{region_id}/')
    ceph = APIClient(
        application=_application_name,
        service_uri='ceph/')
    cloud = APIClient(
        application=_application_name,
        service_uri='cloud/')
    cloud_bill = APIClient(
        application=_application_name,
        service_uri='cloud/pricing/')
    detach = APIClient(
        application=_application_name,
        service_uri='detach/{resource_id}/')
    device = APIClient(
        application=_application_name,
        service_uri='device/')
    device_type = APIClient(
        application=_application_name,
        service_uri='device_type/')
    domain = APIClient(
        application=_application_name,
        service_uri='domain/')
    image = APIClient(
        application=_application_name,
        service_uri='image/')
    interface = APIClient(
        application=_application_name,
        service_uri='interface/')
    ip_address = APIClient(
        application=_application_name,
        service_uri='ip_address/')
    ip_validator = APIClient(
        application=_application_name,
        service_uri='ip_validator/')
    ipmi = APIClient(
        application=_application_name,
        service_uri='ipmi/')
    metrics = APIClient(
        application=_application_name,
        service_uri='metrics/{region_id}/')
    policy_log = APIClient(
        application=_application_name,
        service_uri='policy_log/{project_id}/')
    pool_ip = APIClient(
        application=_application_name,
        service_uri='pool_ip/')
    project = APIClient(
        application=_application_name,
        service_uri='project/')
    ptr_record = APIClient(
        application=_application_name,
        service_uri='ptr_record/')
    record = APIClient(
        application=_application_name,
        service_uri='record/')
    region_image = APIClient(
        application=_application_name,
        service_uri='region_image/')
    router = APIClient(
        application=_application_name,
        service_uri='router/')
    run_robot = APIClient(
        application=_application_name,
        service_uri='run_robot/')
    server = APIClient(
        application=_application_name,
        service_uri='server/')
    server_type = APIClient(
        application=_application_name,
        service_uri='server_type/')
    snapshot = APIClient(
        application=_application_name,
        service_uri='snapshot/')
    snapshot_history = APIClient(
        application=_application_name,
        service_uri='snapshot_history/')
    snapshot_tree = APIClient(
        application=_application_name,
        service_uri='snapshot_tree/{vm_id}/')
    storage = APIClient(
        application=_application_name,
        service_uri='vm/{vm_id}/storage/')
    storage_type = APIClient(
        application=_application_name,
        service_uri='storage_type/')
    subnet = APIClient(
        application=_application_name,
        service_uri='subnet/')
    subnet_space = APIClient(
        application=_application_name,
        service_uri='subnet_space/{allocation_id}/')
    virtual_router = APIClient(
        application=_application_name,
        service_uri='virtual_router/')
    vm = APIClient(
        application=_application_name,
        service_uri='vm/')
    vm_history = APIClient(
        application=_application_name,
        service_uri="vm_history/")
    vpn = APIClient(
        application=_application_name,
        service_uri="vpn/")
    vpn_history = APIClient(
        application=_application_name,
        service_uri="vpn_history/")
    vpn_status = APIClient(
        application=_application_name,
        service_uri="vpn_status/{vpn_id}/")
    whitelist = APIClient(
        application=_application_name,
        service_uri='cix_whitelist/')


# Documentation Services
class documentation(object):
    _application_name = 'Documentation'
    application = APIClient(
        application=_application_name,
        service_uri='Application/')


# Financial
class financial(object):
    _application_name = 'Financial'
    account_purchase_adjustment = APIClient(
        application=_application_name,
        service_uri='account_purchase_adjustment/')
    account_purchase_adjustment_contra = APIClient(
        application=_application_name,
        service_uri='account_purchase_adjustment_contra/address/{source_id}/')
    account_purchase_debit_note = APIClient(
        application=_application_name,
        service_uri='account_purchase_debit_note/')
    account_purchase_debit_note_contra = APIClient(
        application=_application_name,
        service_uri='account_purchase_debit_note_contra/address/{source_id}/')
    account_purchase_invoice = APIClient(
        application=_application_name,
        service_uri='account_purchase_invoice/')
    account_purchase_invoice_contra = APIClient(
        application=_application_name,
        service_uri='account_purchase_invoice_contra/address/{source_id}/')
    account_purchase_payment = APIClient(
        application=_application_name,
        service_uri='account_purchase_payment/')
    account_purchase_payment_contra = APIClient(
        application=_application_name,
        service_uri='account_purchase_payment_contra/address/{source_id}/')
    account_sale_adjustment = APIClient(
        application=_application_name,
        service_uri='account_sale_adjustment/')
    account_sale_adjustment_contra = APIClient(
        application=_application_name,
        service_uri='account_sale_adjustment_contra/address/{source_id}/')
    account_sale_credit_note = APIClient(
        application=_application_name,
        service_uri='account_sale_credit_note/')
    account_sale_credit_note_contra = APIClient(
        application=_application_name,
        service_uri='account_sale_credit_note_contra/address/{source_id}/')
    account_sale_invoice = APIClient(
        application=_application_name,
        service_uri='account_sale_invoice/')
    account_sale_invoice_contra = APIClient(
        application=_application_name,
        service_uri='account_sale_invoice_contra/address/{source_id}/')
    account_sale_payment = APIClient(
        application=_application_name,
        service_uri='account_sale_payment/')
    account_sale_payment_contra = APIClient(
        application=_application_name,
        service_uri='account_sale_payment_contra/address/{source_id}/')
    allocation = APIClient(
        application=_application_name,
        service_uri='allocation/')
    balance_sheet = APIClient(
        application=_application_name,
        service_uri='balance_sheet/')
    cash_purchase_debit_note = APIClient(
        application=_application_name,
        service_uri='cash_purchase_debit_note/')
    cash_purchase_debit_note_contra = APIClient(
        application=_application_name,
        service_uri='cash_purchase_debit_note_contra/address/{source_id}/')
    cash_purchase_invoice = APIClient(
        application=_application_name,
        service_uri='cash_purchase_invoice/')
    cash_purchase_invoice_contra = APIClient(
        application=_application_name,
        service_uri='cash_purchase_invoice_contra/address/{source_id}/')
    cash_purchase_receipt = APIClient(
        application=_application_name,
        service_uri='cash_purchase_receipt/')
    cash_purchase_refund = APIClient(
        application=_application_name,
        service_uri='cash_purchase_refund/')
    cash_sale_credit_note = APIClient(
        application=_application_name,
        service_uri='cash_sale_credit_note/')
    cash_sale_credit_note_contra = APIClient(
        application=_application_name,
        service_uri='cash_sale_credit_note_contra/address/{source_id}/')
    cash_sale_invoice = APIClient(
        application=_application_name,
        service_uri='cash_sale_invoice/')
    cash_sale_invoice_contra = APIClient(
        application=_application_name,
        service_uri='cash_sale_invoice_contra/address/{source_id}/')
    cash_sale_receipt = APIClient(
        application=_application_name,
        service_uri='cash_sale_receipt/')
    cash_sale_refund = APIClient(
        application=_application_name,
        service_uri='cash_sale_refund/')
    cloud_bill = APIClient(
        application=_application_name,
        service_uri='cloud_bill/{project_id}/')
    credit_limit = APIClient(
        application=_application_name,
        service_uri='credit_limit/')
    creditor_account_history = APIClient(
        application=_application_name,
        service_uri='creditor_account/{id}/history/')
    creditor_account_statement = APIClient(
        application=_application_name,
        service_uri='creditor_account/{id}/statement/')
    creditor_ledger = APIClient(
        application=_application_name,
        service_uri='creditor_ledger/')
    creditor_ledger_aged = APIClient(
        application=_application_name,
        service_uri='creditor_ledger/aged/')
    creditor_ledger_contra_transaction = APIClient(
        application=_application_name,
        service_uri='creditor_ledger/contra_transaction/')
    creditor_ledger_transaction = APIClient(
        application=_application_name,
        service_uri='creditor_ledger/transaction/')
    debtor_account_history = APIClient(
        application=_application_name,
        service_uri='debtor_account/{id}/history/')
    debtor_account_statement = APIClient(
        application=_application_name,
        service_uri='debtor_account/{id}/statement/')
    debtor_ledger = APIClient(
        application=_application_name,
        service_uri='debtor_ledger/')
    debtor_ledger_aged = APIClient(
        application=_application_name,
        service_uri='debtor_ledger/aged/')
    debtor_ledger_contra_transaction = APIClient(
        application=_application_name,
        service_uri='debtor_ledger/contra_transaction/')
    debtor_ledger_transaction = APIClient(
        application=_application_name,
        service_uri='debtor_ledger/transaction/')
    global_nominal_account = APIClient(
        application=_application_name,
        service_uri='global_nominal_account/')
    journal_entry = APIClient(
        application=_application_name,
        service_uri='journal_entry/')
    nominal_account_history = APIClient(
        application=_application_name,
        service_uri='nominal_account/{id}/history/')
    nominal_account_type = APIClient(
        application=_application_name,
        service_uri='nominal_account_type/')
    nominal_contra = APIClient(
        application=_application_name,
        service_uri='nominal_contra/')
    payment_method = APIClient(
        application=_application_name,
        service_uri='payment_method/')
    period_end = APIClient(
        application=_application_name,
        service_uri='period_end/')
    profit_loss = APIClient(
        application=_application_name,
        service_uri='profit_and_loss/')
    purchases_analysis = APIClient(
        application=_application_name,
        service_uri='purchases_analysis/')
    purchases_by_country = APIClient(
        application=_application_name,
        service_uri='purchases_by_country/')
    purchases_by_territory = APIClient(
        application=_application_name,
        service_uri='purchases_by_territory/{territory_id}/')
    rtd = APIClient(
        application=_application_name,
        service_uri='rtd/')
    sales_analysis = APIClient(
        application=_application_name,
        service_uri='sales_analysis/')
    sales_by_country = APIClient(
        application=_application_name,
        service_uri='sales_by_country/')
    sales_by_territory = APIClient(
        application=_application_name,
        service_uri='sales_by_territory/{territory_id}/')
    statement = APIClient(
        application=_application_name,
        service_uri='statement/')
    statement_log = APIClient(
        application=_application_name,
        service_uri='statement_log/')
    statement_settings = APIClient(
        application=_application_name,
        service_uri='statement_settings/')
    trial_balance = APIClient(
        application=_application_name,
        service_uri='trial_balance/')
    tax_rate = APIClient(
        application=_application_name,
        service_uri='tax_rate/')
    vat3 = APIClient(
        application=_application_name,
        service_uri='vat3/')
    vies_purchases = APIClient(
        application=_application_name,
        service_uri='vies_purchases/')
    vies_sales = APIClient(
        application=_application_name,
        service_uri='vies_sales/')
    year_end = APIClient(
        application=_application_name,
        service_uri='year_end/')


# HelpDesk
class support(object):
    _application_name = 'Support'
    iris_condition = APIClient(
        application=_application_name,
        service_uri='iris_condition/')
    iris_condition_translation = APIClient(
        application=_application_name,
        service_uri='iris_condition/{iris_condition_id}/translation/')
    iris_defect = APIClient(
        application=_application_name,
        service_uri='iris_defect/')
    iris_defect_translation = APIClient(
        application=_application_name,
        service_uri='iris_defect/{iris_defect_id}/translation/')
    iris_extended_condition = APIClient(
        application=_application_name,
        service_uri='iris_extended_condition/')
    iris_extended_condition_translation = APIClient(
        application=_application_name,
        service_uri='iris_extended_condition/{iris_extended_condition_id}/translation/')
    iris_ntf = APIClient(
        application=_application_name,
        service_uri='iris_ntf/')
    iris_ntf_translation = APIClient(
        application=_application_name,
        service_uri='iris_ntf/{iris_ntf_id}/translation/')
    iris_repair = APIClient(
        application=_application_name,
        service_uri='iris_repair/')
    iris_repair_translation = APIClient(
        application=_application_name,
        service_uri='iris_repair/{iris_repair_id}/translation/')
    iris_section = APIClient(
        application=_application_name,
        service_uri='iris_section/')
    iris_section_translation = APIClient(
        application=_application_name,
        service_uri='iris_section/{iris_section_id}/translation/')
    iris_symptom = APIClient(
        application=_application_name,
        service_uri='iris_symptom/')
    iris_symptom_translation = APIClient(
        application=_application_name,
        service_uri='iris_symptom/{iris_symptom_id}/translation/')
    item = APIClient(
        application=_application_name,
        service_uri='ticket/{transaction_type_id}/{tsn}/item/')
    item_history = APIClient(
        application=_application_name,
        service_uri=('ticket/{transaction_type_id}/{tsn}/item/'
                     '{item_id}/history/'))
    item_status = APIClient(
        application=_application_name,
        service_uri='item_status/')
    part_used = APIClient(
        application=_application_name,
        service_uri=('ticket/{transaction_type_id}/{tsn}/item/'
                     '{item_id}/part_used/'))
    reason_for_return = APIClient(
        application=_application_name,
        service_uri='reason_for_return/')
    reason_for_return_translation = APIClient(
        application=_application_name,
        service_uri='reason_for_return/{reason_for_return_id}/translation/')
    service_centre_logic = APIClient(
        application=_application_name,
        service_uri='service_centre_logic/')
    service_centre_warrantor = APIClient(
        application=_application_name,
        service_uri='service_centre/{address_id}/warrantor/')
    status = APIClient(
        application=_application_name,
        service_uri='status/')
    ticket = APIClient(
        application=_application_name,
        service_uri='ticket/{transaction_type_id}/')
    ticket_history = APIClient(
        application=_application_name,
        service_uri='ticket/{transaction_type_id}/{tsn}/history/')
    ticket_question = APIClient(
        application=_application_name,
        service_uri='ticket_question/')
    ticket_type = APIClient(
        application=_application_name,
        service_uri='ticket_type/')
    warrantor_logic = APIClient(
        application=_application_name,
        service_uri='warrantor_logic/')
    warrantor_service_centre = APIClient(
        application=_application_name,
        service_uri='warrantor/{address_id}/service_centre/')


# Import Engine (BETA)
class import_engine(object):
    _application_name = 'Import'
    application = APIClient(
        application=_application_name,
        service_uri='Application/')
    import_service = APIClient(
        application=_application_name,
        service_uri='Import/')
    model = APIClient(
        application=_application_name,
        service_uri='Application/{idApplication}/Model/')


# Membership
class membership(object):
    _application_name = 'Membership'
    address = APIClient(
        application=_application_name,
        service_uri='Address/')
    address_link = APIClient(
        application=_application_name,
        service_uri='Address/{idAddress}/Link/')
    cloud_bill = APIClient(
        application=_application_name,
        service_uri='cloud_bill/{address_id}/{target_address_id}/')
    cloud_budget = APIClient(
        application=_application_name,
        service_uri='cloud_budget/')
    country = APIClient(
        application=_application_name,
        service_uri='Country/')
    currency = APIClient(
        application=_application_name,
        service_uri='Currency/')
    department = APIClient(
        application=_application_name,
        service_uri='Department/')
    email_confirmation = APIClient(
        application=_application_name,
        service_uri='email_confirmation/{email_token}')
    franchise_logic = APIClient(
        application=_application_name,
        service_uri='franchise_logic/{builder_address_id}/{distributor_address_id}/')
    language = APIClient(
        application=_application_name,
        service_uri='Language/')
    member = APIClient(
        application=_application_name,
        service_uri='Member/')
    member_link = APIClient(
        application=_application_name,
        service_uri='Member/{idMember}/Link/')
    notification = APIClient(
        application=_application_name,
        service_uri='Address/{idAddress}/Notification/')
    profile = APIClient(
        application=_application_name,
        service_uri='Profile/')
    public_key = APIClient(
        application=_application_name,
        service_uri='public_key/')
    subdivision = APIClient(
        application=_application_name,
        service_uri='Country/{idCountry}/Subdivision/')
    team = APIClient(
        application=_application_name,
        service_uri='Team/')
    territory = APIClient(
        application=_application_name,
        service_uri='Territory/')
    timezone = APIClient(
        application=_application_name,
        service_uri='Timezone/')
    transaction_type = APIClient(
        application=_application_name,
        service_uri='TransactionType/')
    token = APIClient(
        application=_application_name,
        service_uri='auth/login/',
    )
    user = APIClient(
        application=_application_name,
        service_uri='User/')
    verbose_address = APIClient(
        application=_application_name,
        service_uri='address/verbose/')

# NLP Services
class nlp(object):
    _application_name = 'NLP'
    embedding_use = APIClient(
        application=_application_name,
        service_uri='embedding_use/')

# OTP Services
class otp(object):
    _application_name = 'OTP'
    otp = APIClient(
        application=_application_name,
        service_uri='otp/')
    otp_auth = APIClient(
        application=_application_name,
        service_uri='otp_auth/{email}/')


# PAT
class pat(object):
    _application_name = 'PAT'
    pod = APIClient(
        application=_application_name,
        service_uri='Pod/')


# Plot (BETA) -> Only list methods implemented!
class plot(object):
    _application_name = 'Plot'
    reading = APIClient(
        application=_application_name,
        service_uri='Source/{idSource}/Reading/')
    source = APIClient(
        application=_application_name,
        service_uri='Source/')


# Reporting
class reporting(object):
    _application_name = 'Reporting'
    export = APIClient(
        application=_application_name,
        service_uri='Export/')
    package = APIClient(
        application=_application_name,
        service_uri='Package/')
    report = APIClient(
        application=_application_name,
        service_uri='Report/')
    report_template = APIClient(
        application=_application_name,
        service_uri='ReportTemplate/')


# Scheduler
class scheduler(object):
    _application_name = 'Scheduler'
    task = APIClient(
        application=_application_name,
        service_uri='task/')
    task_log = APIClient(
        application=_application_name,
        service_uri='task_log/')


# SCM
class scm(object):
    _application_name = 'SCM'
    agreed_price = APIClient(
        application=_application_name,
        service_uri='AgreedPrice/')
    brand = APIClient(
        application=_application_name,
        service_uri='Brand/')
    bin = APIClient(
        application=_application_name,
        service_uri='Bin/')
    bin_sku = APIClient(
        application=_application_name,
        service_uri='Bin/{id}/SKU/')
    cloud_bill = APIClient(
        application=_application_name,
        service_uri='CloudBill/{address_id}/')
    # idSKUComponent should be passed as pk to resource methods
    critical_bom = APIClient(
        application=_application_name,
        service_uri='SKU/{idSKU}/BOM/')
    # CriticalBOM for member returns all BOM records for the idMember
    # doing the request
    critical_bom_for_member = APIClient(
        application=_application_name,
        service_uri='SKU/BOM/')
    manufactured_item = APIClient(
        application=_application_name,
        service_uri='ManufacturedItem/')
    purchase_order = APIClient(
        application=_application_name,
        service_uri='PurchaseOrder/')
    return_question = APIClient(
        application=_application_name,
        service_uri='ReturnQuestion/')
    return_question_field_type = APIClient(
        application=_application_name,
        service_uri='ReturnQuestionFieldType/')
    sales_order = APIClient(
        application=_application_name,
        service_uri='SalesOrder/')
    service_group = APIClient(
        application=_application_name,
        service_uri='ServiceGroup/')
    sku = APIClient(
        application=_application_name,
        service_uri='SKU/')
    sku_category = APIClient(
        application=_application_name,
        service_uri='SKUCategory/')
    sku_category_return_question = APIClient(
        application=_application_name,
        service_uri='SKUCategory/{idSKUCategory}/ReturnQuestion/')
    sku_stock = APIClient(
        application=_application_name,
        service_uri='SKU/{idSKU}/Stock/')
    sku_stock_adjustment = APIClient(
        application=_application_name,
        service_uri='SKUStockAdjustment/')
    sku_value = APIClient(
        application=_application_name,
        service_uri='SKU/{idSKU}/Value/')
    validate_purchase_order = APIClient(
        application=_application_name,
        service_uri='Validate/PurchaseOrder/')
    validate_sales_order = APIClient(
        application=_application_name,
        service_uri='Validate/SalesOrder/')


# Security
class security(object):
    _application_name = 'Security'
    security_event = APIClient(
        application=_application_name,
        service_uri='SecurityEvent/')
    security_event_logout = APIClient(
      application=_application_name,
      service_uri='SecurityEvent/{idUser}/Logout/')


# Support Framework Services
class support_framework(object):
    _application_name = 'SupportFramework'
    application = APIClient(
        application=_application_name,
        service_uri='Member/{idMember}/Application/')
    dto = APIClient(
        application=_application_name,
        service_uri='DTO/')
    dto_parameter = APIClient(
        application=_application_name,
        service_uri='DTO/{idDTO}/Parameter/')
    exception_code = APIClient(
        application=_application_name,
        service_uri='ExceptionCode/')
    language_exception_code = APIClient(
        application=_application_name,
        service_uri='ExceptionCode/{exception_code}/Language/')
    member = APIClient(
        application=_application_name,
        service_uri='Member/')
    method = APIClient(
        application=_application_name,
        service_uri=('Member/{idMember}/Application/{idApplication}/'
                     'Service/{idService}/Method/'))
    method_parameter = APIClient(
        application=_application_name,
        service_uri=('Member/{idMember}/Application/{idApplication}/Service/'
                     '{idService}/Method/{idMethod}/Parameter/'))
    service = APIClient(
        application=_application_name,
        service_uri='Member/{idMember}/Application/{idApplication}/Service/')


# Training
class training(object):
    _application_name = 'Training'
    cls = APIClient(
        application=_application_name,
        service_uri='Class/')
    student = APIClient(
        application=_application_name,
        service_uri='Student/')
    syllabus = APIClient(
        application=_application_name,
        service_uri='Syllabus/')
