# c4tfun
[c4tdotfun] is a CNT X bot that will post any new CNT created on snekdotfun.

# Redhat 9 Guide

# Install Virtual Environment 
1) sudo dnf groupinstall "Development Tools"
2) sudo dnf install python3-devel
3) sudo dnf install python3-pip
4) pip3 install virtualenv
5) python3 -m venv venv
6) source venv/bin/activate
7) sudo yum update
8) sudo yum install git
9) git clone [thisrepo]

# Run bot using tmux
1) sudo dnf install tmux
2) tmux new -s bot_session
3) source venv/bin/activate
4) python app.py
5) Press Ctrl + b, then type :detach and press Enter [to detach]
6) tmux attach-session -t bot_session [To reconnect]

# Troubleshoot SSL issue

# Suppress InsecureRequestWarning
```
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#add below code to each api url request
response = requests.get(details_url, verify=False)
response = requests.get(image_url, verify=False)
```

