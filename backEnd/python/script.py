from json import loads, dumps
import sys
import requests
from re import findall

try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus
import threading
from time import sleep
import threading


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


isJobsDone = False
isJobsDone2 = False
userTweetIdsList = []
threadsCount = 1
guestID = None
currentCursor = None
currentCursor2 = None
session = None
userID = None
threadsError = False
threadsLock = threading.Lock()
isAppDone = False
searchTweetIdsList = []
cursorsList = []
isTweetFound = False


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


def handleGuestID():
    global guestID, isAppDone
    while not isAppDone:
        guestID = guest_activate(False)
        sleep(1)


def handleFirstLoop():
    global currentCursor, guestID, session, userID, isJobsDone, userTweetIdsList, threadsError, threadsLock
    while not isJobsDone:
        try:
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
                    with threadsLock:
                        isJobsDone = True
                        break
                else:
                    with threadsLock:
                        currentCursor = quote_plus(findall(r"\"cursor\"\:\{\"value\"\:\"((\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"\,\"cursorType\"\:\"Bottom", str(getTweetsReq.text))[0][0])
                        lent = len(list(set(userTweetIdsList)))
                        userTweetIdsList += newResponseTweetsIds
                        if len(list(set(userTweetIdsList))) == lent:
                            isJobsDone = True
                            break
            elif "Rate limit exceeded" in str(getTweetsReq.text):
                with threadsLock:
                    threadsError = {"status": "failed", "error": 1101, "user_state": None, "data": None}
                    isJobsDone = True
                    break
            else:
                with threadsLock:
                    threadsError = {"status": "failed", "error": 1014, "user_state": None, "data": None}
                    isJobsDone = True
                    break
        except:
            continue


