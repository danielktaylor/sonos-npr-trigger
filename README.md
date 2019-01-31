# sonos-npr-trigger

Docker container that runs a simple flask app to grab the latest NPR news show and send it to the first Sonos group it finds. Useful for triggering via IFTTT.

# Paths

HTTP server runs on port 5000

* `/volumedown` - turn volume down 10%
* `/volumeup` - turn volume up 10%
* `/skip` - skip the track
* `/resume` - keep playing
* `/pause` - pause track
* `/listen` - grab tracks from NPR and send to Sonos system

# Creating container

> docker create --name=sonos-npr --restart=unless-stopped --net=host yoblin/sonos-npr-trigger && docker start sonos-npr
