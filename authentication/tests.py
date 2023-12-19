from django.test import TestCase

# Create your tests here.
# import requests
#
url = 'http://35.81.98.141:8000/api/social-tk/'  # Replace with the actual API endpoint URL

# social_token = f'EAALm7vOLvgoBAIy4PW0aezf8Dub4ZBGdRCoIhBGo0bxNoMLWXBSpLkSE8Xs7W82dC8negMUWD7UX9hRcoAGeAYBmJxVfZBjdZCZCgvHF4PSTHhakCyr8EFHsZBPlTZALoo1fQ9NsvCrolxM7G0t1yIqPFdSF70ygLjZBuVqSeOTdk0G7wg9yFqhb49q9dmugAB7xP32a8Qmx85VB09Yy9rqTYcmoou09ZCS3HuinXHUZCDWPp57VdKRP1'  # Replace with the actual social token
social_token = 'AQXG0CyD5vAllhYsUup7jPRsn3EsdrSIsSPWGiEktLQPc5781MpGQU7D1Sv9walof2yRxxpoDEl45PMzwt26EIquRD7Kii6-NZV5phK65VAw-BmH5irUHKVm4YkUUN3a9FI5d4xFPuhkxprlL4MKg3AS53T8ogAy1M4KTLoXR0IP7S-QWZWOdjLcqjBE5iIeranBxAAO9Ywkc3-ChlFR6QD9N2k6e9ExDe-6_LL-4Y6bsBvmgxTSmyJGyobzdMdwVN3g0FLb48D9WouJ0hbJ_f1NgySl_cnDZSKnlM7UmxIQuyXUh35sqOGfwvmcPzrUkh9jxBj_VkR9xg_owrimXl3kt6BNnw'  # Replace with the actual social token
#
# headers = {
#     'Authorization': f'Bearer {social_token}'
# }
#
# response = requests.post(url, headers=headers)
#
# if response.status_code == 200:
#     data = response.json()
#     # Handle the response data
#     print(data)
# else:
#     # Handle the error
#     print(response.text)
#     print(f"Request failed with status code {response.status_code}")


import requests

# url = 'http://example.com/your-api-endpoint'  # Replace with the actual API endpoint URL

# social_token = '<social_token>'  # Replace with the actual social token

headers = {
    'Authorization': 'Bearer ' + social_token
}

response = requests.post(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Handle the response data
    print(data)
else:
    # Handle the error
    print(f"Request failed with status code {response.status_code}")
    print(response.json())  # Print the error response details