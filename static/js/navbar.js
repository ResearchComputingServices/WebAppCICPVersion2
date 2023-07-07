function changeLang(siteLang) {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var isFrench = siteLang === 'fr';
  var langSegment = isFrench ? '/fr/' : '/en/';


  var replacedUrl;

  if (isFrench) {
    if (siteUrl.includes('/en/')) {
      alert("Case1")
      replacedUrl = siteUrl.replace(/\/en\//, langSegment);
    }
  } else {
    alert("Case2")
    replacedUrl = siteUrl.replace(/\/fr\//, langSegment);

  }
  link.setAttribute("href", replacedUrl);
  alert(replacedUrl)
  window.location.replace(replacedUrl);
}
