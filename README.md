# DevOps and AI on AWS: CloudWatch Anomaly Detection

## Overview
This project explores using Amazon CloudWatch anomaly detection to monitor and detect unusual patterns in application metrics. The objective is to enable anomaly detection for a metric, configure alarms based on expected values, and utilize both the AWS Command Line Interface (AWS CLI) and a Python script to retrieve and post custom metrics.

___
## Problem Statement

Applications generate a continuous stream of metrics, such as a count of currently logged-in users, which often follow a predictable pattern of values over a 24-hour period. Relying on static thresholds for alarms is inefficient because they cannot dynamically adapt to these expected daily fluctuations, making it difficult to surface true anomalies without manual user intervention.

___
## Problem Reframing & Requirements

To effectively monitor application health and troubleshoot performance issues, the monitoring solution requires:
* The ability to automatically identify unusual patterns in an application's behavior.
* Configuration of alarms that compare a metric's value to an expected value based on an anomaly detection model rather than a static threshold.
* The capability to monitor application-specific data points, such as memory usage by process, that are not available through default CloudWatch metrics.

___
## Solution & Tool Tradeoffs

The chosen solution leverages Amazon CloudWatch's native anomaly detection and custom metric capabilities.

**Tradeoffs Considered:**
* **CloudWatch Anomaly Detection vs. Static Alarms:** CloudWatch anomaly detection applies statistical and machine learning algorithms to continuously analyze metrics and determine normal baselines. This provides a more sophisticated monitoring solution that automatically adapts to application patterns, whereas static thresholds would trigger false alarms during expected peak usage times.
* **Custom Metrics via Python vs. Default Metrics:** Posting custom metrics enables detailed observability into specific processes (like memory used by nginx and AWS Systems Manager Agent), which makes diagnosing issues like out-of-memory exceptions much easier to scale.

___
## Architecture

* Compute & Application: Simulated instances running nginx and the AWS Systems Manager Agent (SSM Agent).
* Monitoring & Alerts: Amazon CloudWatch for tracking metrics, applying the `ANOMALY_DETECTION_BAND` math function, and triggering alarms.
* Automation & Operations: AWS CLI for retrieving alarm details and a Python script (`custom-memory-metrics.py`) running in a Visual Studio Code IDE to post custom metrics.

___
## Data Assets & Schemas

The monitoring setup utilizes specific CloudWatch namespaces and dimensions to organize related metrics:
* **TravelApplication Namespace:** Contains the `UserLogins` metric, which tracks a predictable pattern of user logins over a 24-hour period.
* **HostResources Namespace:** Contains custom metrics for `MemoryUsage`.
* **Dimensions:** Custom metrics are categorized using `Hostname` and `ProcessName` key-value pairs to create unique identities for the metrics.

___
## Pipeline Execution Flow

The implementation follows a structured progression to set up, test, and observe anomaly detection:

1. **Alarm Creation:** Enabled anomaly detection and created a CloudWatch alarm named `logins-alarm` for the `UserLogins` metric within the `TravelApplication` namespace.
2. **Metric Retrieval:** Used the AWS CLI (`describe-anomaly-detectors` and `get-metric-data`) to retrieve alarm settings and observe the `ANOMALY_DETECTION_BAND` function, which calculates the upper and lower limits of the expected values.
3. **Custom Metric Posting:** Executed a Python script to post custom memory usage metrics for `nginx` and `amazon-ssm-agent` processes every 60 seconds.
4. **Alarm Observation:** Navigated to the CloudWatch console to observe the alarm state, verifying that the alarm transitioned when a spike in the `UserLogins` metric went outside the expected gray anomaly detection band.
5. **History Correlation:** Reviewed the alarm's History tab to observe the time and description of state changes to correlate events.

___
## Security & Roles

* Environment Access: Operations are performed within a provisioned lab environment utilizing secure login credentials to access a VS Code IDE workspace.
* Programmatic Access: The AWS CLI and Python scripts utilize API calls (such as `put_metric_data`) to post and retrieve telemetry data from Amazon CloudWatch.

___
## Business Outcomes & Analytical Outputs

* Automated Incident Response: Implemented automated anomaly detection to reduce the time required to identify and respond to unusual application behavior.
* Adaptive Monitoring: Replaced brittle static alarms with machine-learning-backed anomaly detection bands that adapt to the application's expected 24-hour patterns.
* Deep Observability: Gained detailed visibility into application health by posting custom memory metrics, enabling administrators to easily diagnose process-level performance issues.
