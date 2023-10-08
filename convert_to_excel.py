import pandas as pd
import numpy as np

# Expanded set of key terms and problematic clauses for leases in England and Wales
data = {
    'Key Terms': [
        "Break clause: Allows tenant/landlord to end lease early",
        "Right of First Refusal: Tenant gets the first opportunity to buy or rent a new space",
        "Rent Review Clause: Regular review of the rental amount, typically yearly",
        "Covenant of Quiet Enjoyment: Tenant's right to undisturbed use and enjoyment of the property",
        "Repair Obligation: The responsibility to maintain and repair the property",
        "Subletting Clause: Conditions under which the tenant can sublet the property",
        "Use Clause: Permitted uses of the rented property",
        "Rent Payment: Method and date of rent payment specified",
        "Guarantor Requirement: The inclusion of a third party to guarantee rent payment",
        "Insurance: Tenant's obligation to insure their contents",
        "Renewal Option: Terms under which the lease can be renewed",
        "Access Rights: Landlord's rights to access the property for inspections or repairs",
        "Deposit Protection: Details of the tenant's deposit protection in a government-approved scheme",
        "Utilities and Bills: Allocation of responsibility for utilities and other bills",
        "Penalties: Penalties in case of bounced cheques or failed direct debit",
        "Termination Notice: The notice period required for termination",
        "Furnishing: Details of any furnishings provided as part of the lease",
        "Pets Clause: Specification about allowing or disallowing pets in the property",
        "Garden Maintenance: Responsibilities concerning garden or outdoor space maintenance"
    ],
    'Problem Clauses': [
        "Automatic Rent Increase: Rent increases automatically, potentially above inflation rates",
        "Lack of Break Clause: Lease doesn't allow for early termination",
        "Unilateral Changes: Landlord can change terms without tenant's agreement",
        "Wear and Tear: Tenant responsible for all repairs, even normal wear and tear",
        "Early Termination Penalties: Substantial charges for terminating the lease early",
        "Vague Fair Wear: Undefined or vague terms related to 'fair wear and tear'",
        "Dispute Costs: Tenant bears all legal fees in the event of disputes",
        "Guest Restrictions: Limitations or charges related to having guests over",
        "Withholding Deposit: Conditions allowing the landlord to withhold deposit are unclear",
        "Eviction for Showings: Tenant must vacate for property showings on short notice",
        "Late Rent Penalties: Excessive charges for slightly delayed rent payments",
        "Ambiguous Terms: Presence of clauses open to multiple interpretations",
        "Fixed Council Tax: Tenant pays a fixed council tax irrespective of actual usage",
        "No Cause Eviction: Landlord can evict without providing a clear reason",
        "Deposit Return Delays: No clear timeline for the return of the deposit after lease termination",
        "Mandatory Cleaning: Tenant must pay for professional cleaning, irrespective of property condition at end of lease",
        "Automatic Renewal: Lease automatically renews without explicit tenant approval"
    ]
}

# Finding the maximum length between the two lists
max_len = max(len(data['Key Terms']), len(data['Problem Clauses']))

# Padding the lists to make them of the same length
data['Key Terms'] = data['Key Terms'] + [np.nan] * (max_len - len(data['Key Terms']))
data['Problem Clauses'] = data['Problem Clauses'] + [np.nan] * (max_len - len(data['Problem Clauses']))

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('lease_terms_data.xlsx', index=False, engine='openpyxl')

print("Excel file 'lease_terms_data.xlsx' created successfully!")