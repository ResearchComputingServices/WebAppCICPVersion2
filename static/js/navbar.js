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
  } else {
    var urlSegments = siteUrl.split('/');
    var themeIndex = urlSegments.indexOf('theme');
    var dateIndex = urlSegments.indexOf('date');

    if (themeIndex !== -1) {
      urlSegments.splice(themeIndex, 0, langSegment);
    } else if (dateIndex !== -1) {
      urlSegments.splice(dateIndex, 0, langSegment);
    } else {
      urlSegments.push(langSegment);
    }

    replacedUrl = urlSegments.join('/');
  }

  link.setAttribute("href", replacedUrl);
  window.location.replace(replacedUrl);
}

