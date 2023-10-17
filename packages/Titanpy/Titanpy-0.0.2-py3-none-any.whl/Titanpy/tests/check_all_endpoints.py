import Titanpy
# --------- ENDPOINT GROUPS --------- #

# Accounting
accounting_endpoints = [
    'export/inventory-bills',
    'export/invoice-items',
    'export/invoices',
    'export/payments',
    'ap-credits',
    'ap-payments',
    'inventory-bills',
    'invoices',
    'journal-entries',
    'payments',
    'payment-terms',
    'tax-zones',
]
accounting_id_endpoints = [
    'journal-entries-details/',
    'journal-entries-summary/',
    'payment-types/',
]

# CRM
crm_endpoints = [
    'export/bookings',
    'export/customers',
    'export/customers/contacts',
    'export/leads',
    'export/locations',
    'export/locations/contacts',
    'booking-provider-tags',
    'bookings',
    'customers',
    'customers/contacts',
    'leads',
    'locations',
    'locations/contacts',
]

crm_id_endpoints = [
    'booking-provider-tags/',
    '/bookings',
    '/bookings/',
    '/bookings-contacts/',
    'bookings/',
    'bookings-contacts/',
    'customers/',
    'customers-contacts/',
    'customers-notes/',
    'leads/',
    'leads-notes/',
    'locations/',
    'locations-contacts/',
    'locations-notes/',
]

# Forms
forms_endpoints = [
    'forms',
    'submissions',
]


# Reporting
reporting_endpoints = [
    'report-categories',
]
reporting_id_endpoints = [
    'dynamic-value-sets/',
    '/reports',
    '/reports/',
]

# --------- AVAILABLE ENDPOINTS --------- #

available_endpoints = [
    'jobs',
]
available_endpoint_groups = [
    accounting_endpoints,
    accounting_id_endpoints,
    reporting_endpoints,
    reporting_id_endpoints,
    forms_endpoints,
    crm_endpoints,
    crm_id_endpoints,
]
for group in available_endpoint_groups:
    available_endpoints.extend(group)


# --------- TEST ENDPOINTS --------- #

tp = Titanpy.Connect(cred_path="./credentials/servicetitan_credentials.json")
for endpoint in available_endpoints:
    response = tp.Get(endpoint = endpoint)
    print(response.status_code)
    