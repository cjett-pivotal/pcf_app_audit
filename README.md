A script to consume the [cf-orgs-usage API](https://github.com/cbusch-pivotal/cf-orgs-usage) and print out Organization and Space usage (number of apps and instances)

## Usage

```
#> python pcf_app_audit.py
```
```
Usage API URL? <http(s)://usage-api.example.com>: https://cf-orgs-usage.apps.home.local
Using basic auth? <y/n>y
Username: admin
Password: <password>
```

## Output
The script will write the output to the terminal as well as output a file `app_usage.csv`


Org	| Space	| # Apps	| # Instances
---	| -----	| ------	| -----------
p-spring-cloud-services	| instances	| 112	| 204
system	| p-spring-cloud-services	| 2	| 2
system	| pivotal-services	| 1	| 0
system	| SMOKE-1-SPACE-c2fe1929de941a1a	| 1	| 1
system	| autoscaling	| 4	| 6
