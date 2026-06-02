[![Build Status](https://dev.azure.com/tsacc-msfwex01-16-rusmos01-it-ba/GTP_Infra/_apis/build/status%2FGTP_Infra?repoName=GTP_Infra&branchName=develop)](https://dev.azure.com/tsacc-msfwex01-16-rusmos01-it-ba/GTP_Infra/_build/latest?definitionId=319&repoName=GTP_Infra&branchName=develop)

# JTI Global Template
This project intends to be a default platform to stablish communication with the independent tobacco trade peers.

## Setup
0. sh install.sh

## Required Tools
* Node.js 8.11.3
* MongoDB 3.4.4
* Redis 4.0.10

## Additional References
* Material-UI - [material-ui.com](https://material-ui.com/)

## Environments
|environment    |ip                              |url                        |basic auth |os             |
|:--------------|:-------------------------------|:--------------------------|:----------|:--------------|
|development    |-                               |-                          |no         |mac            |
|staging        |-                               |-                          |?          |-              |
|production     |-                               |-                          |?          |-              |

## Releated Accounts
|user                |password         |type               |description                                  |
|:-------------------|:----------------|:------------------|:--------------------------------------------|
|?                   |[n/a,use keys]   |SSH                |system root user                             |

## IssueTracker
http://agile.sensory-minds.com/issues/jtitopgt


## Maintainers
* Sascha Strohmeier <s.strohmeier@sensory-minds.com>
* Dietmar Weiß <d.weiss@sensory-minds.com>
* Jorge Ramirez <j.ramirez-hernandez@sensory-minds.com>
* José Gonçalves <j.goncalves@sensory-minds.com>


## Magic Snippets 
Backup Database
* ```$ mongodump --archive --gzip --db=jtitrade > dump.gz```

Database Restore
* ```$ mongorestore --drop --archive=dump.gz --gzip --db=jtitrade```

## FileSystem
For configuration and data storage, the following file system structure is used:

set the following config variables:
* ```fileSystem: "minio"| emty```

### Minio
set the following config variables:
* ```fileSystem: "minio"```
* ```minio: ```
  * ```host: 'localhost'```
  * ```port: PORT```
  * ```accessKey: '************'```
  * ```secretKey: '************'```
  * ```useSSL: boolean```
  * ```manualBucket: string``` (optional) set a bucket name to use for all files
  * ```removePath: string``` (optional) remove a path from the file path before saving or use it to the bucket


