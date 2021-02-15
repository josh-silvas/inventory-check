# Get Alerts for PS5 availability

## Development
Start in `main.py` to see the flow the app. 

## Deployment
    
    crontab -e
 
    */2 * * * * /path/to/code/operationPS5/check.sh > /path/to/code/operationPS5/cronresult.log
