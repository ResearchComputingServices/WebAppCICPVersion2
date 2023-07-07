function changeLang(siteLang) {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var isFrench = siteLang === 'fr';
  var langSegment = isFrench ? '/fr/' : '/en/';
  alert(langSegment)

  var replacedUrl;

  if (isFrench) {
    if (siteUrl.includes('/fr/')) {
      replacedUrl = siteUrl.replace(/\/fr\//, langSegment);
    }
  } else {
    if (siteUrl.includes('/en/')) {
      replacedUrl = siteUrl.replace(/\/en\//, langSegment);
    }
  }
  link.setAttribute("href", replacedUrl);
  alert(replacedUrl)
  window.location.replace(replacedUrl);
}
