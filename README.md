# 🔧 Github-Automation-Tools
Tools to automate certain tasks

## Instalation
```
pip install -r requirements.txt
```

## Instructions
### Total Time
Create an issue with the total time from all the others opened issues.
In the body of the issues you should have something like that:

```
Issue description
...
Time : 4h
```
Or
```
Issue description
...
Time : 2h - 1,5d
```
Or
```
Issue description
...
Time : 30m/task
```

Add your `credentials` to `getTimeFromIssues.py`:
```
credentials = {
	'login_username': 'LOGIN',
	'password': 'YOUR_PASSWORD',
	'repo': 'USERNAME/REPO_NAME',
	'assignee': 'ASSIGNEE_NAME'
}
```

And then run the script:
```
python getTimeFromIssues.py
```


