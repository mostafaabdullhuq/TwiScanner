from json import loads, dumps
import sys
import requests
from bs4 import BeautifulSoup
from re import findall
from datetime import datetime
import time

try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus
from random import choice

x = sys.argv[1]


"""
Error Codes:

getHomeReq => 1000
getSearchReq => 1001
getMainJsReq => 1002
clientEventPostReq1 => 1003
clientEventPostReq2 => 1004
searchAdaptiveGetReq => 1005
getProfilePage => 1006
graphqlOptionsReq => 1007
graphqlGetReq => 1008
getTweetsReq => 1009
searchAdaptiveGetReq => 1010
searchAdaptiveGetReq => 1011
searchTweetIdsList => 1012
searchAdaptiveGetReq => 1013
getTweetsReq => 1014
getProfile => 1015
getInfo => 1016


Exception => 1100
Rate Limit => 1101

States:

Banned => 1
Good => 2
Not Found => 3
Suspended => 4
Protected => 5
No Tweets => 6

"""


def guest_activate(proxy):
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    }
    session = requests.session()
    session.verify = False
    try:
        if proxy:
            session.proxies = {"https": proxy}
            session.proxies.update({"https": proxy})
        response = session.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers)
        guestID = response.json()["guest_token"]
        return guestID
    except:
        return False


