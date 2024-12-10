# GOCAutomation Platform

## Project Overview

> **GOCAutomation platform** is a comprehensive, integrated solution that helps you automate for velocity, collaboration, and growth. The platform automates common operation tasks so we can focus on the higher-value work.
It integrates basic information for GOC managed hosts and automation functions based on external interfaces like `ICINGA2, NetIQ, Ansible, RB-PAM` etc.

<br/>

## Project technology stack

| Name                  | Comment                     			 |
| --------------------- | -------------------------------------- |
| Python                | Backend development language           |
| Django                | Django Web development framework       |
| Javascript            | Front-end dev language                 |
| Bootstrap             | Front-end framework     				 |
| MySQL                 | MySQL database             			 |
| Redis                 | Redis cache database         			 |
| ICINGA2               | ICINGA2 API           				 |
| NETIQ                 | NETIQ API       						 |
| Ansible               | Ansible API             				 |
| HPE iLO               | HPE iLO Restful API                 	 |

<br/>

## Project Architecture Diagram

![GOC_Automation_Diagram](https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/boc_automation/raw/Intro/GOC_Automation_Diagram.png?at=refs%2Fheads%2Fmaster)

<br/>

## Initial development environment

| Env / Tool 			| Version                | Comment             |
| --------------------- | ---------------------- | ------------------- |
| Python      			| 3.7.0               	 | Python Interpreter  |
| Django      			| 3.2.15              	 | Django Framework    |
| Django Templates      | 2.10                   | Templates engine    |
| VS Code     			| 1.73.1			     | IDE Editor  	       |
| MySQL       			| 5.7.39                 | MySQL Database      |
| Redis       			| 4.0.6                  | Cache Database      |

<br/>

The above is the initial development environment of the project. The third-party library environment required by the project is in the `requirements.txt` file under `GOC_Automation`. All can be installed using the following command.

```python
pip install -r requirements.txt
```

<br/>

## Project Main Page

![main_page](https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/raw/Intro/main_page_screenshot.png?at=refs%2Fheads%2Fmaster)

<br/>

## Project environment construction and deployment
```
1. Prepare the `Docker` environment for the project

2. Use docker-compose to deploy the project

redis:
  image: redis:4.0.6
  ports:
    - "6379:6379"

mysql:
  image: mysql:5.7.39
  ports:
    - "3306:3306"

web:
  image: goc_automation_web:1.2
  ports:
    - "9999:9999"

nginx:
  image: nginx:1.14.1
  ports:
    - "80:80"
    - "443:443"
```

<br/>
<br/>
## Reference

[Ansible API Documentation](https://docs.ansible.com/ansible/latest/api/index.html)<br/>
[HPE iLO Redfish API Reference](https://hewlettpackard.github.io/ilo-rest-api-docs/ilo5/#traversing-the-data-model)<br/>
[ICINGA2 Monitoring Documentation](https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/)<br/>
[NetIQ Monitoring API Documentation](https://rb-netiqws-sl4.de.bosch.com:9996/QdbAddonWebService/qdbaddon.asmx)<br/>
[CyberArk PAM Developer Documentation](https://docs.cyberark.com/Product-Doc/OnlineHelp/PAS/Latest/en/Content/HomeTilesLPs/LP-Tile5.htm?tocpath=Developer%7C_____0)

<br/>

