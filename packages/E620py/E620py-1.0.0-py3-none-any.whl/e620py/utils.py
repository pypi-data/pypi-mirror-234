"Helpful and reuseable functions"


def convert_post_tags(post):
    post_tag_lists = [tag for tag in post['tags'].values()]
    post_tags = []
    for tag_list in post_tag_lists:
        post_tags.extend(tag_list)
    post = {**post, 'all_tags': post_tags}
    return post
