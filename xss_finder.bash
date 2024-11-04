# XSS Vulnerability Testing Tool

# This script is designed to automate the testing of web applications for Cross-Site Scripting (XSS) vulnerabilities.
# It performs the following functions:

# Usage:
# - Ensure that `subdomains.txt`, `parameters.txt`, and `xss_payloads.txt` are prepared with the necessary data.
# - Execute the script in a Bash environment to perform the tests.

for one_domain in $(cat subdomains.txt); do
    for one_param in $(cat parameters.txt); do
        while IFS= read -r one_payload; do
            # URL encode spaces and tags in the payload
            encoded_payload=$(echo "$one_payload" | sed -e 's/ /%20/g' -e 's/</%3C/g' -e 's/>/%3E/g' -e 's/"/%22/g' -e "s/'/%27/g")

            # Sending request with the payload and checking if it’s reflected in the response
            if curl -s "$one_domain?$one_param=$encoded_payload" | grep -q "$one_payload"; then
                echo "There is XSS in $one_domain?$one_param=$encoded_payload"
            fi
        done < xss_payloads.txt
    done
done

