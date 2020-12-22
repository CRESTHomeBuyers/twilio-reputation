# CREST Home Buyers
# www.WeBuyTidewaterHouses.com
# We Buy Houses in Hampton Roads
# Sell Your Fast Fast in Virginia Beach, Portsmouth, Norfolk, Chesapeake Suffolk, Hampton, Newport News
# ------------------------------------------------------------------------------------------------------
# Phone Number Reputation Monitoring Tool
# Takes a list of phone numbers and returns spam scores from 3 different monitoring agencies.

from ConfigParser import SafeConfigParser
import requests
import json

# Create parser to read from config file.
parser = SafeConfigParser()
parser.read('twilio-reputation.cfg')

twilio_sid = parser.get('twilio_creds', 'sid')
twilio_token = parser.get('twilio_creds', 'token')
numbers = parser.get('numbers', 'number_list')

print "Starting: Twilio Phone Number Reputation Monitoring Tool..."
#print "Twilio SID: %s" % twilio_sid
#print "Twilio Token: %s" % twilio_token
print "Numbers: %s" % numbers

addons = ["nomorobo_spamscore", "marchex_cleancall", "icehook_scout"]

number_list = numbers.split(",")

spam_list = []

for number in number_list:
    print "CHECKING NUMBER: %s" % number
    for addon in addons:
        print "\tRunning addon %s on number %s" % (addon, number)
        query = "https://%s:%s@lookups.twilio.com/v1/PhoneNumbers/%s/?AddOns=%s" % (twilio_sid, twilio_token, number, addon)
        #print "\tQuery is %s" % query
        r = requests.get(query)
        #print r.text
        j = json.loads(r.text)

        if addon == "nomorobo_spamscore":
            score = j["add_ons"]["results"][addon]["result"]["score"]
            score_text = "\t\tNomorobo Spamscore: %s" % score
            print score_text
            if score == 1:
                print "\t\t***ALERT***: NOMOROBO IDENTIFIED %s AS SPAM." % (number)
                if number not in spam_list:
                    spam_list.append(number)
        if addon == "marchex_cleancall":
            score = j["add_ons"]["results"][addon]["result"]["result"]["recommendation"]
            score_text = "\t\tMarchex Recommendation: %s" % score
            print score_text
            if score == "FAIL":
                print "\t\t***ALERT***: MARCHEX IDENTIFIED %s AS SPAM." % (number)
                if number not in spam_list:
                    spam_list.append(number)
        if addon == "icehook_scout":

            score = j["add_ons"]["results"][addon]["result"]["risk_rating"]
            score_text = "\t\tIcehook Risk Level: %s" % score
            print score_text
            if score == "highly_likely":
                print "\t\t***ALERT***: ICEHOOK IDENTIFIED %s AS SPAM." % (number)
                if number not in spam_list:
                    spam_list.append(number)

print "--------------------------------------------------------------------------------------------------------"
print "RESULTS\nThe following numbers were reported as spam:"
for n in spam_list:
    print n

raw_input("Press any key to exit.")
