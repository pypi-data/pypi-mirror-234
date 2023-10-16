"Classes made for specific purposes"

import logging
import json
from httpx import HTTPError, Response
from .networking import NetworkClient
from .exceptions import NetworkError, NoResults, AlreadyExists, InvalidArgs, RateLimited
from .utils import convert_post_tags

logger = logging.getLogger(__name__)
default_session = NetworkClient()


class Fetcher:
    """Generic fetcher.

    Will work with any endpoints that support the "id" parameter
    """

    def __init__(self, networkclient=default_session):
        self.endpoint = ""
        self.session = networkclient
        self.type_name = "item"
        self.fetch_limit = 320

    def strip_dict_container(self, contained_item) -> list:
        """Some requests will have a single dictionary surrounding the list of objects, some wont, so this fixes that and removes the dictionary if it exists.

        Args:
            contained_item (list|dict): the object to remove the dictionary from.

        Returns:
            list: the cleaned object.
        """
        try:
            item = contained_item[list(contained_item)[0]]
        except TypeError:
            logger.debug("Dictionary does not surround objects")
            item = contained_item
        except IndexError:
            logger.debug(
                "No dictionary container and list empty (its most likely there were no results for the request made)"
            )
            item = contained_item
        return item

    def get(
        self, get_options: dict, fetch_count: int = 320, return_request: bool = False
    ) -> list | Response:
        """Retrieves up to 320 items from the fetcher specified endpoint.
        Note: 320 is the default as thats the fetch limit for most endpoints dealing with posts, but there are some endpoints that support fetching more or less then 320 at a time.

        Args:
            get_options (dict): the get options to include in the web request.
            fetch_count (int, optional): number of objects to fetch. Defaults to 320.
            return_request (bool, optional): whether or not to include the full httpx response object. Defaults to False.

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.
            NoResults: gets raised if no results were found.

        Returns:
            list | Response: list of fetched objects or the full response.
        """
        
        logger.debug(f"get args: '{get_options}' fetch count: '{fetch_count}'")

        if fetch_count > self.fetch_limit:
            fetch_count = self.fetch_limit
            logger.debug(f"Fetch count over limit, reduced to {self.fetch_limit}")

        options = {**get_options, 'limit': fetch_count}

        try:
            request = self.session.get(url=self.endpoint, params=options)
            logger.debug(f"request status {request.status_code}")
            request.raise_for_status()
        except HTTPError:
            logger.error("Network error occurred")
            raise NetworkError

        decoded_request = self.strip_dict_container(json.loads(request.text))
        if len(decoded_request) < 1:
            logger.warning("Nobody here but us chickens!")
            raise NoResults(f"Request options: {get_options}")

        if return_request:
            return request
        return decoded_request

    def looped_get(
        self, get_options: dict, fetch_count: int = 320, fetch_all: bool = False
    ) -> list:
        """Bulk fetches objects from fetcher specified endpoint.
        Note: only works with endpoints that have an "id" parameter.

        Args:
            get_options (dict): the get options to include in the web request.
            fetch_count (int, optional): number of objects to fetch. Defaults to 320.
            fetch_all (bool, optional): whether or not to fetch all results, overrides the "fetch_count" arg. Defaults to False.

        Returns:
            list: list of fetched objects
        """

        initial_fetch = self.get(get_options, fetch_count, False)
        objects_list = initial_fetch
        page = 0

        while True:
            last_object_id = initial_fetch[-1]['id']
            page += 1
            logger.debug(f"Fetching page: {page}")

            try:
                loop_objects_list = self.get(
                    {**get_options, 'page': f"b{last_object_id}"}, 320, False
                )
            except NoResults:
                if fetch_all:
                    logger.info(f"Fetched {len(loop_objects_list)} {self.type_name}s")
                else:
                    logger.info(
                        f"Failed to fetch all items. Count: {len(loop_objects_list)}"
                    )
                break

            for item in loop_objects_list:
                if len(objects_list) >= fetch_count and not fetch_all:
                    break
                objects_list.append(item)

            if len(objects_list) >= fetch_count and not fetch_all:
                break

        if fetch_all:
            logger.info(f"Fetched {len(objects_list)} {self.type_name}s")
        else:
            logger.info(
                f"Fetched {len(objects_list)} out of {fetch_count} {self.type_name}s"
            )
        return objects_list


