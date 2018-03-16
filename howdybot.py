import praw
import pprint

# fill in with your info
sample_user = 'some username';
sample_password = 'some password';
sample_user_agent = 'some agent';
sample_client_id = 'some client id';
sample_client_secret = 'some client secret';

reddit = praw.Reddit(client_id=sample_client_id,
                     client_secret=sample_client_secret,
                     user_agent=sample_user_agent,
                     username=sample_user,
                     password=sample_password)

# subreddit to check
sub = reddit.subreddit('testingground4bots')

# phrases that bot looks for in each comment
phrases = ['howdy']

for submission in sub.new(limit=10): 
    print('Title: ',submission.title,'\n')
    submission.comments.replace_more(limit=0)
    top_level_comments = list(submission.comments)
    comment_queue = submission.comments[:]
    while comment_queue:
        comment = comment_queue.pop(0)
        if not hasattr(comment, 'body'):
            continue
        for phrase in phrases:
            if phrase in comment.body.lower() and comment.author != sample_user:
                alreadyReplied = False
                for comment_replies in comment.replies:
                    if comment_replies.author == sample_user:
                        alreadyReplied = True
                        break
                if not alreadyReplied:
                    print('Replied to: ', comment.body)
                    comment.reply('Howdy!')
        comment_queue.extend(comment.replies)
    print('----------------------------------------')