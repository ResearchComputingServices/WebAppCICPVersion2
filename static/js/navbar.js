// function getLanguageFromUrl(url) {
//   var langSegment = url.match(/\/(en|fr)\//);
//   if (langSegment && langSegment.length > 1) {
//     return langSegment[1];
//   }
//   return ""; // Default language if no language segment found
// }

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

//   var buttonText = targetLang === "fr" ? "English" : "Français";
//   link.setAttribute("href", replacedUrl);
//   link.innerText = buttonText;
//   window.location.href = replacedUrl;
// }

// // Add an event listener to the link element
// document.getElementById("langButton").addEventListener("click", changeLang);


function getLanguageFromUrl(url) {
  var langSegment = url.match(/\/(en|fr)\//);
  if (langSegment && langSegment.length > 1) {
    return langSegment[1].toLowerCase(); // Return language code in lowercase
  }
  return ""; // Default language if no language segment found
}

function updateButtonText() {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var currentLang = getLanguageFromUrl(siteUrl);

  var buttonTextElement = link.querySelector('span[data-en], span[data-fr]');
  var buttonText = currentLang === "fr" ? buttonTextElement.getAttribute('data-en') : buttonTextElement.getAttribute('data-fr');

  link.innerText = buttonText;
}

// Update button text based on the user's current language
updateButtonText();

// Add an event listener to the link element
document.getElementById("langButton").addEventListener("click", function (event) {
  event.preventDefault();
  var siteUrl = window.location.href;
  var currentLang = getLanguageFromUrl(siteUrl);
  var targetLang = currentLang === "en" ? "fr" : "en";
  var langSegment = "/" + currentLang + "/";
  var replacedUrl = siteUrl.replace(langSegment, "/" + targetLang + "/");
  if (replacedUrl === siteUrl) {
    return;
  }
  window.location.href = replacedUrl;
});