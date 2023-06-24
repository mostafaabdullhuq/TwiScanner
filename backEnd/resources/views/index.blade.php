<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    @vite('resources/css/app.css')
    @vite('node_modules/@fortawesome/fontawesome-free/css/all.min.css')
    <link rel="shortcut icon" href="{{ asset('images/logo-small.jpg') }}" type="image/x-icon" />
    <title>TwiScanner</title>
</head>

<body class="h-screen flex flex-col gap-4 bg-white">
    <section class="container text-center grid lg:grid-cols-2 grid-cols-1 items-center gap-10 lg:py-4 pt-24">
        <div class="flex flex-col gap-4 justify-start animate-bounce">
            <img src="{{ asset('images/logo.png') }}" alt="Website logo" srcset="" class="" />
            <p class="text-3xl ml-2 font-semibold text-gray-400 lg:text-left">
                Find out if you are
                <span class="animate-pulse">visible</span> in
                <span class="text-sky-500">twitter</span> search!
            </p>
        </div>
        <img src="{{ asset('images/hero.jpeg') }}" alt="" srcset="" class="" />
    </section>
    <!-- main page container  -->
    <main class="container flex flex-col gap-4 py-10 flex-1">
        <!-- First section container -->
        <section class="flex lg:flex-row flex-col gap-4">
            <!-- user search card -->
            <div class="card lg:w-2/3 flex flex-col gap-4 lg:order-1">
                <p id="errormessage" class="hidden bg-red-600 text-white p-4 text-center text-xl rounded-lg"></p>
                <input
                    class="p-6 username-input rounded-lg drop-shadow-sm text-2xl outline-none transition-colors hover:placeholder:text-gray-500 focus:placeholder:text-white"
                    type="text" name="username" placeholder="@TwiScanner" maxlength="20" />
                <button id="checkuser"
                    class="p-6 rounded-lg drop-shadow-sm transition-colors bg-slate-600 hover:bg-slate-700 text-white uppercase text-xl font-medium">
                    Check
                </button>
            </div>

            <!-- user main details card -->
            <div class="card lg:w-2/3">
                <!-- image, name and username of the user -->
                <div class="flex gap-4 items-center mb-4 w-full">
                    <img id="profile_picture" src="{{ asset('images/logo-small.jpg') }}" alt="Profile Image"
                        loading="lazy" class="w-24 h-24 rounded-full object-cover bg-white" />
                    <div class="flex flex-1 flex-col">
                        <p id="name" class="text-2xl font-bold text-slate-800 break-all">
                            Twi Scanner
                        </p>
                        <p class="text-xl text-slate-500">
                            @<span id="username" class="username-container break-all ml-1">TwiScanner</span>
                        </p>
                    </div>
                </div>
                <p id="bio" class="w-full ml-4 text-slate-600">
                    TwiScanner makes you know more about your twitter
                    account. Find out if you are visible on twitter search
                    and get a summery about your twitter account in one
                    place.
                </p>
            </div>
        </section>
        <!-- Second section container -->
        <section class="grid lg:grid-cols-3 xl:grid-cols-4 md:grid-cols-2 grid-cols-1 gap-4">
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-magnifying-glass card-icon"></i>
                    <p class="card-title">Search Status</p>
                </div>
                <p id="search_status" class="card-info uppercase card-info-text">
                    N/A
                </p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-regular fa-clock card-icon"></i>
                    <p class="card-title">Creation Date</p>
                </div>
                <p id="creation_date" class="card-info card-info-text">
                    N/A
                </p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-user-group card-icon"></i>
                    <p class="card-title">Followers</p>
                </div>
                <p id="followers_count" class="card-info card-info-num">
                    0
                </p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-star card-icon"></i>
                    <p class="card-title">Following</p>
                </div>
                <p id="following_count" class="card-info card-info-num">
                    0
                </p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-regular fa-newspaper card-icon"></i>
                    <p class="card-title">Tweets</p>
                </div>
                <p id="tweets_count" class="card-info card-info-num">0</p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-circle-check card-icon"></i>
                    <p class="card-title">Verified</p>
                </div>
                <p id="verification_status" class="card-info card-info-text">
                    N/A
                </p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-earth-americas card-icon"></i>
                    <p class="card-title">Location</p>
                </div>
                <p id="location" class="card-info card-info-text">N/A</p>
            </div>
            <div class="card">
                <div class="flex gap-2 items-center">
                    <i class="fa-solid fa-photo-film card-icon"></i>
                    <p class="card-title">Media</p>
                </div>
                <p id="media_count" class="card-info card-info-num">0</p>
            </div>
        </section>
    </main>
    <footer class="w-full py-10">
        <p class="text-center text-slate-500">
            &copy; Copyright <span class="font-bold">2023</span> all rights
            reserved | <span class="font-bold uppercase">TwiScanner</span>
        </p>
    </footer>
    @vite('resources/js/app.js')
</body>

</html>
