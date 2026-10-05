import requests
import os
import sys
import pandas as pd
import math
from datetime import datetime
import time


API_KEY = #API key goes here
API_VERSION = "20240404"

header = {
        "Authorization": f"Token token={API_KEY}",
        "X-Api-Version": API_VERSION,
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }

#creates a candidate with basic info
def create_candidate(first_name, last_name, email, phone):

    URL = "https://api.teamtailor.com/v1/candidates"

    headers = header

    body = {
        "data": {
            "type": "candidates",
            "attributes": {
                "first-name": first_name,
                "last-name": last_name,
                "email": email,
                "phone": phone
            },
        }
    }

    response = requests.post(URL, headers=headers, json=body, timeout=30)

    if response.ok:
        candidate_id = response.json()["data"]["id"]
        print(f"Created candidate {candidate_id}")
        return(candidate_id)
    else:
        print(f"Failed with status {response.status_code}:")
        print(response.text)
        sys.exit(1)

#updates a text custom field
def update_custom_field(candidate_id, field_id, value):

    URL = "https://api.teamtailor.com/v1/custom-field-values"

    headers = header

    body = {
        "data": {
            "type": "custom-field-values",
            "attributes": {
                "value": value
            },
            "relationships": {
                "custom-field": {
                    "data": {
                        "id": field_id,
                        "type": "custom-fields"
                    }
                },
                "owner": {
                    "data": {
                        "id": candidate_id,
                        "type": "candidates"
                    }
                }
            }
        }
    }

    response = requests.post(URL, headers=headers, json=body, timeout=30)

    if response.ok:
        print(response.json)
    else:
        print(f"Failed with status {response.status_code}:")
        print(response.text)
        sys.exit(1)

#list of custom field ids for general fields which will accept a value as formatted in the sheet
custom_field_ids_general = {
    "job_title": 1273923,
    "vr_student": 1469418,
    "rtd_opt_in": 1469430,
    "town_city": 1267637,
    "hireflix": 1262940,
    "uk_holds_dual_nationality": 1262893,
    "consent_to_financial_check": 1262900,
    "uk_resident_10_years": 1274791,
    "uk_resident_5_years": 1262889,
    "uk_resident_3_years": 1262888,
    "plagiarism_on_course": 1476301,
    "notice_period": 1469431,
    "confirm_salary": 1469433,
    "ic_session": 1469434,
    "cloud_infrastructure_training": 1469435,
    "country_of_residence": 1262866,
    "uk_rtw_other_reason": 1274790
}

#gets the ids for the multi select options of a specific field and returns these as a dict (only works for up to 30 options)
def get_multiselect_ids(custom_field_id):
    URL = "https://api.teamtailor.com/v1/custom-field-options?filter[custom-field]="+str(custom_field_id)+"&page%5Bsize%5D=30"

    headers = header

    options = {}

    response = requests.get(URL, headers=headers, timeout=30)

    if response.ok:
        for option in response.json()["data"]:

            options[option["attributes"]["value"]] = option["id"]

    else:
        print(f"Failed with status {response.status_code}:")

    return options

#list of custom fields which have select options so need a specific id to upload values
custom_field_ids_select = {
    "cohort": 1469024,
    "degree_stream": 1469050,
    "mla_stream": 1469415,
    "masters_stream": 1469416,
    "degree_outcome": 1485156,
    "mla_outcome": 1485525,
    "uk_region": 1267976,
    "work_study_status": 1262980,
    "uk_rtw": 1262996
}

#fields with a multi select value where they can have more than one option selected
custom_field_ids_multiselect = {
    "nationalities": 1275481,
    "commercial_skills": 1262985,
    "salary_expectations": 1262982,
    "uk_last_10_years_checks": 1274792,
    "course_type": 1484860
}

