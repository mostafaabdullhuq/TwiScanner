"use strict";

const userNameInput = document.querySelector(".username-input"),
    userNameOutput = document.querySelector(".username-container"),
    checkButton = document.getElementById("checkuser"),
    profilePicture = document.getElementById("profile_picture"),
    fullName = document.getElementById("name"),
    userName = document.getElementById("username"),
    bioContainer = document.getElementById("bio"),
    searchStatus = document.getElementById("search_status"),
    creationDate = document.getElementById("creation_date"),
    followers = document.getElementById("followers_count"),
    following = document.getElementById("following_count"),
    tweetsCount = document.getElementById("tweets_count"),
    verificationStatus = document.getElementById("verification_status"),
    userLocation = document.getElementById("location"),
    mediaCount = document.getElementById("media_count"),
    errorMessage = document.getElementById("errormessage"),
    userRegex = new RegExp("^([a-zA-Z1-9_]){1,15}$"),
    defaultData = {
        type: 2,
        created_at: "N/A",
        description:
            "TwiScanner makes you know more about your twitter account. Find out if you are visible on twitter search and get a summery about your twitter account in one place.",
        fast_followers_count: 0,
        favourites_count: 0,
        followers_count: 0,
        friends_count: 0,
        location: "N/A",
        media_count: 0,
        name: "Twi Scanner",
        normal_followers_count: 0,
        profile_image_url_https: "/images/logo-small.jpg",
        protected: false,
        screen_name: "TwiScanner",
        statuses_count: 0,
        verified: "N/A",
        search_status: "N/A",
    },
    loadingData = {
        type: 1,
        created_at:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        description:
            "TwiScanner makes you know more about your twitter account. Find out if you are visible on twitter search and get a summery about your twitter account in one place.",
        fast_followers_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        favourites_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        followers_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        friends_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        location:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        media_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        name: "Twi Scanner",
        normal_followers_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        profile_image_url_https: "/images/logo-small.jpg",
        protected:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        screen_name: "Loading...",
        statuses_count:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        verified:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
        search_status:
            '<i class="fa-solid fa-circle-notch animate-spin text-4xl"></i>',
    };

userNameInput.addEventListener("keyup", function (e) {
    const userName = e.target.value;
    if (userName.length > 0 && userName.length <= 20) {
        userNameOutput.innerHTML = userName;
    } else if (userName.length <= 0) {
        userNameOutput.innerHTML = "twishadow";
    }
});

// a function that takes date object and convert it to Day Month Year
function formatDate(date) {
    let monthNames = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "June",
        "July",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ];

    let day = date.getDate();
    let monthIndex = date.getMonth();
    let year = date.getFullYear();

    return day + " " + monthNames[monthIndex] + " " + year;
}

// a function to handle error popup by changing it's text and show it
function showErrorMessage(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
    userNameInput.classList.add("border-2");
    userNameInput.classList.add("border-red-600");
}

function hideErrorMessage() {
    errorMessage.textContent = "";
    errorMessage.classList.add("hidden");
    userNameInput.classList.remove("border-2");
    userNameInput.classList.remove("border-red-600");
}

// a function to change the content of cards that contain info about user
function handleUserData(data) {
    if (data) {
        // get user profile picture
        profilePicture.src =
            data.profile_image_url_https || "/images/logo-small.jpg";

        // get user full name
        fullName.innerHTML = data.name || "Not Available";

        // get user username
        userName.innerHTML = data.screen_name || "Not Available";

        // get user bio
        bioContainer.innerHTML = data.description || "User doesn't have a bio.";
        // get user creation date
        if (data.type === 1 || data.type === 2) {
            creationDate.innerHTML = data.created_at;
        } else {
            creationDate.innerHTML = formatDate(new Date(data.created_at));
        }

        searchStatus.innerHTML = data.search_status || "N/A";

        // get user followers count
        followers.innerHTML = data.followers_count ?? "N/A";

        // get user following count
        following.innerHTML = data.friends_count ?? "N/A";

        // get user tweets count
        tweetsCount.innerHTML = data.statuses_count ?? "N/A";

        if (data.type === 1 || data.type === 2) {
            verificationStatus.innerHTML = data.verified;
        } else {
            // get user verification status
            if (data.verified) {
                verificationStatus.innerHTML = "Yes";
            } else {
                verificationStatus.innerHTML = "No";
            }
        }

        // get user location
        userLocation.innerHTML = data.location || "N/A";

        // get user media count
        mediaCount.innerHTML = data.media_count ?? "N/A";
    }
}

function handleCardInfo(type) {
    searchStatus.classList.remove("text-fuchsia-600");
    searchStatus.classList.remove("text-gray-600");
    searchStatus.classList.remove("text-yellow-600");
    searchStatus.classList.remove("text-red-600");
    searchStatus.classList.remove("text-green-600");
    searchStatus.classList.remove("card-info");
    searchStatus.classList.add("card-info-status");
    switch (type) {
        // if account good
        case 1:
            searchStatus.classList.add("text-green-600");
            break;
        // if account banned
        case 2:
            searchStatus.classList.add("text-red-600");

            break;
        // if account protected
        case 3:
            searchStatus.classList.add("text-fuchsia-600");
            break;
        // if account suspended
        case 4:
            searchStatus.classList.add("text-yellow-600");
            break;

        // if account not found
        case 5:
            searchStatus.classList.add("text-gray-600");
            break;
        case 6:
            searchStatus.classList.add("text-indigo-600");
            break;
        default:
            searchStatus.classList.remove("card-info-status");
            searchStatus.classList.add("card-info");
            break;
    }
}

checkButton.addEventListener("click", function (e) {
    hideErrorMessage();

    let userName = userNameInput.value;
    // if user entered not valid username
    if (userRegex.test(userName)) {
        handleCardInfo(-1);
        handleUserData(loadingData);
        fetch(`http://127.0.0.1:8000/api/search/${userName}`)
            .then((response) => {
                // if response success from backend
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(
                        "Something went wrong, please try again later."
                    );
                }
            })
            // get the response from backend
            .then((response) => {
                let responseData = response.data;

                if (responseData) {
                    responseData.type = 3;
                }

                // if user search success
                if (response.status === "success") {
                    // get user account status
                    const userStatus = response.user_state;
                    switch (userStatus) {
                        case 1:
                            responseData.search_status = "Banned";
                            handleCardInfo(2);
                            handleUserData(response.data);
                            break;
                        case 2:
                            responseData.search_status = "Good";
                            handleCardInfo(1);
                            handleUserData(response.data);
                            break;
                        case 3:
                            responseData = defaultData;
                            responseData.search_status = "Not Found";
                            handleCardInfo(5);
                            break;
                        case 4:
                            responseData = defaultData;
                            responseData.search_status = "Suspended";
                            handleCardInfo(4);
                            break;
                        case 5:
                            responseData.search_status = "Protected";
                            handleCardInfo(3);
                            break;
                        case 6:
                            responseData.search_status = "No Tweets";
                            handleCardInfo(6);
                            break;
                        default:
                            handleUserData(defaultData);
                            break;
                    }
                    handleUserData(responseData);
                }
                // if error happened in search
                else {
                    throw new Error(data);
                }
            })
            .catch((err) => {
                showErrorMessage(
                    "Something went wrong, please try again later."
                );
                handleUserData(defaultData);
            });
    } else {
        showErrorMessage("Please enter a valid username.");
        handleUserData(defaultData);
    }
});
