function changeLang(siteLang) {
    var siteUrl = window.location.href;
    var link = document.getElementById("langButton");
    link.getAttribute("href");

    if (siteUrl == "http://134.117.214.42/en/") {
        window.alert("case1")
        siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
        link.setAttribute("href",
            siteUrl);
        window.alert(siteUrl)
    }
    else if (siteUrl == "http://134.117.214.42/fr/") {
        window.alert("case2")
        siteUrl = siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
        link.setAttribute("href",
            siteUrl);
        window.alert(siteUrl)
    }

    else {
        if (siteLang == 'fr') {
            if (siteUrl.length > 30) {
                window.alert("case3")
                siteUrl = siteUrl.substring(0, 21) + "/fr" + siteUrl.substring(21);
                window.alert(siteUrl)
            }
            else {
                window.alert("case4")
                siteUrl = siteUrl + "/fr/"
                window.alert(siteUrl)
            }

        }

        else if (siteLang == 'en') {
            if (siteUrl.length > 30) {
                window.alert("case5")
                siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
                window.alert(siteUrl)
            }
            else {
                window.alert("case6")
                siteUrl = siteUrl + "/en/"
                window.alert(siteUrl)
            }
        }

        link.setAttribute("href", siteUrl);

    };
};