---
id: alerts
title: Alerts
sidebar_label: Alerts
---

From a soil application it is possible to trigger events and be subscribed to them. For example a client may want to recieve an SMS when the expected bed occupancy for the emergency department is higher than 90% or we as app developers may want to recieve an email warning us that the data did not arrive today.

Soil uses [Elastalert](https://elastalert2.readthedocs.io/en/latest/) as alerts backend and all the rule and alert types should be compatible.

## Alerts Data Model

### Events
Represent a triggered element. They can be created from a script, from a module or via the HTTP API. They have a key and a value.

```python
from soil.alerts import event

event('expected_occupancy', 125)
```

They have a key and a value.

```json
POST soil.amalfianalytics.com/api/v2/alerts/events/
{
    "key": "test_event1",
    "value": 6
}
```
### Alerts
Alerts bind an event key with a condition. They can also define a paramatrized message.

```json
POST soil.amalfianalytics.com/api/v2/alerts/alerts/
{
    "role": "user_role",
    "event_key": "my_event",
    "condition" : {
        "type" : "metric",
        "min_threshold" : 5,
        "max_threshold" : 10
    },
    "message": "Event {0} had value of {1} at {2}.",
    "title": "Alert for {0} trigged."
}
```

The parameters for the message and title are: {0} event_key, {1} value, {2} timestamp (ISO formatted). Only the admins for a role can create alarms. [Here you can find documentation for conditions](https://gitlab.com/amalfianalytics/soil/soil/alerter/-/blob/master/docs/user_guide.md).

### Connections
The connections contain the configuration to send the message to a device or service. Users can create their own subscriptions. There are two types of configuration parameters:
 * Fixed parameters: that are configured in the deployment. For example: smtp server and credentials.
 * User parameters: Parameters that can change from user to user. For example the recipient email. These are defined at the connection_value.

 You can see all available connection types at the [alerter section in Elastalert](https://elastalert2.readthedocs.io/en/latest/ruletypes.html#alerter) but it should be enabled in the server configuration.

```json
POST soil.amalfianalytics.com/api/v2/alerts/connections/
{
    "connection_type": "slack",
    "connection_value": {
        "slack_webhook_url" : "https://hooks.slack.com/services/...."
    }
}
```

### Subscriptions
Subscriptions are the link between the connections and the alerts.

```json
POST soil.amalfianalytics.com/api/v2/alerts/subscriptions/
{
    "connection_id": "609a3f2babafa61f388bb8a5",
    "alert_id":      "609a3f3aabafa61f388bb8a6"
}
```
