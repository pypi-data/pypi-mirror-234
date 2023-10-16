Netorca SDK
===========

The NetOrca SDK is a powerful tool that allows developers to seamlessly
integrate and interact with the NetOrca API, simplifying the management
of various aspects of the NetOrca platform. This documentation provides
comprehensive guidance on using the SDK to access NetOrca’s features and
data.

Overview
--------

The NetOrca SDK offers a set of Python classes and methods that
facilitate communication with the NetOrca API. It provides an
abstraction layer for authentication, making API calls, and handling
responses, enabling developers to focus on building applications and
services that leverage NetOrca’s capabilities.

Prerequisites
-------------

Before using this code, ensure you have the following:

-  NetOrca API Key: You’ll need an API key to authenticate with the
   NetOrca API.
-  URL: The URL for the NetOrca API.
-  Python Environment: Make sure you have Python installed on your
   system.

Installation
------------

First, you need to install the NetOrca SDK if you haven’t already. You
can install it using pip:

.. code:: bash

   pip install netorca-sdk

Sample Code
-----------

.. code:: python

   # Import necessary modules
   import os
   from netorca_sdk.auth import NetorcaAuth
   from netorca_sdk.netorca import Netorca

   # Initialize the authentication object with your API key and API URL
   netorca_auth = NetorcaAuth(api_key=os.environ["api_key"], fqdn=os.environ["url"])

   # Create an instance of the Netorca class with the authentication object
   netorca = Netorca(auth=netorca_auth)

   # Define filters to narrow down the search
   filters = {"service_name": "name_of_the_service"}

   # Retrieve information about services using the defined filters
   services_info = netorca.get_services(filters=filters)

   # Print the result
   print(services_info)

1. Create Deployed Item
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Create a new deployed item associated with a change instance
   change_instance_id = 123  # Replace with the actual change instance ID
   description = {"key": "value"}  # Replace with the desired description data
   result = netorca.create_deployed_item(change_instance_id, description)
   print("Created Deployed Item:", result)

2. Get Deployed Item
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific deployed item by its ID
   deployed_item_id = 456  # Replace with the actual deployed item ID
   result = netorca.get_deployed_item(deployed_item_id)
   print("Deployed Item Information:", result)

3. Get Deployed Items
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of deployed items with optional filters
   filters = {"filter_key": "filter_value"}  # Replace with desired filters, or set to None
   result = netorca.get_deployed_items(filters)
   print("Deployed Items:", result)

4. Get Service Items
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of service items with optional filters
   filters = {"filter_key": "filter_value"}  # Replace with desired filters, or set to None
   result = netorca.get_service_items(filters)
   print("Service Items:", result)

5. Get Services
~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of services with optional filters
   filters = {"filter_key": "filter_value"}  # Replace with desired filters, or set to None
   result = netorca.get_services(filters)
   print("Services:", result)

6. Get Service Item
~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific service item by its ID
   service_item_id = 789  # Replace with the actual service item ID
   result = netorca.get_service_item(service_item_id)
   print("Service Item Information:", result)

7. Get Change Instance
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific change instance by its ID
   change_instance_id = 1234  # Replace with the actual change instance ID
   result = netorca.get_change_instance(change_instance_id)
   print("Change Instance:", result)

8. Get Change Instances
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of change instances with optional filters
   filters = {"filter_key": "filter_value"}  # Replace with desired filters, or set to None
   result = netorca.get_change_instances(filters)
   print("Change Instances:", result)

9. Update Change Instance
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Update information of a specific change instance by its ID
   change_instance_id = 5678  # Replace with the actual change instance ID
   update_data = {"key": "new_value"}  # Replace with the data you want to update
   result = netorca.update_change_instance(change_instance_id, update_data)
   print("Updated Change Instance:", result)

10. Get Service Config
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve information about a specific service config by its ID
   service_config_id = 9012  # Replace with the actual service config ID
   result = netorca.get_service_config(service_config_id)
   print("Service Config Information:", result)

11. Get Service Configs
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Retrieve a list of service configs with optional filters
   filters = {"filter_key": "filter_value"}  # Replace with desired filters, or set to None
   result = netorca.get_service_configs(filters)
   print("Service Configs:", result)

12. Create Service Config
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # Create a new service config with the provided data
   config_data = {"key": "value"}  # Replace with the data for the new service config
   result = netorca.create_service_config(config_data)
   print("Created Service Config:", result)

Replace the placeholder values in each example with the actual data or
IDs you want to use in your interactions with the Netorca API. These
examples demonstrate how to use the various functions provided by the
``Netorca`` class to perform different operations.

Usage
-----

1. Replace ``"api_key_here"`` and ``"api_url_here"`` in the code with
   your actual API key and API URL.

2. Run the Python script to execute the code. It will make a request to
   the Netorca API and retrieve information about services that match
   the specified filters.

3. The result will be printed to the console.

Additional Information
----------------------

-  You can customize the ``filters`` dictionary to filter services based
   on your requirements.

-  For more details on available API endpoints and methods, refer to the
   NetOrca API documentation.

-  Ensure you have the necessary environment variables set for the API
   key and URL before running the code.

Updates
-------

This SDK will aim to always be released in line with the latest NetOrca
version but does not provide any guarantees.

License
-------

This code is provided under the `MIT License <LICENSE>`__.
