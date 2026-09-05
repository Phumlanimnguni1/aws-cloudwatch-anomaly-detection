import psutil
import socket
import boto3
from time import sleep


# Create a CloudWatch client
cloudwatch = boto3.client('cloudwatch')

def get_memory_usage_by_process_names(process_names):
    "Get memory usage by process names"
    results = {}
    # retrieve the process list
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        process_name = proc.info['name']
        # build a dictionary of process name and total memory usage
        if process_name in process_names:
            if not process_name in results:
                results[process_name] = proc.info['memory_info'].rss
            else:
                results[process_name] += proc.info['memory_info'].rss
    return results


# determine the hostname
hostname = socket.gethostname()
while True:
    # get message usage for nginx and ssm-agent
    processes = get_memory_usage_by_process_names(['nginx', 'amazon-ssm-agent'])
    for process in processes:
        # post a metric for the memory usage
        # with hostname and process name as dimensions
        response = cloudwatch.put_metric_data(
            Namespace="HostResources",
            MetricData=[
                {
                    'MetricName': "MemoryUsage",
                    'Dimensions': [
                        {
                            'Name': 'Hostname',
                            'Value': hostname
                        },
                        {
                            'Name': 'ProcessName',
                            'Value': process
                        }
                    ],
                    'Value': processes[process],
                    'Unit': "Bytes"
                }
            ]
        )
        print(f"posted metric for {hostname} {process} {processes[process]}")
    sleep(60)