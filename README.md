# iCloud Photos backup

> a tool to backup your photos from iCloud

Like many others I keep all my family photos in Photos and take comfort that Apple handle the storage + backup.

However something got me worried, *what if* I got infected with some ransomware that encrypted or destroyed my photos, from an attack point of view, that'd probably be a pretty lucrative attack.

## Usage

```bash
docker run \
  --rm -ti \
  -v ${PWD}/backup:/app/backup \
  -v `pwd`/session:/tmp/pyicloud \
  -e USERNAME="xxx@mac.com" \
  chrisns/icloud-photos-backup
```
You can if you're comfortable with it specify your password as an environment too as `PASSWORD` otherwise it'll prompt you to enter it on execution along with a 2FA prompt if you've enabled it - **you have enabled 2FA right?!!**

## But I don't trust you [@chrisns](@chrisns) with my credentials

No, why on earth would you, you'd be mad to blindly run the above docker command, so I'd really urge you to pull this repo, check all the dependencies and use very much at your own discretion.

My target intention is to personally run this on an isolated Raspberry pi with no remote access, and just enough network to talk to iCloud and also syslog so I can observe errors and manually fix.