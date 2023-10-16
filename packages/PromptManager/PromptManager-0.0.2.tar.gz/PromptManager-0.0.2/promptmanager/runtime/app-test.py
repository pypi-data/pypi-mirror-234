process_name = '123'
cmd = 'ps aux | grep ' + process_name + ' | grep -v grep | awk "{{print $2}}"'
print(cmd)