#creates a dict of these field ids with their corresponding options as a sub-dict
# e.g. {1468979: {'MLA': '2696860', 'Degree': '2696861'}}
def get_all_multiselect_keys():
    multi_select_keys = {}

    for key in custom_field_ids_select.keys():
        multi_select_keys[custom_field_ids_select[key]] = get_multiselect_ids(custom_field_ids_select[key])

    for key in custom_field_ids_multiselect.keys():
        multi_select_keys[custom_field_ids_multiselect[key]] = get_multiselect_ids(custom_field_ids_multiselect[key])

    return multi_select_keys

multi_select_keys = get_all_multiselect_keys()

nationality_ids = {'Afghanistan': '2289558', 'Albania': '2289559', 'Algeria': '2289560', 'American Samoa': '2289561', 'Andorra': '2289562', 'Angola': '2289563', 'Anguilla': '2289564', 'Antarctica': '2289565', 'Antigua and Barbuda': '2289566', 'Argentina': '2289567', 'Armenia': '2289568', 'Aruba': '2289569', 'Asia/Pacific Region': '2289570', 'Australia': '2289571', 'Austria': '2289572', 'Azerbaijan': '2289573', 'Bahamas': '2289574', 'Bahrain': '2289575', 'Bangladesh': '2289576', 'Barbados': '2289577', 'Belarus': '2289578', 'Belgium': '2289579', 'Belize': '2289580', 'Benin': '2289581', 'Bermuda': '2289582', 'Bhutan': '2289583', 'Bolivia': '2289584', 'Bosnia and Herzegovina': '2289585', 'Botswana': '2289586', 'Bouvet Island': '2289587', 'Brazil': '2289588', 'British Indian Ocean Territory': '2289589', 'British Virgin Islands': '2289590', 'Brunei': '2289591', 'Bulgaria': '2289592', 'Burkina Faso': '2289593', 'Burundi': '2289594', 'Cambodia': '2289595', 'Cameroon': '2289596', 'Canada': '2289597', 'Cape Verde': '2289598', 'Caribbean Netherlands': '2289599', 'Cayman Islands': '2289600', 'Central African Republic': '2289601', 'Chad': '2289602', 'Chile': '2289603', 'China': '2289604', 'Christmas Island': '2289605', 'Cocos (Keeling) Islands': '2289606', 'Colombia': '2289607', 'Comoros': '2289608', 'Congo': '2289609', 'Cook Islands': '2289610', 'Costa Rica': '2289611', "Cote d'Ivoire": '2289612', 'Croatia': '2289613', 'Cuba': '2289614', 'Curaçao': '2289615', 'Cyprus': '2289616', 'Czech Republic': '2289617', 'Democratic Republic of the Congo': '2289618', 'Denmark': '2289619', 'Djibouti': '2289620', 'Dominica': '2289621', 'Dominican Republic': '2289622', 'East Timor': '2289623', 'Ecuador': '2289624', 'Egypt': '2289625', 'El Salvador': '2289626', 'Equatorial Guinea': '2289627', 'Eritrea': '2289628', 'Estonia': '2289629', 'Ethiopia': '2289630', 'Europe': '2289631', 'Falkland Islands': '2289632', 'Faroe Islands': '2289633', 'Fiji': '2289634', 'Finland': '2289635', 'France': '2289636', 'French Guiana': '2289637', 'French Polynesia': '2289638', 'French Southern and Antarctic Lands': '2289639', 'Gabon': '2289640', 'Gambia': '2289641', 'Georgia': '2289642', 'Germany': '2289643', 'Ghana': '2289644', 'Gibraltar': '2289645', 'Greece': '2289646', 'Greenland': '2289647', 'Grenada': '2289648', 'Guadeloupe': '2289649', 'Guam': '2289650', 'Guatemala': '2289651', 'Guernsey': '2289652', 'Guinea': '2289653', 'Guinea-Bissau': '2289654', 'Guyana': '2289655', 'Haiti': '2289656', 'Heard Island and McDonald Islands': '2289657', 'Honduras': '2289658', 'Hong Kong': '2289659', 'Hungary': '2289660', 'Iceland': '2289661', 'India': '2289662', 'Indonesia': '2289663', 'Iran': '2289664', 'Iraq': '2289665', 'Ireland': '2289666', 'Isle of Man': '2289667', 'Israel': '2289668', 'Italy': '2289669', 'Jamaica': '2289670', 'Japan': '2289671', 'Jersey': '2289672', 'Jordan': '2289673', 'Kazakhstan': '2289674', 'Kenya': '2289675', 'Kiribati': '2289676', 'Kuwait': '2289677', 'Kyrgyzstan': '2289678', 'Laos': '2289679', 'Latvia': '2289680', 'Lebanon': '2289681', 'Lesotho': '2289682', 'Liberia': '2289683', 'Libya': '2289684', 'Liechtenstein': '2289685', 'Lithuania': '2289686', 'Luxembourg': '2289687', 'Macau': '2289688', 'Macedonia (FYROM)': '2289689', 'Madagascar': '2289690', 'Malawi': '2289691', 'Malaysia': '2289692', 'Maldives': '2289693', 'Mali': '2289694', 'Malta': '2289695', 'Marshall Islands': '2289696', 'Martinique': '2289697', 'Mauritania': '2289698', 'Mauritius': '2289699', 'Mayotte': '2289700', 'Mexico': '2289701', 'Micronesia': '2289702', 'Moldova': '2289703', 'Monaco': '2289704', 'Mongolia': '2289705', 'Montenegro': '2289706', 'Montserrat': '2289707', 'Morocco': '2289708', 'Mozambique': '2289709', 'Myanmar (Burma)': '2289710', 'Namibia': '2289711', 'Nauru': '2289712', 'Nepal': '2289713', 'Netherlands': '2289714', 'Netherlands Antilles': '2289715', 'New Caledonia': '2289716', 'New Zealand': '2289717', 'Nicaragua': '2289718', 'Niger': '2289719', 'Nigeria': '2289720', 'Niue': '2289721', 'Norfolk Island': '2289722', 'North Korea': '2289723', 'Northern Mariana Islands': '2289724', 'Norway': '2289725', 'Oman': '2289726', 'Pakistan': '2289727', 'Palau': '2289728', 'Palestine': '2289729', 'Panama': '2289730', 'Papua New Guinea': '2289731', 'Paraguay': '2289732', 'Peru': '2289733', 'Philippines': '2289734', 'Pitcairn Islands': '2289735', 'Poland': '2289736', 'Portugal': '2289737', 'Puerto Rico': '2289738', 'Qatar': '2289739', 'Romania': '2289740', 'Russia': '2289741', 'Rwanda': '2289742', 'Réunion': '2289743', 'Saint Barthélemy': '2289744', 'Saint Helena': '2289745', 'Saint Kitts and Nevis': '2289746', 'Saint Lucia': '2289747', 'Saint Martin': '2289748', 'Saint Pierre and Miquelon': '2289749', 'Saint Vincent and the Grenadines': '2289750', 'Samoa': '2289751', 'San Marino': '2289752', 'Sao Tome and Principe': '2289753', 'Saudi Arabia': '2289754', 'Senegal': '2289755', 'Serbia': '2289756', 'Seychelles': '2289757', 'Sierra Leone': '2289758', 'Singapore': '2289759', 'Sint Maarten': '2289760', 'Slovakia': '2289761', 'Slovenia': '2289762', 'Solomon Islands': '2289763', 'Somalia': '2289764', 'South Africa': '2289765', 'South Georgia and the South Sandwich Islands': '2289766', 'South Korea': '2289767', 'South Sudan': '2289768', 'Spain': '2289769', 'Sri Lanka': '2289770', 'Sudan': '2289771', 'Suriname': '2289772', 'Svalbard and Jan Mayen': '2289773', 'Swaziland': '2289774', 'Sweden': '2289775', 'Switzerland': '2289776', 'Syria': '2289777', 'Taiwan': '2289778', 'Tajikistan': '2289779', 'Tanzania': '2289780', 'Thailand': '2289781', 'Togo': '2289782', 'Tokelau': '2289783', 'Tonga': '2289784', 'Trinidad and Tobago': '2289785', 'Tunisia': '2289786', 'Turkey': '2289787', 'Turkmenistan': '2289788', 'Turks and Caicos Islands': '2289789', 'Tuvalu': '2289790', 'U.S. Virgin Islands': '2289791', 'Uganda': '2289792', 'Ukraine': '2289793', 'United Arab Emirates': '2289794', 'United Kingdom': '2289795', 'United States': '2289796', 'United States Minor Outlying Islands': '2289797', 'Uruguay': '2289798', 'Uzbekistan': '2289799', 'Vanuatu': '2289800', 'Vatican City': '2289801', 'Venezuela': '2289802', 'Vietnam': '2289803', 'Wallis and Futuna': '2289804', 'Western Sahara': '2289805', 'Yemen': '2289806', 'Zambia': '2289807', 'Zimbabwe': '2289808', 'Åland Islands': '2289809'}

