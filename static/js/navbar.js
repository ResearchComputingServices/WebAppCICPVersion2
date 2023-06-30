function changeLang(siteUrl) {
    console.log("Inside Changelang function");
    var link = document.querySelector("a");
    link.getAttribute("href");
    if (siteUrl.includes("/en/")) {
        siteUrl.replace("/en/", "/fr/")

        link.setAttribute("href",
            siteUrl);
        link.textContent = "English";
    }


}