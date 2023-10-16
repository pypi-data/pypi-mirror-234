# Ready Signal API - Python 3.6+
This library is designed to be a wrapper for the Ready Signal API: http://app.readysignal.com

Please direct all questions and/or recommendations to support@readysignal.com

<br>

# Table of Contents
* [Installation](#installation)
### Signal ID Specific
* [List Signals](#list-signals)
* [Signal Detatils](#signal-details)
* [Signal Output](#signal-output)
* [Delete Signal](#delete-signal)
* [Auto Discover Feature](#auto-discover-feature)
### Feature ID Specific
* [Available Features List](#available-features-list)
* [Show Features Data](#show-features-data)
* [Show Features Data Detailed](#show-features-detailed-data)
* [Features Data Output](#feature-data-outputs)

<br>

<br>

## Installation
The Ready Signal API Python library can be found here: https://pypi.org/project/readysignal/
```
pip install readysignal
```

<br>

## Usage

Your **access token** and **signal ID** can be found on your "Manage Signal" page within the Output information.

Your signal ID is also visible within the URL of the "Manage Signal" page:
```
...readysignal.com/signal/SIGNAL_ID/manage
```
<br>

### Setup

```python
import readysignal as rs

access_token = "your access token"
signal_id = 0  # this is your unique signal id number
```

<br>

## * Signal ID Specific *
 <br>

### List Signals

Using your ```access_token```, you can list all signals and metadata that are associated with your Ready Signal account.

```python
rs.list_signals(access_token)
```

#### Example Output

```python
{'data': [{
    'id': 0, 
    'name': 'Signal Name', 
    'description': 'Signal Description', 
    'desired_geo_grain': 'Country', 
    'desired_time_grain': 'Month', 
    'start_at': '11/01/2019', 
    'end_at': '01/31/2020', 
    'created_at': '07/23/2020', 
    'updated_at': '07/28/2020', 
    'deleted_at': None, 
    'company': {
        'id': 0, 
        'chargebee_id': 'ID Hash', 
        'name': 'Company Name', 
        'plan_id': 0, 
        'plan_value_id': 0, 
        'subscription_status': 'active', 
        'created_at': '2020-07-23 13:20:17', 
        'updated_at': '2020-08-03 11:33:50', 
        'need_listining_webhook': 0, 
        'addon_users': None, 
        'notify_after_processing': 0
        }, 
    'user': {
        'id': 0, 
        'company_id': 0, 
        'name': 'Name', 
        'email': 'Email', 
        'email_verified_at': None, 
        'type': 'owner', 
        'active': 'yes', 
        'reactivate': 'no', 
        'created_at': '2020-07-23 13:20:17', 
        'updated_at': '2020-07-23 13:20:17', 
        'deleted_at': None
        }, 
    'industry': {
        'id': 1, 
        'name': 'Automotive', 
        'created_at': '2020-04-10 23:21:38', 
        'updated_at': '2020-04-10 23:21:38', 
        'deleted_at': None
        }, 
    'analysis_type': {
        'id': 3, 
        'name': 'Classification', 
        'created_at': '2020-04-10 23:21:45', 
        'updated_at': '2020-04-10 23:21:45', 
        'deleted_at': None
    }, 
    'output': {
        'json': 'https://app.readysignal.com/api/signals/0/output?format=json'}, 
        'links': {
        'self': 'https://app.readysignal.com/signal/0/manage', 
        'manage': 'https://app.readysignal.com/signal/0/manage'
        }
    },
    {
    'id': 1
    ...
    }
    ]
}
```

<br>

### Signal Details

Using your ```access_token``` and your ```signal_id``` you can view the details of a specific signal.

```python
# get signal details
rs.get_signal_details(access_token, signal_id)
```

#### Example Output

```python
{'data': {
    'id': 0, 
    'name': 'Signal Name', 
    'description': 'Signal Description', 
    'desired_geo_grain': 'Country', 
    'desired_time_grain': 'Month', 
    'start_at': '11/01/2019', 
    'end_at': '01/31/2020', 
    'created_at': '07/23/2020', 
    'updated_at': '07/28/2020', 
    'deleted_at': None, 
    'company': {
        'id': 0, 
        'chargebee_id': 'ID Hash', 
        'name': 'Company Name', 
        'plan_id': 0, 
        'plan_value_id': 0, 
        'subscription_status': 'active', 
        'created_at': '2020-07-23 13:20:17', 
        'updated_at': '2020-08-03 11:33:50', 
        'need_listining_webhook': 0, 
        'addon_users': None, 
        'notify_after_processing': 0
        }, 
    'user': {
        'id': 0, 
        'company_id': 0, 
        'name': 'Name', 
        'email': 'Email', 
        'email_verified_at': None, 
        'type': 'owner', 
        'active': 'yes', 
        'reactivate': 'no', 
        'created_at': '2020-07-23 13:20:17', 
        'updated_at': '2020-07-23 13:20:17', 
        'deleted_at': None
        }, 
    'industry': {
        'id': 1, 
        'name': 'Automotive', 
        'created_at': '2020-04-10 23:21:38', 
        'updated_at': '2020-04-10 23:21:38', 
        'deleted_at': None
        }, 
    'analysis_type': {
        'id': 3, 
        'name': 'Classification', 
        'created_at': '2020-04-10 23:21:45', 
        'updated_at': '2020-04-10 23:21:45', 
        'deleted_at': None
    }, 
    'output': {
        'json': 'https://app.readysignal.com/api/signals/0/output?format=json'}, 
        'links': {
        'self': 'https://app.readysignal.com/signal/0/manage', 
        'manage': 'https://app.readysignal.com/signal/0/manage'
        }
    }
}
```

<br>

### Signal Output
There are three different ways to receive your signal output:
* JSON
* Pandas DataFrame
* CSV export

### JSON
```python
# get signal data as json
rs.get_signal(access_token, signal_id)
```
#### Example Output
```python
{'current_page': 1, 
 'data': [
	{
		'start': '2019-11-01', 
		'end': '2019-11-30', 
		'country': 'United States of America', 
		'actual-snow-fall': '160205.00000000000000000000', 
		'resident-population-by-state': '9826013.22000000000000000000', 
		'actual-snow-cover': '3.56158109943317700000', 
		'population-total': '308745538.00000000000000000000', 
		'population-total-transformed': 17,571.156421818115497622280458798
	}, 
	{
		'start': '2019-12-01', 
		'end': '2019-12-31', 
		'country': 'United States of America', 
		'actual-snow-fall': '219691.00000000000000000000', 
		'resident-population-by-state': '10153546.99400000000000000000', 
		'actual-snow-cover': '8.28314041638492200000', 
		'population-total': '308745538.00000000000000000000', 
		'population-total-transformed': 17,571.156421818115497622280458798
	}, 
	{
		'start': '2020-01-01', 
		'end': '2020-01-31', 
		'country': 'United States of America', 
		'actual-snow-fall': '220869.00000000000000000000', 
		'resident-population-by-state': 10159386.99400000000000000000, 
		'actual-snow-cover': '10.69758409714073700000', 
		'population-total': '308745538.00000000000000000000', 
		'population-total-transformed': 17,571.156421818115497622280458798
	}
	], 
	'first_page_url': 'https://app.readysignal.com/api/signals/0/output?page=1', 
	'from': 1, 
	'last_page': 1, 
	'last_page_url': 'https://app.readysignal.com/api/signals/0/output?page=1', 
	'next_page_url': None, 
	'path': 'https://app.readysignal.com/api/signals/0/output', 
	'per_page': 1000, 
	'prev_page_url': None, 
	'to': 3, 
	'total': 3}
```

### Pandas DataFrame
```python
# get signal data as Pandas DataFrame
rs.get_signal_pandas(access_token, signal_id)
```
#### Example Output
```text
        start  ... population-total-transformed
0  2019-11-01  ... 17,571.156421818115497622280458798
1  2019-12-01  ... 18,109.798447234298274239287429023
2  2020-01-01  ... 18,732.472983479821748127047902849
```

### Export to CSV
```python
# send signal data to csv file
file_name = "test_signal.csv"
rs.signal_to_csv(access_token, signal_id, file_name)
```

### Delete Signal
**USE WITH CAUTION**

Use your ```access_token``` and ```signal_id``` to delete a signal
```python
rs.delete_signal(access_token, signal_id)
```

### Auto Discover Feature
Creates a signal using your own data and the Auto Discover feature. 
Please check Ready Signal site for tips on how to format your data. 
Currently only available at the *"State"* or *"Country"* geo grain and the *“Month”* or *“Day”* time grain. 
Use a file name OR Pandas DataFrame.
Set `create_custom_features=0` to prevent Ready Signal from storing the input target data for future use.

```python
rs.auto_discover(access_token, geo_grain, date_grain, filename=None, df=None, create_custom_features=1)
```

<br>

## * Feature ID Specific*

### Available Features List

Using your ```access_token```, you can view all the features and an overview of their data that can be used with the feature specific functions.

```python
rs.get_features_list(access_token)
```
#### Example Output

```python
{'data': [{'feature_id': 317,
   'slug_name': 'Bonos (0 - 3 years) Maturity at 12/07/2023',
   'feature_name': 'Bonos (0 - 3 years) Maturity at 12/07/2023',
   'product_name': 'Bonos',
   'provider_name': 'Bank Of Mexico',
   'geo_grain': 'Country',
   'geo_grain_delimitation': 'MEXICO',
   'date_grain': 'Day'},
  {'feature_id': 318,
   'slug_name': 'Bonos (0 - 3 years) Maturity at 09/05/2024',
   'feature_name': 'Bonos (0 - 3 years) Maturity at 09/05/2024',
   'product_name': 'Bonos',
   'provider_name': 'Bank Of Mexico',
   'geo_grain': 'Country',
   'geo_grain_delimitation': 'MEXICO',
   'date_grain': 'Day'},
   {'feature_id': 319
   ...
   }
]
}
```
<br>

### Show Feature(s) Data

Using your ```access_token``` and a ```feature``` list containing the feature id(s), see an overview of the data for those specific features.

```python
feat_list = [317, 318]
rs.show_feature(access_token, feat_list)
```

#### Example Output
```python
{317: {'feature_id': 317,
  'feature_name': 'Bonos (0 - 3 years) Maturity at 12/07/2023',
  'product_name': 'Bonos',
  'provider_name': 'Bank Of Mexico',
  'geo_grain': 'Country',
  'date_grain': 'Day',
  'data_notes': None,
  'units': 'Millions of pesos',
  'available_through': '2023-09-26',
  'published_at': None},
 318: {'feature_id': 318,
  'feature_name': 'Bonos (0 - 3 years) Maturity at 09/05/2024',
  'product_name': 'Bonos',
  'provider_name': 'Bank Of Mexico',
  'geo_grain': 'Country',
  'date_grain': 'Day',
  'data_notes': None,
  'units': 'Millions of pesos',
  'available_through': '2023-09-26',
  'published_at': None}}
```
<br>

### Show Feature(s) Detailed Data

Using your ```access_token``` and a ```feature``` list containing the feature id(s), see in depth data for those specific features.

```python
feat_list = [317]
rs.show_feature(access_token, feat_list)
```

#### Example Output
```python
{317: {'name': 'Bonos (0 - 3 years) Maturity at 12/07/2023',
  'short_name': 'Bonos (0 - 3 years) Maturity at 12/07/2023',
  'geo_grain': 'Country',
  'geo_grain_label': 'COUNTRY',
  'geo_grain_delimitation': 'MEXICO',
  'date_grain': 'Day',
  'date_grain_label': 'Daily',
  'licence': 'Public Domain',
  'units': 'Millions of pesos',
  'reporting_lag': '1 Day',
  'first_date': None,
  'description': '',
  'citation': None,
  'why_use': None,
  'state_lvl_data_set_exist': 'No',
  'is_state_lvl_the_same': 'No',
  'allow_grain_transformation_by_date': 'Yes',
  'allow_grain_transformation_by_population': 'No',
  'parent_feature_id': None,
  'product': {'id': 104,
   'name': 'Bonos',
   'created_at': None,
   'updated_at': None,
   'deleted_at': None,
   'provider': {'id': 41,
    'name': 'Bank Of Mexico',
    'publisher_id': 7,
    'created_at': '2022-07-14 14:06:07',
    'updated_at': '2022-07-14 14:06:07',
    'deleted_at': None}},
  'categories': [{'id': 1,
    'name': 'Economic',
    'created_at': '2020-04-10T23:22:58.000000Z',
    'updated_at': '2020-04-10T23:22:58.000000Z',
    'deleted_at': None,
    'sub_categories': [{'id': 1,
      'name': 'Banking',
      'category_id': 1,
      'created_at': '2020-04-10 23:22:58',
      'updated_at': '2020-04-10 23:22:58',
      'deleted_at': None},
     {'id': 2,
      ...
     }
     {'id': 18,
      'name': 'Interest Rates',
      'category_id': 1,
      'created_at': '2020-04-10 23:23:06',
      'updated_at': '2020-04-10 23:23:06',
      'deleted_at': None}]}],
  'deleted_at': None,
  'created_at': '2023-07-10T17:40:50.000000Z',
  'updated_at': '2023-09-19T18:02:05.000000Z'}
  }
```
<br>

### Feature Data Outputs
There are two different ways to receive your feature(s) data:
* JSON
* Pandas DataFrame

You will need your ```access_token```,```feature``` list of feature ids along with a ```start_date``` and ```end_date``` indicating the date range of the features

### JSON
```python
# get feature data as json
rs.get_feature_data(access_token, feature, start_date, end_date)
```
#### Example Output
```python
{'data': [{'Trade Date': '01/04/2021',
   'Security Type': 'Bonos',
   'Maturity Date': '07 dic 2023',
   'Volume': '0.00000000000000000000',
   'Maturity Bucket': '0_3',
   'Last Updated': '09/26/2023'},
  {'Trade Date': '01/05/2021',
   'Security Type': 'Bonos',
   'Maturity Date': '07 dic 2023',
   'Volume': '100.00000000000000000000',
   'Maturity Bucket': '0_3',
   'Last Updated': '09/26/2023'},
   ...
   {'Trade Date': '12/31/2021', 
   'Security Type': 'Bonos', 
   'Maturity Date': '07 dic 2023', 
   'Volume': '0.00000000000000000000', 
   'Maturity Bucket': '0_3', 
   'Last Updated': '09/26/2023'}
   ]
}
```
### Pandas DataFrame
```python
# get feature data as Pandas DataFrame
rs.get_feature_data_pandas(access_token, feature, start_date, end_date)
```
#### Example
```text
   Trade Date  ... Last Updated
0  01/04/2021  ... 09/26/2023
1  01/05/2021  ... 09/26/2023
2  01/06/2021  ... 09/26/2023
```
