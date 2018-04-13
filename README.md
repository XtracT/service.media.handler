# script.media.organizer
A simple Media Organizer add-on for kodi, targeted for Kodi users in android.

Organize your media files (movies, TV shows, anime and music) from a source folder, where everything is mixed, to the proper destination folder, in such a way that Kodi libraries can find your media and use the proper data scrappers.

Just select the different folders and this two options in add-on settings:
- Update libraries when moving files has finished
- Remove files. Those files which are not media (video or audio) can be automatically removed or moved to the unorganizable files folder

# Right now:
- Uses IMDb movies and TV shows database
- Movies and TV shows which are not found are moved to unorganizable files
- Trailer and Sample files are moved to unorganizable files or deleted
- Non media files (nfo, txt, pictures, etc) are moved or deleted too
- Music files need to be tagged in order for kodi to find proper data

# Usage:
- Install add-on via zip file in Kodi, open settings and do as desired
- Run it manually when it is necessary to move the files or use Callbacks add-on to do it with watchdog or in schedule
