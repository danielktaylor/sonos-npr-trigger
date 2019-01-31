# sonos-npr-trigger

Docker container that runs a simple flask app to grab the latest NPR news show and send it to the first Sonos group it finds. Useful for triggering via IFTTT.

# Paths

* `/volumedown` - turn volume down 10%
* `/volumeup` - turn volume up 10%
* `/skip` - skip the track
* `/resume` - keep playing
* `/pause` - pause track
* `/listen` - grab tracks from NPR and send to Sonos system
