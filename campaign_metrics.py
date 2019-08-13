# Get Campaign Metrics by Noman Hamlani | Solutions Architect | Iterable Inc. 
# Purpose: Creates two csv files, one each for triggered and blast campaigns contating all the metrics availble on a per campaign basis

#pip3 install requests
import requests
import csv

# Your projects API Key -> Can be found under project integrations
API_KEY = "7534cd9291f646a9acce76b0fd00d2a2"

# Start and end times must in YYYY-MM-DD format
start_time = "2018-06-25"
end_time = "2018-07-25"

# Location of exported metrics
export_location = "/Users/noman.hamlani/Desktop/"

# Calls Iterable API for campaign metrics per campaign id, sepearates the header and the data
def get_metric_data(c_id):
	m_text = requests.get("https://api.iterable.com/api/campaigns/metrics?campaignId=" + str(c_id) + "&startDateTime=" + start_time + "&endDateTime=" + end_time + "&useNewFormat=true&api_key=" + API_KEY).text
	metric_data = []
	for i in m_text.split('\n')[1:]:
		metric_data.append(i.split(','))
	header_line = m_text.split('\n')[0].split(',')
	return header_line, metric_data


# Intializing triggered and blast campaign files 
triggered_data_file = open(export_location + "triggered.csv", 'w')
blast_data_file = open(export_location + "blast.csv", 'w')

# CSV writer objects
triggered_writer = csv.writer(triggered_data_file)
blast_writer = csv.writer(blast_data_file)

# Loop through Iterable response of list of campaigns, creating an entry in the above CSVs per campaign
campaign_meta = requests.get("https://api.iterable.com/api/campaigns?api_key=" + API_KEY).json()
for camp in campaign_meta["campaigns"]:
	print("Exporting: " + camp["name"])
	if camp["type"] == "Triggered":
		header, data = get_metric_data(camp["id"])
		# Extra array is created for formatting
		triggered_writer.writerow([camp["name"]])
		triggered_writer.writerow(header)
		triggered_writer.writerows(data)
		triggered_writer.writerow(['\n'])

	if camp["type"] == "Blast":
		header, data = get_metric_data(camp["id"])
		# Extra array is created for formatting
		blast_writer.writerow([camp["name"]])
		blast_writer.writerow(header)
		blast_writer.writerows(data)
		blast_writer.writerow(['\n'])
	
print("Done.")