multi_select_keys[1275481] = nationality_ids

#updates a text custom field
def update_select_field(candidate_id, field_id, value):

    URL = "https://api.teamtailor.com/v1/custom-field-values"

    headers = header

    #get corresponding value id
    value_id = multi_select_keys[field_id][value]

    body = {
        "data": {
            "type": "custom-field-values",
            "attributes": {
                "value": [value_id]
            },
            "relationships": {
                "custom-field": {
                    "data": {
                        "id": field_id,
                        "type": "custom-fields"
                    }
                },
                "owner": {
                    "data": {
                        "id": candidate_id,
                        "type": "candidates"
                    }
                }
            }
        }
    }

    response = requests.post(URL, headers=headers, json=body, timeout=30)

    if response.ok:
        print(response.json)
    else:
        print(f"Failed with status {response.status_code}:")
        print(response.text)
        sys.exit(1)


def update_multi_select_field(candidate_id, field_id, value):

    value = value.replace(', ',';')

    value_list = value.split(';')

    output = []

    for value in value_list:
        output.append(multi_select_keys[field_id][value])

    update_custom_field(candidate_id, field_id, output)

def upload_cv(candidate_id, cv_url):
    url = f"https://api.teamtailor.com/v1/candidates/"+str(candidate_id)

    headers = header

    body = {
        "data": {
            "type": "candidates",
            "id": str(candidate_id),
            "attributes": {"resume": cv_url},
        }
    }

    response = requests.patch(url, headers=headers, json=body, timeout=30)

    if response.ok:
        print(response.json)
    else:
        print(f"Failed with status {response.status_code}:")
        print(response.text)
        sys.exit(1)

