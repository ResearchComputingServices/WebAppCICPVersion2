function changeLang(siteLang) {
    var siteUrl = window.location.href;
    var link = document.getElementById("langButton");
    link.getAttribute("href");

    if (siteUrl == "http://134.117.214.42/en/") {
        console.log("case1")
        siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
        link.setAttribute("href",
            siteUrl);
        console.log(siteUrl)
    }
    else if (siteUrl == "http://134.117.214.42/fr/") {
        console.log("case2")
        siteUrl = siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
        link.setAttribute("href",
            siteUrl);
        console.log(siteUrl)
    }

    else {
        if (siteLang == 'fr') {
            if (siteUrl.length > 21) {
                console.log("case3")
                siteUrl = siteUrl.substring(0, 21) + "/fr" + siteUrl.substring(21);
                console.log(siteUrl)
            }
            else {
                console.log("case4")
                siteUrl = siteUrl + "/fr/"
                console.log(siteUrl)
            }

        }

        else if (siteLang == 'en') {
            if (siteUrl.length > 21) {
                console.log("case5")
                siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
                console.log(siteUrl)
            }
            else {
                console.log("case6")
                siteUrl = siteUrl + "/en/"
                console.log(siteUrl)
            }
        }

        link.setAttribute("href", siteUrl);

    };
};