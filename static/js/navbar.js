function changeLang(siteLang) {
    var siteUrl = window.location.href;
    var link = document.getElementById("langButton");
    link.getAttribute("href");

    if (siteLang == 'fr') {
        if (siteUrl.length > 30) {

            if (siteUrl.includes("http://134.117.214.42/fr/")) {
                window.alert("case1")
                window.alert(siteUrl)
                siteUrl = siteUrl
                link.setAttribute("href", siteUrl);
            }

            else if (siteUrl.includes("http://134.117.214.42/fr/")) {
                // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
                window.alert("case2")
                siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
                window.alert(siteUrl)
                link.setAttribute("href", siteUrl);

            }
        }
        else {

            if (siteUrl.includes("http://134.117.214.42/fr/")) {
                window.alert("case3")
                window.alert(siteUrl)
                siteUrl = siteUrl
                link.setAttribute("href", siteUrl);
            }

            else if (siteUrl.includes("http://134.117.214.42/fr/")) {
                // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
                window.alert("case4")
                siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
                window.alert(siteUrl)
                link.setAttribute("href", siteUrl);

            }
        }

    }

    else if (siteLang == 'en') {
        if (siteUrl.length > 30) {

            if (siteUrl.includes("http://134.117.214.42/en/")) {
                window.alert("case4")
                window.alert(siteUrl)
                siteUrl = siteUrl
                link.setAttribute("href", siteUrl);
            }

            else if (siteUrl.includes("http://134.117.214.42/fr/")) {
                // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
                window.alert("case5")
                siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
                window.alert(siteUrl)
                link.setAttribute("href", siteUrl);

            }

        }
        else {

            if (siteUrl.includes("http://134.117.214.42/en/")) {
                window.alert("case6")
                window.alert(siteUrl)
                siteUrl = siteUrl
                link.setAttribute("href", siteUrl);

            }

            else if (siteUrl.includes("http://134.117.214.42/fr/")) {
                window.alert("case7")
                window.alert(siteUrl)
                siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
                link.setAttribute("href", siteUrl);


            }

        }
    }



};