df = pd.read_csv('degree_outcome.csv')

for index, row in df.iterrows():

    #assign values to multi select fields
    if row['course_type'] == 'Degree':
        update_select_field(row['team_tailor_id'], 1485156, row['course_outcome'])
    else:
        update_select_field(row['team_tailor_id'], 1485525, row['course_outcome'])

'''
#read in the csv file to import
df = pd.read_csv('batch_9.csv')

#replace nulls with empty string
df = df.fillna("")

#iterate over each row
for index, row in df.iterrows():

    #creates the candidate
    candidate_id = create_candidate(row["first_name"], row["last_name"], row["email"], row["phone"])

    #assign values to general fields
    for key in custom_field_ids_general.keys():
        if row[key] != "":
            update_custom_field(candidate_id, custom_field_ids_general[key], row[key])

    #assign values to single select fields
    for key in custom_field_ids_select.keys():
        if row[key] != "":
            update_select_field(candidate_id, custom_field_ids_select[key], row[key])

    #assign values to multi select fields
    for key in custom_field_ids_multiselect.keys():
        if row[key] != "":
            update_multi_select_field(candidate_id, custom_field_ids_multiselect[key], row[key])

    #assign import date
    update_custom_field(candidate_id, 1469436, datetime.today().strftime('%Y-%m-%d'))

    #logging email
    with open("myfile.txt", "a") as f:
        f.write(candidate_id+','+ row['email']+'\n')

    #rate limiting - 2 second pause
    print("candidate completed")
    time.sleep(2)
'''