def checkSearch(userName, proxy):
    try:
        with requests.Session() as session:
            if proxy:
                proxyDict = {"https": "{}".format(proxy), "http": "{}".format(proxy)}
                session.proxies.update(proxyDict)
            date_time = str(datetime.now()).split(".")[0]
            pattern = "%Y-%m-%d %H:%M:%S"
            timeStamp = int(time.mktime(time.strptime(date_time, pattern)))

            getHomeReqHeaders = {
                "Host": "twitter.com",
                "Connection": "keep-alive",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
            }

            getHomeReq = session.get("https://twitter.com/", headers=getHomeReqHeaders)
            if getHomeReq.status_code == 200 and "decodeURIComponent" in getHomeReq.text:
                guestToken = findall('decodeURIComponent\("gt\=(\d*);', getHomeReq.text)[0]

                getSearchReqHeaders = {
                    "Host": "twitter.com",
                    "Connection": "keep-alive",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "DNT": "1",
                    "upgrade-insecure-requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "same-origin",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://twitter.com/sw.js",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                }

                getSearchReq = session.get("https://twitter.com/search?q={}&src=typed_query&f=user&prefetchTimestamp={}".format(userName, timeStamp), headers=getSearchReqHeaders)
                if getSearchReq.status_code == 200:
                    getMainJsReqHeaders = {
                        "Host": "abs.twimg.com",
                        "Connection": "keep-alive",
                        "Origin": "https://twitter.com",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                        "DNT": "1",
                        "Accept": "*/*",
                        "Sec-Fetch-Site": "cross-site",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "script",
                        "Referer": "https://twitter.com/",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                    }

                    getMainJsReq = session.get("https://abs.twimg.com/responsive-web/client-web/main.5c903175.js", headers=getMainJsReqHeaders)
                    if getMainJsReq.status_code == 200 and 'authorization:"Bearer' in getMainJsReq.text:
                        autherizationToken = findall(',a="(AA(\w*\%?)*)",c=', getMainJsReq.text)[0][0]
                        appID = findall('",o="(\d*)",s', getMainJsReq.text)[0]
                        clientEventReq1Headers = {
                            "Host": "api.twitter.com",
                            "Connection": "keep-alive",
                            "Content-Length": "703",
                            "DNT": "1",
                            "x-twitter-client-language": "en",
                            "authorization": "Bearer {}".format(autherizationToken),
                            "content-type": "application/x-www-form-urlencoded",
                            "Accept": "*/*",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                            "x-guest-token": "{}".format(guestToken),
                            "x-twitter-active-user": "yes",
                            "Origin": "https://twitter.com",
                            "Sec-Fetch-Site": "same-site",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Dest": "empty",
                            "Referer": "https://twitter.com/search?q=m_abdullhuq&src=typed_query&f=user",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Accept-Language": "en-US,en;q=0.9",
                        }
                        clientEventReq1Data = {
                            "category": "perftown",
                            "log": loads(
                                dumps(
                                    """[{"description":"rweb:init:storePrepare","product":"rweb","duration_ms":167},{"description":"rweb:ttft:perfSupported","product":"rweb","duration_ms":1},{"description":"rweb:ttft:connect","product":"rweb","duration_ms":14},{"description":"rweb:ttft:process","product":"rweb","duration_ms":59},{"description":"rweb:ttft:response","product":"rweb","duration_ms":1},{"description":"rweb:ttft:interactivity","product":"rweb","duration_ms":512}]"""
                                )
                            ),
                        }
                        clientEventPostReq1 = session.post("https://api.twitter.com/1.1/jot/client_event.json", headers=clientEventReq1Headers, data=clientEventReq1Data)
                        if clientEventPostReq1.status_code == 200 and clientEventPostReq1.text == "":
                            clientEventPostReq2Headers = {
                                "Host": "api.twitter.com",
                                "Connection": "keep-alive",
                                "Content-Length": "424",
                                "DNT": "1",
                                "x-twitter-client-language": "en",
                                "authorization": "Bearer {}".format(autherizationToken),
                                "content-type": "application/x-www-form-urlencoded",
                                "Accept": "*/*",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                                "x-guest-token": "{}".format(guestToken),
                                "x-twitter-active-user": "yes",
                                "Origin": "https://twitter.com",
                                "Sec-Fetch-Site": "same-site",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Dest": "empty",
                                "Referer": "https://twitter.com/search?q={}&src=typed_query&f=user".format(userName),
                                "Accept-Encoding": "gzip, deflate, br",
                                "Accept-Language": "en-US,en;q=0.9",
                            }

                            clientEventPostReq2Data = {
                                "debug": "true",
                                "log": loads(
                                    dumps(
                                        """[{{"_category_":"client_event","format_version":2,"triggered_on":{},"event_namespace":{{"page":"search","section":"search_filter_user","action":"show","client":"m5"}},"client_event_sequence_start_timestamp":{},"client_event_sequence_number":0,"client_app_id":"{}"}}]""".format(
                                            timeStamp, timeStamp, appID
                                        )
                                    )
                                ),
                            }
                            clientEventPostReq2 = session.post("https://api.twitter.com/1.1/jot/client_event.json", headers=clientEventPostReq2Headers, data=clientEventPostReq2Data)
                            if clientEventPostReq2.status_code == 200 and clientEventPostReq2.text == "":
                                searchAdaptiveGetReqHeaders = {
                                    "Host": "api.twitter.com",
                                    "Connection": "keep-alive",
                                    "authorization": "Bearer {}".format(autherizationToken),
                                    "DNT": "1",
                                    "x-twitter-client-language": "en",
                                    "x-guest-token": "{}".format(guestToken),
                                    "x-twitter-active-user": "yes",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                                    "Accept": "*/*",
                                    "Origin": "https://twitter.com",
                                    "Sec-Fetch-Site": "same-site",
                                    "Sec-Fetch-Mode": "cors",
                                    "Sec-Fetch-Dest": "empty",
                                    "Referer": "https://twitter.com/search?q={}&src=typed_query&f=user".format(userName),
                                    "Accept-Language": "en-US,en;q=0.9",
                                }
                                searchAdaptiveGetReq = session.get(
                                    "https://api.twitter.com/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&result_filter=user&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel".format(
                                        userName
                                    ),
                                    headers=searchAdaptiveGetReqHeaders,
                                )
                                if "users" in searchAdaptiveGetReq.text and searchAdaptiveGetReq.status_code == 200:
                                    usersResult = searchAdaptiveGetReq.json()["globalObjects"]["users"]
                                    if usersResult == {}:
                                        return {"status": "success", "error": None, "user_state": 3, "data": None}
                                    else:
                                        usersList = []
                                        for eachUser in usersResult:
                                            usersList.append(str(usersResult[eachUser]["screen_name"]).lower())
                                        # if user is valid search result
                                        if userName.lower() in usersList:
                                            return {"status": "success", "error": None, "user_state": 2, "data": None}
                                        else:
                                            return {"status": "success", "error": None, "user_state": 1, "data": None}
                                else:
                                    return {"status": "failed", "error": 1005, "user_state": None, "data": None}
                            else:
                                return {"status": "failed", "error": 1004, "user_state": None, "data": None}
                        else:
                            return {"status": "failed", "error": 1003, "user_state": None, "data": None}
                    else:
                        return {"status": "failed", "error": 1002, "user_state": None, "data": None}
                else:
                    return {"status": "failed", "error": 1001, "user_state": None, "data": None}
            else:
                return {"status": "failed", "error": 1000, "user_state": None, "data": None}
    except:
        return {"status": "failed", "error": 1100, "user_state": None, "data": None}


