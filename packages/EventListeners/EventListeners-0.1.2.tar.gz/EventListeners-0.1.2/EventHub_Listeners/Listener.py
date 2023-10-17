import sys

from azure.eventhub import EventHubConsumerClient
import requests
import json
import pkg_resources

# Get the path to config file from command line argument
config_file = sys.argv[1]

# Read the config file
with open(config_file, "r") as f:
    config = json.load(f)


# Define function that will trigger a specific job
def trigger_job(job_id):
    # Construct the API request URL - get url and path from config file
    api_url = f"{config['workspace_url']}{config['run_job_api_path']}"

    # TODO: Get the access token from key vault
    # access_token = read_secret_from_keyvault(config['key_vault_url'], config['access_token_secret_name'])

    # Set the request headers
    headers = {
        "Authorization": f"Bearer {config['access_token']}",
        "Content-Type": "application/json"
    }

    # Trigger the job, i.e. make the API request
    response = requests.post(api_url, headers=headers, json={"job_id": job_id})

    # Handle the response
    if response.status_code == 200:
        print("Job successfully triggered")

        # Parse the response JSON
        response_json = json.loads(response.text)
        run_id = response_json["run_id"]
        print("Run ID: ", run_id)
    else:
        print(f"Error triggering job: {response.text}")


# Define the callback function
def on_event(partition_context, event):
    print("Received event from partition: ", partition_context.partition_id)
    print("Event body: ", event.body_as_str())
    print("Event properties: ", event.properties)
    print("Event sequence number: ", event.sequence_number)
    print("Event offset: ", event.offset)
    print("Event enqueued time: ", event.enqueued_time)

    trigger_job(config['job_id'])
    # TODO invoke job1
    # TODO invoke job2

    # Update the checkpoint so that the app doesn't read the same event again
    # partition_context.update_checkpoint(event)


print(f"Event hub connection string: {config['event_hub_connection_str']}")
print(f"Event hub name: {config['event_hub_name']}")
print(f"Event hub consumer group: {config['event_hub_consumer_group']}")

# Create the client object that will consume events from Event Hub
client = EventHubConsumerClient.from_connection_string(
    config['event_hub_connection_str'],
    config['event_hub_consumer_group'],
    eventhub_name=config['event_hub_name']
)
print("Client created")

# Listen continuously for events on the EventHub
print("Listening for events...")
with client:
    client.receive(on_event=on_event)
