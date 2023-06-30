function changeLang(siteLang) {
    var siteUrl = window.location.href;
    var link = document.getElementById("langButton");
    link.getAttribute("href");
    if (siteUrl.includes("en")) {
        siteUrl = siteUrl.replace("en", "fr");
        link.setAttribute("href",
            siteUrl);
    }
    else if (siteUrl.includes("fr")) {

        siteUrl = siteUrl.replace("fr", "en");
        link.setAttribute("href",
            siteUrl);
    }

    else {
        if (siteLang == 'fr') {
            if (length(siteUrl) > 21) {
                siteUrl = siteUrl.substring(0, 21) + "/fr" + currentUrl.substring(21);
            }
            else {
                siteUrl = siteUrl + "/fr/"
            }

        }

        else {
            if (length(siteUrl) > 21) {
                siteUrl.substring(0, 21) + "/en" + currentUrl.substring(21);
            }
            else {
                siteUrl = siteUrl + "/en/"
            }
        }
        link.setAttribute("href", siteUrl);

    };
};