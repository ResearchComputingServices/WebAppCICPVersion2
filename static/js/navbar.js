function getLanguageFromUrl(url) {
  var langSegment = url.match(/\/(en|fr)\//);
  if (langSegment && langSegment.length > 1) {
    return langSegment[1];
  }
  return ""; // Default language if no language segment found
}

function changeLang(event) {
  event.preventDefault(); // Prevent the default behavior of the anchor

  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var currentLang = getLanguageFromUrl(siteUrl);
  var targetLang = currentLang === "en" ? "fr" : "en";

  var langSegment = "/" + currentLang + "/";
  var replacedUrl = siteUrl.replace(langSegment, "/" + targetLang + "/");

  if (replacedUrl === siteUrl) {
    return; // No language segment replacement needed, exit function
  }

  var buttonText = targetLang === "en" ? "Français" : "English";
  link.innerText = buttonText;
  window.location.href = replacedUrl; // Navigate to the new language URL
}