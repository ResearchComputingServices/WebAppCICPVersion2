// function changeLang(siteLang) {
//   var siteUrl = window.location.href;
//   var link = document.getElementById("langButton");

//   var isFrench = siteLang === 'fr';
//   var langSegment = isFrench ? '/fr/' : '/en/';

//   var replacedUrl;

//   if (isFrench) {
//     if (siteUrl.includes('/en/')) {

//       replacedUrl = siteUrl.replace(/\/en\//, langSegment);
//     }
//   } else {

//     replacedUrl = siteUrl.replace(/\/fr\//, langSegment);


//   }
//   link.setAttribute("href", replacedUrl);
//   window.location = replacedUrl;
// }
function changeLang() {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var currentLang = getLanguageFromUrl(siteUrl);
  var targetLang = currentLang === "en" ? "fr" : "en";

  var langSegment = "/" + currentLang + "/";
  var replacedUrl = siteUrl.replace(langSegment, "/" + targetLang + "/");

  if (replacedUrl === siteUrl) {
    return; // No language segment replacement needed, exit function
  }

  link.setAttribute("href", replacedUrl);
  window.location.href = replacedUrl;
}

function getLanguageFromUrl(url) {
  var langSegment = url.match(/\/(en|fr)\//);
  if (langSegment && langSegment.length > 1) {
    return langSegment[1];
  }
  return ""; // Default language if no language segment found
}
