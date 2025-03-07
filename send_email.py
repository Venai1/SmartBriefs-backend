'''
API_KEY = "re_7ZbDEmYy_Dizg5KJPsMc76zxfGegSBGrs"

import os
import resend

resend.api_key = API_KEY

params: resend.Emails.SendParams = {
    "from": "SmartBriefs <smartbriefs@newsletter.venai.dev>",
    "to": ["vinesh.seepersaud@gmail.com"],
    "subject": "hello world from venais computer",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)
print(email)
'''