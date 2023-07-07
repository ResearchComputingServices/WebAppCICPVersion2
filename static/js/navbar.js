function changeLang(siteLang) {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var isFrench = siteLang === 'fr';
  var langSegment = isFrench ? '/fr/' : '/en/';
  alert(langSegment)

  var replacedUrl;

  if (siteUrl.includes('/en/')) {
    alert("Case1")
    replacedUrl = siteUrl.replace(/\/en\//, langSegment);
    alert(replacedUrl)
  } else if (siteUrl.includes('/fr/')) {
    alert("Case2")
    replacedUrl = siteUrl.replace(/\/fr\//, langSegment);
    alert(replacedUrl)
  }
  link.setAttribute("href", replacedUrl);
  alert("replacedUrl in window", replacedUrl)
  window.location.replace(replacedUrl);
}