class PostCache:
    "No worky, dont use"

    # ? very likely going to scrap this idea completely since i dont really feel like spending hours figuring out my own cache system, but i might come back to it at a later date
    def __init__(self, post_limit=1000):
        self.post_list = []
        self.post_limit = post_limit

    def add_post(self, post):
        if self.search_cache(id=post['id']) != None:
            logger.debug(f"Post {post['id']} already cached")
            return

        if len(self.post_list) >= self.post_limit:
            removed_post_id = self.post_list.pop(-1)['id']
            logger.debug(
                f"Removed post {removed_post_id} from cache. Reason: cache full"
            )

        self.post_list.append(post)

    def search_cache(self, id=None, tags=None):
        if id == None and tags == None:
            logger.error("No id or tags provided to search for, returning empty list")
            return []
        if id != None and tags == None:
            results = next((item for item in self.post_list if item['id'] == id), None)
        else:
            tag_list = str(tags).split()
            results = []
            for post in self.post_list:
                post = convert_post_tags(post)
                search = list(filter(lambda tag: tag in tag_list, post['all_tags']))
                if search == tag_list:
                    results.append(post)
        return results


class PostHandler(Fetcher):
    """Main class for handling post related tasks.

    Args:
        network_client (NetworkClient): client to use when making web requests.
    """

    def __init__(self, network_client=default_session):
        super().__init__(network_client)
        self.endpoint = "/posts.json"
        self.type_name = "post"

    def get_posts(
        self, tags: str, fetch_count: int = 320, fetch_all: bool = False
    ) -> list[dict]:
        """Fetches posts matching the provided tags.

        Args:
            tags (str): space separated list of tags to search for, supports normal e621 search syntax.
            fetch_count (int, optional): number of posts to fetch, can only fetch up to 320 at a time. Defaults to 320.
            fetch_all (bool, optional): whether or not to fetch all results, overrides the "fetch_count" arg. Defaults to False.

        Returns:
            list[dict]: list of posts that were fetched
        """

        logger.info(f"Fetching {fetch_count} posts with the tags: '{tags}'")
        if fetch_all or fetch_count <= 320:
            posts = self.get(get_options={'tags': tags}, fetch_count=fetch_count)
        else:
            posts = self.looped_get(get_options={'tags': tags}, fetch_count=fetch_count)
        logger.info("Fetch done")
        return posts

    def vote(self, post_id: int, vote: int) -> int:
        """Upvotes or downvotes a given post.

        If you upvote a post while it is currently upvoted, it will remove your vote, same goes for downvoting.

        Args:
            post_id (int): post id of post to vote on.
            vote (int): the vote you want to make (1 for upvote, -1 for downvote, 0 to remove your vote).

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            int: the value of your current vote.
        """

        endpoint = f"/posts/{post_id}/votes.json"
        if vote not in [1, -1, 0]:
            logger.warn("Invalid vote, must be '1', '-1' or '0'")
            return 0

        try:
            request = self.session.post(endpoint, params={'score': vote})
            request.raise_for_status()
        except HTTPError:
            logger.error(
                f"Failed to upvote post {post_id} due to network error. Request status code: {request.status_code}"
            )
            raise NetworkError

        new_score = json.loads(request.text)['our_score']
        logger.info(f"Voted {vote} on post {post_id}. New vote: {new_score}")
        return new_score

    def favorite(self, post_id: int, favorite: bool) -> bool:
        """Favorites a given post.

        Args:
            post_id (int): post id of post to favorite.
            favorite (bool): favorites the post if true.

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            bool: whether or not the current post is a favorite.
        """

        if favorite:
            try:
                request = self.session.post(
                    "/favorites.json", params={'post_id': post_id}
                )
                request.raise_for_status()
            except HTTPError:
                if request.status_code == 422:
                    logger.warning(f"Post {post_id} already favorited")
                    return True
                raise NetworkError

            logger.info(f"Post {post_id} favorited")
            return True

        try:
            request = self.session.delete(f"/favorites/{post_id}.json")
            request.raise_for_status()
        except HTTPError:
            logger.error(
                f"A network error occurred. Request status code: {request.status_code}"
            )
            raise NetworkError

        post = self.get({'tags': f'id:{post_id}'})[0]
        return post['is_favorited']

    def edit(
        self,
        post_id,
        tag_diff: type[str] = None,
        source_diff: type[str] = None,
        parent_id: type[int] = None,
        description: type[str] = None,
        rating: type[str] = None,
        edit_reason: type[str] = None,
    ) -> list[dict]:
        """Updates a given post with the parameters specified.

        Only include parameters that you are actually changing, leave everything else on None.

        The format for tag/source diff is having a plus sign directly before the tag you want to add, and having a minus sign instead for removing tags (ex. "+male -female").

        Args:
            post_id (_type_): post id of post to edit.
            tag_diff (type[str], optional): space separated diff of tags to add/remove. Defaults to None.
            source_diff (type[str], optional): space separated diff of sources to add/remove. Defaults to None.
            parent_id (type[int], optional): the id of the parent post, if there is one. Defaults to None.
            description (type[str], optional): the new description for the post you are editing. Defaults to None.
            rating (type[str], optional): the new rating for the post you are editing. Defaults to None.
            edit_reason (type[str], optional): the reason for editing the post. Defaults to None.

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            list[dict]: returns the newly updated post inside a list.
        """

        post_data = {}
        if tag_diff != None:
            post_data = {**post_data, 'post[tag_string_diff]': tag_diff}
        if source_diff != None:
            post_data = {**post_data, 'post[source_diff]': source_diff}
        if parent_id != None:
            post_data = {**post_data, 'post[parent_id]': parent_id}
        if description != None:
            post_data = {**post_data, 'post[description]': description}
        if rating != None:
            post_data = {**post_data, 'post[rating]': rating}
        if edit_reason != None:
            post_data = {**post_data, 'post[edit_reason]': edit_reason}

        try:
            request = self.session.patch(f"/posts/{post_id}.json", params=post_data)
            request.raise_for_status()
        except HTTPError:
            logger.error(
                f"A network error occurred. Request status code: {request.status_code}"
            )
            raise NetworkError
        logger.info(f"Edited post {post_id} successfully")
        return [self.strip_dict_container(json.loads(request.text))]

    def upload(
        self,
        tags: str,
        rating: str,
        source: str,
        description: str = None,
        upload_file=None,
        direct_url: str = None,
        parent_id: int = None,
    ) -> list[dict]:
        """Uploads a new post based on the provided parameters.

        Either "upload_file" or "direct_url" must be specified or it will fail.

        Args:
            tags (str): space separated list of tags to include in the new post.
            rating (str): the rating of the post.
            source (str): space separated list of urls that the original image/video came from (can be an empty string if there are no sources).
            description (str, optional): the description of the new post. Defaults to None.
            upload_file (any filetype object, optional): the image/video to upload. Defaults to None.
            direct_url (str, optional): the url leading to the image/video you wish to upload. Defaults to None.
            parent_id (int, optional): the id of the parent post, if there is one. Defaults to None.

        Raises:
            AlreadyExists: gets raised if the post already exists.
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            list[dict]: the newly uploaded post in a list.
        """

        post_data = {
            'upload[tag_string]': tags,
            'upload[rating]': rating,
            'upload[source]': source,
        }
        if description != None:
            post_data = {**post_data, 'upload[description]': description}
        if parent_id != None:
            post_data = {**post_data, 'upload[parent_id]': parent_id}

        if upload_file != None:
            post_file = {'upload[file]': upload_file}
        elif direct_url != None:
            post_data = {**post_data, 'upload[direct_url]': direct_url}
        else:
            logger.error("Upload failed, no file or direct url given")
            return []

        try:
            if upload_file != None:
                request = self.session.post(
                    "/uploads.json", data=post_data, files=post_file
                )
            else:
                request = self.session.post("/uploads.json", data=post_data)
            request.raise_for_status()
        except HTTPError:
            if request.status_code == 412:
                error_status = json.loads(request.text)
                logger.error(
                    f"Upload failed, post already exists. Id: {error_status['post_id']}"
                )
                raise AlreadyExists(int(error_status['post_id']))

            logger.error(
                f"Upload failed, a network error occurred. Request status code: {request.status_code}"
            )
            raise NetworkError

        status = json.loads(request.text)
        logger.info(f"Post uploaded successfully! Id: {status['post_id']}")
        try:
            return self.get({'tags': f"id:{status['post_id']}"})
        except NoResults:
            logger.warning("Failed to get post after upload")
            return []


