function changeLang(siteLang) {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var isFrench = siteLang === 'fr';
  var langSegment = isFrench ? '/fr/' : '/en/';

  var replacedUrl;

  if (siteUrl.includes('/en/')) {
    replacedUrl = siteUrl.replace(/\/en\//, langSegment);
  } else if (siteUrl.includes('/fr/')) {
    replacedUrl = siteUrl.replace(/\/fr\//, langSegment);
  }
  link.setAttribute("href", replacedUrl);
  window.location.replace(replacedUrl);
}
