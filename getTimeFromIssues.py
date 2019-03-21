from github import Github
import re

credentials = {
	'login_username': 'LOGIN',
	'password': 'YOUR_PASSWORD',
	'repo': 'USERNAME/REPO_NAME',
	'assignee': 'ASSIGNEE_NAME'
}

git = Github(credentials['login_username'], credentials['password'])

repo = git.get_repo(credentials['repo'])
labels = repo.get_labels()
issues = repo.get_issues(state='open')

range_by_labels = {label.name: {'min': 0, 'max': 0} for label in labels}
total_min_range = int()
total_max_range = int()

min2sec = lambda minutes: float(minutes.replace(',', '.')) * 60.0
hour2sec = lambda hours: float(hours.replace(',', '.')) * 60.0 * 60.0
day2sec = lambda days: float(days.replace(',', '.')) * 24.0 * 60.0 * 60.0


def toSec(number, unit):
	# if minutes
	if unit == 'm':
		return min2sec(number)
	
	# if hour
	if unit == 'h':
		return hour2sec(number)
	
	# if days
	if unit == 'd':
		return day2sec(number)


def main():
	global issues
	global total_max_range
	global total_min_range
	global range_by_labels

	for issue in issues:
		desc = issue.body

		time_str = re.search('Time : (.*)', desc)
		if not time_str:
			continue

		time = time_str.group(1)
		pattern = re.search(
			'([0-9,.]{1,3}(m|d|h))( - ([0-9,.]{1,3}(m|d|h)))?( ?/ ?[a-zA-Z]+)?', time)
		if not pattern:
			continue
		
		min_range = int()
		max_range = int()
		unitMin = str()
		unitMax = str()
		
		# 30m, 4h, ...
		if not pattern.group(3) and not pattern.group(6):
			max_range = min_range = re.search('([0-9,.]+)', pattern.group(1)).group(1)
			unitMax = unitMin = pattern.group(2)
		# 4h/test, 2d / task
		elif not pattern.group(3) and pattern.group(6):
			max_range = min_range = str(float(re.search('([0-9,.]+)', pattern.group(1)).group(1)) * 5)
			unitMax = unitMin = pattern.group(2)
		# 3h - 6,5d
		elif pattern.group(3):
			min_range = re.search('([0-9,.]+)', pattern.group(1)).group(1)
			max_range = re.search('([0-9,.]+)', pattern.group(4)).group(1)
			unitMin = pattern.group(2)
			unitMax = pattern.group(5)

		min_range = toSec(min_range, unitMin)
		max_range = toSec(max_range, unitMax)

		issue_labels = issue.get_labels()

		range_by_labels[issue_labels[0].name]['min'] += min_range
		range_by_labels[issue_labels[0].name]['max'] += max_range
		
		total_min_range += min_range
		total_max_range += max_range


def setTotalTime():
	global total_max_range
	global total_min_range
	global range_by_labels
	global repo
	global credentials

	title = 'Total time : {}h - {}h'.format(
		int(total_min_range / 60 / 60), int(total_max_range / 60 / 60))
	
	body = str()
	for label, ranges in range_by_labels.items():
		hoursMin = int(ranges['min'] / 60 / 60)
		hoursMax = int(ranges['max'] / 60 / 60)

		if hoursMin == 0:
			continue
		
		if hoursMin == hoursMax:
			body += "**{}**: {}h\n".format(label, hoursMin)
		else:
			body += "**{}**: {}h - {}h\n".format(label, hoursMin, hoursMax)

	repo.create_issue(title=title, body=body, assignee=credentials['assignee'])


if __name__ == "__main__":
	main()
	setTotalTime()