class PoolHandler(Fetcher):
    """Main class for pool related functions.

    Args:
        network_client (NetworkClient): client to use when making web requests.
    """

    def __init__(self, network_client=default_session):
        super().__init__(network_client)
        self.endpoint = "/pools.json"
        self.type_name = "pool"
        self.categories = ["series", "collection"]
        self.order = [
            "name",
            "created_at",
            "updated_at",
            "post_count",
        ]

    def filter_args(self, args: dict) -> dict:
        """Filters out the provided dictionary and returns all values that are not None.

        Args:
            args (dict): the dictionary to filter through.

        Returns:
            dict: the filtered dictionary.
        """
        # ? might move this to the utils module

        args_to_be_removed = []
        for arg, arg_value in args.items():
            if arg_value == None:
                args_to_be_removed.append(arg)

        for arg in args_to_be_removed:
            args.pop(arg)
        return args

    def validate_args(self, args: dict):
        # for use mainly with the create and edit functions of this class
        try:
            if len(args["pool[post_ids][]"]) > 1000:
                logger.warning("Too many posts, limit is 1000")
                raise InvalidArgs
        except KeyError:
            pass

        try:
            if args["pool[category]"] not in self.categories:
                logger.warning(
                    f"Category invalid, must be one of the following {str(self.categories)}"
                )
                raise InvalidArgs
        except KeyError:
            pass

        try:
            if len(args["pool[name]"]) > 250:
                logger.warning("Name is too long, character limit is 250")
                raise InvalidArgs
        except KeyError:
            pass

        try:
            if len(args["pool[description]"]) > 10000:
                logger.warning("Description is too long, character limit is 10000")
        except KeyError:
            pass

        try:
            int(args["pool[name]"])
        except ValueError:
            pass
        except KeyError:
            pass
        else:
            logger.warning("Name cannot contain only numbers")
            raise InvalidArgs

    def get_pools(
        self,
        name_search: str = None,
        description_search: str = None,
        creator_name_search: str = None,
        search_category: str = "series",
        search_order: str = "updated_at",
        fetch_count: int = 320,
        pool_id: int = None,
        creator_id: int = None,
        is_active: bool = None,
        fetch_all: bool = False,
    ) -> list[dict]:
        """Fetches a list of pools that match the given search parameters.

        Must have at least one search query.

        Args:
            name_search (str, optional): searches through names of pools. Defaults to None.
            description_search (str, optional): searches through the descriptions of pools. Defaults to None.
            creator_name_search (str, optional): searches for pools with creators that match this search. Defaults to None.
            search_category (str, optional): the type of pool to search for (can be either "series" or "collection"). Defaults to "series".
            search_order (str, optional): what order the returned list should be in. Defaults to "updated_at".
            fetch_count (int, optional): number of pools to fetch. Defaults to 320.
            pool_id (int, optional): the pool id to search for. Defaults to None.
            creator_id (int, optional): searches for all pools made by the given creator id. Defaults to None.
            is_active (bool, optional): whether or not the pools to search for should be active or not (if not provided, will search for both). Defaults to None.
            fetch_all (bool, optional): whether or not to fetch all results, overrides the "fetch_count". Defaults to False.

        Raises:
            InvalidArgs: raised if the search query parameters are not valid.

        Returns:
            list[dict]: list of pools that were fetched.
        """

        request_args = {
            "search[name_matches]": name_search,
            "search[description_matches]": description_search,
            "search[creator_name]": creator_name_search,
            "search[category]": search_category,
            "search[order]": search_order,
            "search[id]": pool_id,
            "search[creator_id]": creator_id,
            "search[is_active]": is_active,
        }
        request_args = self.filter_args(request_args)

        if search_category not in self.categories and search_category != "":
            logger.warning(
                f"Search category invalid, must be one of the following {str(self.categories)}"
            )
            raise InvalidArgs
        if search_order not in self.order and search_order != "":
            logger.warning(
                f"Search order invalid, must be one of the following {str(self.order)}"
            )
            raise InvalidArgs

        if fetch_all or fetch_count <= 320:
            pools = self.get(get_options=request_args, fetch_count=fetch_count)
        else:
            pools = self.looped_get(
                get_options=request_args, fetch_count=fetch_count, fetch_all=fetch_all
            )
        logger.info(f"{len(pools)} pools found")
        return pools

    def create(
        self, name: str, description: str, category: str, post_ids: list[int] = []
    ) -> list[dict]:
        """Creates a new pool.

        Args:
            name (str): the name of the new pool.
            description (str): the description of the new pool.
            category (str): what type of pool it will be (can be "series" or "collection")
            post_ids (list[int], optional): a list of post ids to be included in the pool. Defaults to [].

        Raises:
            AlreadyExists: gets raised if a pool of the same name already exists.
            RateLimited: if you reach the hourly limit of how many pools you can make, this will get raised until the limit resets
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            list[dict]: the newly made post in a list
        """

        request_args = {
            "pool[name]": name,
            "pool[description]": description,
            "pool[category]": category,
        }
        if post_ids != []:
            request_args = {**request_args, "pool[post_ids][]": post_ids}

        self.validate_args(request_args)

        try:
            request = self.session.post(self.endpoint, params=request_args)
            request.raise_for_status()
        except HTTPError:
            if request.status_code == 422:
                status_message = json.loads(request.text)["errors"]
                try:
                    if status_message["name"][0] == "has already been taken":
                        logger.error("Pool name already taken")
                        raise AlreadyExists
                except KeyError:
                    if (
                        status_message["creator"][0]
                        == "reached the hourly limit for this action"
                    ):
                        logger.error("Rate limited, try again in an hour")
                        raise RateLimited
            else:
                logger.error(
                    f"Failed to create pool, a network error occurred. Request status code: {request.status_code}"
                )
                raise NetworkError
        pool = self.strip_dict_container([json.loads(request.text)])
        logger.info(f"Pool made successfully! id: {pool['id']}")
        return [pool]

    def edit(
        self,
        id: int,
        name: str = None,
        description: str = None,
        post_ids: list[int] = None,
        is_active: bool = None,
        category: str = None,
    ) -> list[dict]:
        """Updates a pool using the provided parameters.

        Args:
            id (int): the id of the pool you want to edit.
            name (str, optional): the new name for the pool. Defaults to None.
            description (str, optional): the new description for the pool. Defaults to None.
            post_ids (list[int], optional): a list of post ids to be included in the pool. Defaults to None.
            is_active (bool, optional): whether or not the pool is currently active. Defaults to None.
            category (str, optional): the new category for the pool. Defaults to None.

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            list[dict]: the newly edited pool in a list.
        """

        request_args = {
            "pool[name]": name,
            "pool[description]": description,
            "pool[post_ids][]": post_ids,
            "pool[is_active]": is_active,
            "pool[category]": category,
        }

        request_args = self.filter_args(request_args)
        self.validate_args(request_args)

        try:
            request = self.session.put(f"/pools/{id}.json", params=request_args)
            request.raise_for_status()
        except HTTPError:
            logger.error("Unknown error occurred.")
            raise NetworkError(f"Raw response data: {request.text}")

        logger.info(f"Edited pool {id} successfully")
        return self.get({"search[id]": id})

    def revert(self, id: int, version_id: int) -> list[dict]:
        """Revert a given pool to a previous state

        Args:
            id (int): the id of the pool to revert
            version_id (int): the version id to revert back to

        Raises:
            NetworkError: gets raised upon encountering a network error that cannot be resolved.

        Returns:
            list[dict]: the reverted post in a list
        """
        try:
            request = self.session.put(
                f"/pools/{id}/revert.json", params={"version_id": version_id}
            )
            request.raise_for_status()
        except HTTPError:
            logger.error("Unknown error occurred.")
            raise NetworkError(f"Raw response data: {request.text}")

        logger.info(f"Reverted pool {id} to version {version_id}")
        return self.get({"search[id]": id})
