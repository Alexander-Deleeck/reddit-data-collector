import json

FILE = "" # Provide path to comments json file

# Load the JSON data from the file
with open(FILE, 'r') as file:
    comments_data = json.load(file)

def find_highest_score_comment(comment_tree, highest_score_comment={'score': -1}):
    for comment in comment_tree:
        # Update the highest score comment if the current one has a higher score
        if comment['score'] > highest_score_comment['score']:
            highest_score_comment = comment
        # Recursively search in replies
        if comment['replies']:
            highest_score_comment = find_highest_score_comment(comment['replies'], highest_score_comment)
    return highest_score_comment

highest_score_comment = find_highest_score_comment(comments_data)

def display_comment(comment, level=0):
    # Print the current comment with indentation based on its level in the hierarchy
    indent = '  ' * level
    print(f"{indent}Author: {comment['author']}, Score: {comment['score']}")
    print(f"{indent}Text: {comment['text']}\n")
    
    # Recursively display replies with increased indentation
    for reply in comment['replies']:
        display_comment(reply, level + 1)

# Display the highest score comment and its child comments
display_comment(highest_score_comment)