def checkShadow(userName, proxy):
    try:
        guestID = guest_activate(proxy)
        with requests.Session() as session:
            session.verify = False
            userTweetIdsList = []
            searchTweetIdsList = []
            if proxy:
                proxyDict = {"https": "{}".format(proxy), "http": "{}".format(proxy)}
                session.proxies.update(proxyDict)
            getProfilePageHeaders = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,nl;q=0.6",
            }
            getProfilePage = session.get("https://twitter.com/{}".format(userName), headers=getProfilePageHeaders)
            if getProfilePage.status_code == 200:
                graphqlOptionsReqHeaders = {
                    "Host": "api.twitter.com",
                    "Accept": "*/*",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "authorization,content-type,x-csrf-token,x-guest-token,x-twitter-active-user,x-twitter-client-language",
                    "Origin": "https://twitter.com",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://twitter.com/{}".format(userName),
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,nl;q=0.6",
                }
                param = {"variables": str(loads((dumps('{{"screen_name":"{}","withHighlightedLabel":true}}'.format(userName)))))}
                graphqlOptionsReq = session.options(
                    "https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName?".format(userName.lower()), headers=graphqlOptionsReqHeaders, params=param
                )
                if graphqlOptionsReq.status_code == 200:
                    graphqlGetReqHeaders = {
                        "Host": "api.twitter.com",
                        "x-twitter-client-language": "en",
                        "x-csrf-token": "a9b7d0e0fe277ca386decfd4373cdd71",
                        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                        "content-type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                        "x-guest-token": "{}".format(guestID),
                        "x-twitter-active-user": "yes",
                        "Accept": "*/*",
                        "Origin": "https://twitter.com",
                        "Sec-Fetch-Site": "same-site",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": "https://twitter.com/{}".format(userName),
                        "Accept-Language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,nl;q=0.6",
                    }
                    param = {"variables": str(loads((dumps('{{"screen_name":"{}","withHighlightedLabel":true}}'.format(userName)))))}
                    graphqlGetReq = session.get(
                        "https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName?".format(userName.lower()), headers=graphqlGetReqHeaders, params=param
                    )

                    if graphqlGetReq.status_code == 200 and "user" in str(graphqlGetReq.text) and "created_at" in str(graphqlGetReq.text):
                        # print(graphqlGetReq.text)
                        userDetails = graphqlGetReq.json()["data"]["user"]["legacy"]
                        userID = graphqlGetReq.json()["data"]["user"]["rest_id"]
                        getTweetsReqHeaders = {
                            "Host": "twitter.com",
                            "Connection": "keep-alive",
                            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                            "DNT": "1",
                            "x-twitter-client-language": "en",
                            "x-csrf-token": "a9b7d0e0fe277ca386decfd4373cdd71",
                            "x-guest-token": "{}".format(guestID),
                            "x-twitter-active-user": "yes",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                            "Accept": "*/*",
                            "Sec-Fetch-Site": "same-origin",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Dest": "empty",
                            "Referer": "https://twitter.com/",
                            "Accept-Language": "en-US,en;q=0.9",
                            "Cookie1": 'personalization_id="v1_cvet2wHhji0RQ6jewODqQw=="; guest_id=v1%3A161365290208151861; ct0=41ddc0c5eb88510407b5d30d4f72ca6c; _sl=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCP1FNbV3AToMY3NyZl9p%250AZCIlMjA3Y2VjMjliNjhhNGEwOTVmZmRhYWFmODMxOGE5OWI6B2lkIiU1MzEz%250ANDAzNDUxOTliY2E1OTI1MWY4NmY4MWQ3OTQ0MA%253D%253D--180911d4e5b56a30b643927e79cfe9fc4b20fad6; gt='
                            + guestID,
                        }
                        getTweetsReq = session.get(
                            f"https://twitter.com/i/api/graphql/DhQ8lYnLh5T5K8aVUgHVnQ/UserTweets?variables=%7B%22userId%22%3A%22{userID}%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%2C%22__fs_interactive_text%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Afalse%7D",
                            headers=getTweetsReqHeaders,
                        )
                        if "data" in str(getTweetsReq.text) and getTweetsReq.status_code == 200 and "user" in str(getTweetsReq.text) and "UserUnavailable" not in str(getTweetsReq.text):
                            responseTweetsIds = []
                            for _ in getTweetsReq.json()["data"]["user"]["result"]["timeline"]["timeline"]["instructions"][1]["entries"]:

                                if _["content"]["entryType"] == "TimelineTimelineItem":
                                    responseTweetsIds.append(_["sortIndex"])
                            userTweetIdsList += responseTweetsIds
                            if len(responseTweetsIds) != 0:
                                if '111111111111cursorType":"Bottom' in str(getTweetsReq.text) and 'cursor":{"value' in str(getTweetsReq.text):
                                    currentCursor = quote_plus(
                                        findall(r"\"cursor\"\:\{\"value\"\:\"((\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"\,\"cursorType\"\:\"Bottom", str(getTweetsReq.text))[0][0]
                                    )
                                    isDone1 = False
                                    while True:
                                        getTweetsReqHeaders = {
                                            "Host": "twitter.com",
                                            "Connection": "keep-alive",
                                            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                                            "DNT": "1",
                                            "x-twitter-client-language": "en",
                                            "x-csrf-token": "a9b7d0e0fe277ca386decfd4373cdd71",
                                            "x-guest-token": "{}".format(guestID),
                                            "x-twitter-active-user": "yes",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                                            "Accept": "*/*",
                                            "Sec-Fetch-Site": "same-origin",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Dest": "empty",
                                            "Referer": "https://twitter.com/",
                                            "Accept-Language": "en-US,en;q=0.9",
                                            "Cookie1": 'personalization_id="v1_cvet2wHhji0RQ6jewODqQw=="; guest_id=v1%3A161365290208151861; ct0=41ddc0c5eb88510407b5d30d4f72ca6c; _sl=1; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCP1FNbV3AToMY3NyZl9p%250AZCIlMjA3Y2VjMjliNjhhNGEwOTVmZmRhYWFmODMxOGE5OWI6B2lkIiU1MzEz%250ANDAzNDUxOTliY2E1OTI1MWY4NmY4MWQ3OTQ0MA%253D%253D--180911d4e5b56a30b643927e79cfe9fc4b20fad6; gt='
                                            + guestID,
                                        }
                                        getTweetsReq = session.get(
                                            f"https://twitter.com/i/api/2/timeline/profile/{userID}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=200&cursor={currentCursor}&userId={userID}&ext=mediaStats%2ChighlightedLabel",
                                            headers=getTweetsReqHeaders,
                                        )
                                        if "globalObjects" in str(getTweetsReq.text) and getTweetsReq.status_code == 200 and "tweets" in str(getTweetsReq.text):
                                            newResponseTweetsIds = list(getTweetsReq.json()["globalObjects"]["tweets"].keys())
                                            if len(newResponseTweetsIds) == 0:
                                                isDone1 = True
                                                break
                                            else:
                                                currentCursor = quote_plus(
                                                    findall(r"\"cursor\"\:\{\"value\"\:\"((\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"\,\"cursorType\"\:\"Bottom", str(getTweetsReq.text))[0][0]
                                                )
                                                lent = len(list(set(userTweetIdsList)))
                                                userTweetIdsList += newResponseTweetsIds
                                                if len(list(set(userTweetIdsList))) == lent:
                                                    isDone1 = True
                                                    break
                                                continue
                                        elif "Rate limit exceeded" in str(getTweetsReq.text):
                                            return {"status": "failed", "error": 1101, "user_state": None, "data": None}
                                        else:
                                            return {"status": "failed", "error": 1014, "user_state": None, "data": None}
                                isDone1 = True
                                if isDone1:
                                    searchAdaptiveGetReqHeaders = {
                                        "Host": "twitter.com",
                                        "Connection": "keep-alive",
                                        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                                        "DNT": "1",
                                        "x-twitter-client-language": "en",
                                        "x-guest-token": "{}".format(guestID),
                                        "x-twitter-active-user": "yes",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                                        "Accept": "*/*",
                                        "Sec-Fetch-Site": "same-origin",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Dest": "empty",
                                        "Referer": "https://twitter.com/search?q={}&src=typed_query&f=live".format(userName),
                                        "Accept-Language": "en-US,en;q=0.9",
                                    }
                                    searchAdaptiveGetReq = session.get(
                                        f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=(from%3A{userName})%20-filter%3Areplies&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CsignalsReactionMetadata%2CsignalsReactionPerspective%2CvoiceInfo",
                                        headers=searchAdaptiveGetReqHeaders,
                                    )
                                    if "globalObjects" in searchAdaptiveGetReq.text and searchAdaptiveGetReq.status_code == 200 and "tweets" in searchAdaptiveGetReq.text:
                                        resultTweetsIds = []
                                        for tweet_id in searchAdaptiveGetReq.json()["globalObjects"]["tweets"]:
                                            if "Twitter Media Policy" in searchAdaptiveGetReq.json()["globalObjects"]["tweets"][tweet_id]["full_text"]:
                                                break
                                            else:
                                                resultTweetsIds.append(tweet_id)
                                        searchTweetIdsList += resultTweetsIds
                                        if len(resultTweetsIds) != 0:
                                            if 'cursorType":"Bottom' in str(searchAdaptiveGetReq.text) and 'cursor":{"value' in str(searchAdaptiveGetReq.text):
                                                currentCursor2 = quote_plus(
                                                    findall(r"\"cursor\"\:\{\"value\"\:\"(scroll:(\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"", str(searchAdaptiveGetReq.text))[0][0]
                                                )
                                                isDone = False
                                                while True:
                                                    searchAdaptiveGetReqHeaders = {
                                                        "Host": "twitter.com",
                                                        "Connection": "keep-alive",
                                                        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                                                        "DNT": "1",
                                                        "x-twitter-client-language": "en",
                                                        "x-guest-token": "{}".format(guestID),
                                                        "x-twitter-active-user": "yes",
                                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                                                        "Accept": "*/*",
                                                        "Sec-Fetch-Site": "same-origin",
                                                        "Sec-Fetch-Mode": "cors",
                                                        "Sec-Fetch-Dest": "empty",
                                                        "Referer": "https://twitter.com/search?q={}&src=typed_query&f=live".format(userName),
                                                        "Accept-Language": "en-US,en;q=0.9",
                                                    }
                                                    searchAdaptiveGetReq = session.get(
                                                        f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=(from%3A{userName})%20-filter%3Areplies&tweet_search_mode=live&count=20&query_source=typed_query&cursor={currentCursor2}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel",
                                                        headers=searchAdaptiveGetReqHeaders,
                                                    )
                                                    if (
                                                        "globalObjects" in str(searchAdaptiveGetReq.text)
                                                        and searchAdaptiveGetReq.status_code == 200
                                                        and "tweets" in str(searchAdaptiveGetReq.text)
                                                    ):
                                                        newResultTweetsIds = list(searchAdaptiveGetReq.json()["globalObjects"]["tweets"].keys())
                                                        if len(newResultTweetsIds) == 0:
                                                            isDone = True
                                                            break
                                                        else:
                                                            currentCursor2 = quote_plus(
                                                                findall(r"\"cursor\"\:\{\"value\"\:\"(scroll:(\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"", str(searchAdaptiveGetReq.text))[0][0]
                                                            )
                                                            searchTweetIdsList += newResultTweetsIds
                                                            continue
                                                    elif "Rate limit exceeded" in str(searchAdaptiveGetReq.text):
                                                        return {"status": "failed", "error": 1101, "user_state": None, "data": None}
                                                    else:
                                                        return {"status": "failed", "error": 1013, "user_state": None, "data": None}
                                                if isDone:
                                                    isFound = False
                                                    for eachId in searchTweetIdsList:
                                                        if eachId in userTweetIdsList:
                                                            isFound = True
                                                            break
                                                        else:
                                                            continue
                                                    if len(searchTweetIdsList) >= 1:
                                                        isFound = True
                                                    if isFound == True:
                                                        return {"status": "success", "error": None, "user_state": 2, "data": userDetails}
                                                    else:
                                                        return {"status": "success", "error": None, "user_state": 1, "data": userDetails}
                                                else:
                                                    return {"status": "failed", "error": 1100, "user_state": None, "data": None}
                                            else:
                                                return {"status": "failed", "error": 1011, "user_state": None, "data": None}
                                        else:
                                            return {"status": "success", "error": None, "user_state": 1, "data": userDetails}
                                    else:
                                        return {"status": "failed", "error": 1010, "user_state": None, "data": None}
                                else:
                                    return {"status": "failed", "error": 1100, "user_state": None, "data": None}
                            else:
                                return {"status": "success", "error": None, "user_state": 6, "data": userDetails}
                        elif "UserUnavailable" in str(getTweetsReq.text):
                            return {"status": "success", "error": None, "user_state": 5, "data": userDetails}
                        else:
                            return {"status": "failed", "error": 1009, "user_state": None, "data": None}
                    elif "Rate limit exceeded" in str(graphqlGetReq.text):
                        return {"status": "failed", "error": 1101, "user_state": None, "data": None}
                    elif graphqlGetReq.status_code == 200 and "user" in str(graphqlGetReq.text) and "User has been suspended" in str(graphqlGetReq.text):
                        return {"status": "success", "error": None, "user_state": 4, "data": None}
                    elif '"name":"NotFoundError"' in str(graphqlGetReq.text):
                        return {"status": "success", "error": None, "user_state": 3, "data": None}
                    else:
                        return {"status": "failed", "error": 1008, "user_state": None, "data": None}
                else:
                    return {"status": "failed", "error": 1007, "user_state": None, "data": None}
            else:
                return {"status": "failed", "error": 1006, "user_state": None, "data": None}
    except:
        return {"status": "failed", "error": 1100, "user_state": None, "data": None}


def getDetails(userName, proxy):
    try:
        with requests.Session() as session:
            if proxy:
                proxyDict = {"https": "{}".format(proxy), "http": "{}".format(proxy)}
                session.proxies.update(proxyDict)
            getProfileHeaders = {
                "Host": "twitter.com",
                "Connection": "keep-alive",
                "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
            }
            getProfile = session.get(f"https://twitter.com/{userName}", headers=getProfileHeaders)
            if getProfile.status_code == 200 and 'decodeURIComponent("gt' in getProfile.text:
                guestToken = findall('decodeURIComponent\("gt=(\d*);', getProfile.text)[0]
                getInfoHeaders = {
                    "Host": "twitter.com",
                    "Connection": "keep-alive",
                    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                    "DNT": "1",
                    "x-twitter-client-language": "en",
                    "x-csrf-token": "1",
                    "sec-ch-ua-mobile": "?0",
                    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                    "content-type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                    "x-guest-token": f"{guestToken}",
                    "x-twitter-active-user": "no",
                    "sec-ch-ua-platform": '"Windows"',
                    "Accept": "*/*",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": f"https://twitter.com/{userName}",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Cookie": f"gt={guestToken}; ct0=1",
                }
                getInfo = session.get(
                    f"https://twitter.com/i/api/graphql/B-dCk4ph5BZ0UReWK590tw/UserByScreenName?variables=%7B%22screen_name%22%3A%22{userName}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%7D",
                    headers=getInfoHeaders,
                )
                if '"data":{"user":' in getInfo.text and getInfo.status_code == 200:
                    userInfo = getInfo.json()["data"]["user"]["result"]["legacy"]
                    return {"status": "success", "error": None, "user_state": 2, "data": userInfo}
                elif "Rate limit exceeded" in str(getInfo.text):
                    return {"status": "failed", "error": 1101, "user_state": None, "data": None}
                elif getInfo.status_code == 200 and "user" in str(getInfo.text) and "User has been suspended" in str(getInfo.text):
                    return {"status": "success", "error": None, "user_state": 4, "data": None}
                elif """"message":"Not found""" in str(getInfo.text):
                    return {"status": "success", "error": None, "user_state": 3, "data": None}
                else:
                    return {"status": "failed", "error": 1016, "user_state": None, "data": None}
            else:
                return {"status": "failed", "error": 1015, "user_state": None, "data": None}
    except:
        return {"status": "failed", "error": 1100, "user_state": None, "data": None}


if __name__ == "__main__":
    userName = sys.argv[1]
    # searchResult = checkSearch(userName, False)
    shadowResult = checkShadow(userName, False)
    # detailsResult = getDetails(userName, False)
    # print(dumps(shadowResult))
    # print(dumps({"search": searchResult, "shadow": shadowResult, "details": detailsResult}), end="")
    print(dumps(shadowResult), end="")
    # print(dumps({"shadow": shadowResult, "details": detailsResult}), end="")