def handleSecondLoop():
    global currentCursor2, guestID, session, userID, isJobsDone2, userTweetIdsList, threadsError, threadsLock, searchTweetIdsList, cursorsList
    while not isJobsDone2:
        try:
            if currentCursor2 not in cursorsList:
                # with threadsLock:
                cursorsList.append(currentCursor2)
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
                searchURL = f"https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q=(from%3A{userName})%20-filter%3Areplies&tweet_search_mode=live&count=20&query_source=typed_query&cursor={currentCursor2}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel"
                searchAdaptiveGetReq = session.get(
                    searchURL,
                    headers=searchAdaptiveGetReqHeaders,
                )
                if "globalObjects" in str(searchAdaptiveGetReq.text) and searchAdaptiveGetReq.status_code == 200 and "tweets" in str(searchAdaptiveGetReq.text):
                    newResultTweetsIds = list(searchAdaptiveGetReq.json()["globalObjects"]["tweets"].keys())
                    if len(newResultTweetsIds) == 0:
                        with threadsLock:
                            isJobsDone2 = True
                            break
                    else:
                        currentCursor2 = quote_plus(findall(r"\"cursor\"\:\{\"value\"\:\"(scroll:(\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"", str(searchAdaptiveGetReq.text))[0][0])
                        searchTweetIdsList += newResultTweetsIds
                        continue
                elif "Rate limit exceeded" in str(searchAdaptiveGetReq.text):
                    with threadsLock:
                        isJobsDone2 = True
                        threadsError = {"status": "failed", "error": 1101, "user_state": None, "data": None}
                else:
                    with threadsLock:
                        isJobsDone2 = True
                        threadsError = {"status": "failed", "error": 1013, "user_state": None, "data": None}
        except Exception as i:
            with threadsLock:
                isJobsDone2 = True
                threadsError = {"status": "failed", "error": 1100, "user_state": None, "data": str(i)}


def handleFindTweets():
    global isTweetFound, threadsError
    while not isTweetFound:
        try:
            for eachId in searchTweetIdsList:
                if eachId in userTweetIdsList:
                    isTweetFound = True
                    break
                else:
                    continue
        except Exception as i:
            threadsError = {"status": "failed", "error": 1100, "user_state": None, "data": str(i)}


def makeThreads(targetType):
    threadsList = []
    # make threads
    for _ in range(threadsCount):
        if targetType == 1:
            thread = threading.Thread(target=handleFirstLoop, daemon=True)
        elif targetType == 2:
            thread = threading.Thread(target=handleSecondLoop, daemon=True)
        else:
            thread = threading.Thread(target=handleFindTweets, daemon=True)
        threadsList.append(thread)

    for eachThread in threadsList:
        eachThread.start()


def checkShadow(userName, proxy):
    try:
        global guestID, userID, session, isJobsDone, isJobsDone2, userTweetIdsList, currentCursor, currentCursor2, isAppDone, isTweetFound, searchTweetIdsList
        with requests.Session() as session:
            session.verify = False
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
                            userInstructions = getTweetsReq.json()["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
                            if len(userInstructions) > 1:
                                jsonResponse = userInstructions[1]["entries"]
                            else:
                                return {"status": "success", "error": None, "user_state": 6, "data": userDetails}
                            for _ in jsonResponse:
                                if _["content"]["entryType"] == "TimelineTimelineItem":
                                    responseTweetsIds.append(_["sortIndex"])
                            userTweetIdsList += responseTweetsIds
                            if len(responseTweetsIds) != 0:
                                if 'cursorType":"Bottom' in str(getTweetsReq.text) and 'cursor":{"value' in str(getTweetsReq.text):
                                    currentCursor = quote_plus(
                                        findall(r"\"cursor\"\:\{\"value\"\:\"((\w?\=?\+?\-?\&?\*?\#?\_?\/?\\?)*)\"\,\"cursorType\"\:\"Bottom", str(getTweetsReq.text))[0][0]
                                    )
                                    isDone1 = False
                                    makeThreads(1)
                                    while not isJobsDone:
                                        sleep(1)
                                if threadsError:
                                    return threadsError
                                else:
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
                                        userTweets = searchAdaptiveGetReq.json()["globalObjects"]["tweets"]
                                        for tweet_id in userTweets:
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
                                                makeThreads(2)
                                                makeThreads(3)
                                                while not isJobsDone2:
                                                    if isTweetFound:
                                                        break
                                                    sleep(1)
                                                if threadsError:
                                                    return threadsError
                                                else:
                                                    isDone = True
                                                if isDone:
                                                    if isTweetFound:
                                                        return {"status": "success", "error": None, "user_state": 2, "data": userDetails}
                                                    isFound = False
                                                    for eachId in searchTweetIdsList:
                                                        if eachId in userTweetIdsList:
                                                            isFound = True
                                                            break
                                                        else:
                                                            continue
                                                    if isFound == True:
                                                        return {"status": "success", "error": None, "user_state": 2, "data": userDetails}
                                                    else:
                                                        return {"status": "success", "error": None, "user_state": 1, "data": userDetails}
                                                else:
                                                    return {"status": "failed", "error": 1100, "user_state": None, "data": "isDone"}
                                            else:
                                                return {"status": "failed", "error": 1011, "user_state": None, "data": None}
                                        else:
                                            return {"status": "success", "error": None, "user_state": 1, "data": userDetails}
                                    else:
                                        return {"status": "failed", "error": 1010, "user_state": None, "data": None}
                                else:
                                    return {"status": "failed", "error": 1100, "user_state": None, "data": "isDone1"}
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
    except Exception as i:
        return {"status": "failed", "error": 1100, "user_state": None, "data": f"checkShadowException: {str(i)}"}


if __name__ == "__main__":
    try:
        threading.Thread(target=handleGuestID, daemon=True).start()
        userName = sys.argv[1]
        shadowResult = checkShadow(userName, False)
        isAppDone = True
        print(dumps(shadowResult), end="")
    except Exception as i:
        print(dumps({"status": "failed", "error": 1100, "user_state": None, "data": f"mainException: {str(i)}"}))
