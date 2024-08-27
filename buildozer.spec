[app]

# (str) Title of your application
title = Chonky Dog

# (str) Source code where the main.py file is located
source.dir = .

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Add all your project's dependencies here
requirements = python3, kivy

# (str) Package name
package.name = chonkydog

# (str) Package domain (for example: org.example.myandroidgame)
package.domain = org.chonkydog

# (str) Source code where the main.py file is located
source.include_exts = py,png,jpg,kv,atlas,ogg,wav,mp3

# (list) Include specific directories (comma separated) (from the source. dir)
source.include_dirs = assets/,images/,sounds/,widgets/

# Orientation
orientation = portrait

# Fullscreen mode
fullscreen = 1

# Permissions
android.permissions = RECORD_AUDIO, MODIFY_AUDIO_SETTINGS

# Uncomment if needed for audio focus
# android.meta_data = com.google.android.gms.ads.APPLICATION_ID = YOUR_ADMOB_APP_ID
