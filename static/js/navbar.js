// function changeLang() {
//   var siteUrl = window.location.href;
//   var link = document.getElementById("langButton");

//   var currentLang = getLanguageFromUrl(siteUrl);
//   var targetLang = currentLang === "en" ? "fr" : "en";

//   var langSegment = "/" + currentLang + "/";
//   var replacedUrl = siteUrl.replace(langSegment, "/" + targetLang + "/");

//   if (replacedUrl === siteUrl) {
//     return; // No language segment replacement needed, exit function
//   }

//   link.setAttribute("href", replacedUrl);
//   window.location.href = replacedUrl;
// }

// function getLanguageFromUrl(url) {
//   var langSegment = url.match(/\/(en|fr)\//);
//   if (langSegment && langSegment.length > 1) {
//     return langSegment[1];
//   }
//   return ""; // Default language if no language segment found
// }



function changeLang() {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var currentLang = getLanguageFromUrl(siteUrl);
  var targetLang = currentLang === "en" ? "fr" : "en";
  var altText = targetLang === "en" ? "Francias" : "English";

  var langSegment = "/" + currentLang + "/";
  var replacedUrl = siteUrl.replace(langSegment, "/" + targetLang + "/");

  if (replacedUrl === siteUrl) {
    return; // No language segment replacement needed, exit function
  }

  link.setAttribute("href", replacedUrl);
  link.innerText = altText;
  window.location.href = replacedUrl;


  function getLanguageFromUrl(url) {
    var langSegment = url.match(/\/(en|fr)\//);
    if (langSegment && langSegment.length > 1) {
      return langSegment[1];
    }
    return ""; // Default language if no language segment found
  }
};
