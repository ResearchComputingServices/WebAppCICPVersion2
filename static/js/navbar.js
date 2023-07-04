function changeLang(siteLang) {
    var siteUrl = window.location.href;
    var link = document.getElementById("langButton");
    link.getAttribute("href");

    if (siteUrl.includes("http://134.117.214.42/en/")) {
        siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
        link.setAttribute("href",
            siteUrl);
    }
    else if (siteUrl.includes("http://134.117.214.42/fr/")) {

        siteUrl = siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
        link.setAttribute("href",
            siteUrl);
    }

    else {
        if (siteLang == 'fr') {
            if (siteUrl.length > 21) {
                siteUrl = siteUrl.substring(0, 21) + "/fr" + siteUrl.substring(21);
            }
            else {
                siteUrl = siteUrl + "/fr/"
            }

        }

        else if (siteLang == 'en') {
            if (siteUrl.length > 21) {
                siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
            }
            else {
                siteUrl = siteUrl + "/en/"
            }
        }

        link.setAttribute("href", siteUrl);

    };
};