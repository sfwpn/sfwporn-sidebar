# Fetches sidebar from one subreddit and applies it to other subreddits
# Subreddits to have sidebar applied to MUST HAVE the delimiters in the sidebar file.
# With the default delimiters the sidebar should include a chunk of text like:
# 
# START_DELIM = '>* [VideoPorn](/r/VideoPorn)'
# END_DELIM = '* [Moderator Log](http://reddit.com/r/moderationporn/new)'
#
# --Subredit-specific sidebar goes here--


import re
import reddit
import HTMLParser
from ConfigParser import SafeConfigParser
import sys, os

# set up the config parser
cfg_file = SafeConfigParser()
path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
path_to_cfg = os.path.join(path_to_cfg, 'network-sidebar.cfg')
cfg_file.read(path_to_cfg)


# defines the source and network subreddits
SOURCE_SUBREDDIT = 'sfwpornnetworkcss'
NETWORK_SUBREDDITS = ['lolsfwhappyfuntime']

# login info for the script to log in as, this user must be a mod in the main subreddit
REDDIT_USERNAME = cfg_file.get('reddit', 'username')
REDDIT_PASSWORD = cfg_file.get('reddit', 'password')
REDDIT_UA = cfg_file.get('reddit', 'user_agent')

# don't change unless you want different delimiter strings for some reason
START_DELIM = '>* [VideoPorn](/r/VideoPorn)'
END_DELIM = '* [Moderator Log](http://reddit.com/r/moderationporn/new)'


# log into reddit
print "Logging in as /u/"+REDDIT_USERNAME+"..."
r = reddit.Reddit(user_agent=REDDIT_UA)
r.login(REDDIT_USERNAME, REDDIT_PASSWORD)
print "  Success!"


# get the source stylesheet
print "Getting source sidebar from /r/"+SOURCE_SUBREDDIT+"..."
source_subreddit = r.get_subreddit(SOURCE_SUBREDDIT)
# fetch the stylesheet from the main subreddit
source_sidebar = source_subreddit.get_settings()['description']
print source_sidebar
# construct the regex object
replace_pattern = re.compile('%s.*?%s' % (re.escape(START_DELIM), re.escape(END_DELIM)), re.IGNORECASE|re.DOTALL|re.UNICODE)
# extract sidebar from source stylesheet
source_sidebar = HTMLParser.HTMLParser().unescape(source_sidebar)
source_sidebar = re.search(replace_pattern, source_sidebar).group(0)
print "  Success!"


# Apply sidebar to network subreddits
print "Updating network subreddits' sidebars:"
for dest_sr in NETWORK_SUBREDDITS:
    print "  /r/"+dest_sr+"..."
    
    dest_subreddit = r.get_subreddit(dest_sr)
    dest_sidebar = dest_subreddit.get_settings()['description']
    dest_sidebar = HTMLParser.HTMLParser().unescape(dest_sidebar)


    new_sidebar = re.sub(replace_pattern, source_sidebar, dest_sidebar)
    print new_sidebar
    
    dest_subreddit.update_settings(description=new_sidebar)
    
    print "    Done!"


# update the sidebar
# current_sidebar = main_subreddit.get_settings()['description']
# current_sidebar = HTMLParser.HTMLParser().unescape(current_sidebar)
# replace_pattern = re.compile('%s.*?%s' % (re.escape(START_DELIM), re.escape(END_DELIM)), re.IGNORECASE|re.DOTALL|re.UNICODE)
# new_sidebar = re.sub(replace_pattern,
#                     '%s\\n\\n%s\\n%s' % (START_DELIM, list_text, END_DELIM),
#                     current_sidebar)
# main_subreddit.update_settings(description=new_sidebar)