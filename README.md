# superestart
A supervisord plugin used to autorestart program by specific time.

Updated 2021-09-08 onward by Daniel Pittman <daniel@rimspace.net>

main changes: make it work with modern python and supervison(-win) :)

## Usage

```
[eventlistener:superestart]
command=superestart --crontab "0 1 * * *" --group_name foo --api_endpoint "127.0.0.1:9009"
events=TICK_5
```
