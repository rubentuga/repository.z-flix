'''#####-----Build File-----#####'''
buildfile = 'https://www.dropbox.com/scl/fi/axlao9mgigffxj3464333/builds.xml?rlkey=43g7376kbgllthxxi26t8o0ui&e=1&st=r2h85tuq&dl=0'

'''#####-----Notifications File-----#####'''
notify_url  = 'http://dr-venture.com/709/Wizard/notify.txt'

'''#####-----Changelog Directory-----#####'''
changelog_dir  = 'http://dr-venture.com/709/Wizard/changelogs/'

'''#####-----Videos File-----#####'''
videos_url = 'http://CHANGEME'

'''#####-----Excludes-----#####'''
excludes  = ['plugin.video.whatever']

#Change Build Name(s) Guide
'''
1. Add your Old/New build names to the BUILDS variable below.
2. Update your builds file to remove the Old Build and add the New Build.
   IMPORTANT: Apply the Old Build version to the New Build entry.
3. Bump the version of your New Build.
4. At first run the user will be prompted to install the update (Your New Build).'''

#Change Build Name(s)
BUILDS = [{'Old Build': "Old Build_1", 'New Build': "New Build_1"},
          {'Old Build': "Old Build_2", 'New Build': "New Build_2"}]
