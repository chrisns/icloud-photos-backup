# iCloud Photos backup
[![Security Scanning](https://github.com/chrisns/icloud-photos-backup/actions/workflows/security.yml/badge.svg)](https://github.com/chrisns/icloud-photos-backup/actions/workflows/security.yml)
[![Docker Image CI](https://github.com/chrisns/icloud-photos-backup/actions/workflows/dockerimage.yml/badge.svg)](https://github.com/chrisns/icloud-photos-backup/actions/workflows/dockerimage.yml)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=bugs)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=chrisns_icloud-photos-backup&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=chrisns_icloud-photos-backup)
[![Known Vulnerabilities](https://snyk.io/test/github/chrisns/icloud-photos-backup/badge.svg)](https://snyk.io/test/github/chrisns/icloud-photos-backup)



> a tool to backup your photos from iCloud

Like many others I keep all my family photos in Photos and take comfort that Apple handle the storage + backup.

However something got me worried, _what if_ I got infected with some ransomware that encrypted or destroyed my photos, from an attack point of view, that'd probably be a pretty lucrative attack.

Or what if the pictures I have of my kids were misclassified by a well intentioned Apple and I lost access to the originals like [this guy](https://news.yahoo.com/dad-took-photos-naked-toddler-142928196.html) did with his google life.

## Usage

###
```bash
mkdir -p session keyring photos
### Get or renew a login session with 2FA

docker run \
  --rm -ti \
  -v ${PWD}/session:/tmp/pyicloud \
  -v ${PWD}/keyring:/home/app/.local/share/python_keyring \
  -e USERNAME="xxx@mac.com" \
  ghcr.io/chrisns/icloud-photos-backup

# If it works this should start downloading photos, but they're only going to a docker volume, not to your host machine to ^C to exit

docker run \
  --name photobackup \
  -d \
  -v ${PWD}/backup:/app/photos \
  -v ${PWD}/keyring:/home/app/.local/share/python_keyring \
  -v ${PWD}/session:/tmp/pyicloud \
  -e USERNAME="xxx@mac.com" \
  ghcr.io/chrisns/icloud-photos-backup

# you can follow the logs to see progress, initial backup could take a LONG time (days-weeks)
docker logs -f photobackup

# you can then maybe add a cron job to do:

docker start -a photobackup
```

## But I don't trust you [@chrisns](@chrisns) with my credentials

No, why on earth would you, you'd be mad to blindly run the above docker command, so I'd really urge you to pull this repo, check all the dependencies and use very much at your own discretion.

My target intention is to personally run this on an isolated Raspberry pi with no remote access, and just enough network to talk to iCloud and also syslog so I can observe errors and manually fix.
