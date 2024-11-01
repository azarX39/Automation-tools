# XSS Vulnerability Testing Tool

# This script is designed to automate the testing of web applications for Cross-Site Scripting (XSS) vulnerabilities.
# It performs the following functions:

# Usage:
# - Ensure that `subdomains.txt`, `parameters.txt`, and `xss_payloads.txt` are prepared with the necessary data.
# - Execute the script in a Bash environment to perform the tests.

for one_domain in $(cat subdomains.txt); do
    for one_param in $(cat parameters.txt); do
        while IFS= read -r one_payload; do
            curl -s "$one_domain?$one_param=$one_payload" | grep -q "$one_payload" && \
            echo "There is XSS in $one_param on $one_domain using payload: $one_payload" || \
            echo "No XSS in $one_param on $one_domain with payload: $one_payload"
        done < xss_payloads.txt
    done
done
