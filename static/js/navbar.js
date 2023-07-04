// function changeLang(siteLang) {
//     var siteUrl = window.location.href;
//     var link = document.getElementById("langButton");
//     link.getAttribute("href");

//     if (siteLang == 'fr') {
//         if (siteUrl.length > 30) {

//             if (siteUrl.includes("http://134.117.214.42/fr/")) {
//                 window.alert("case1")
//                 // siteUrl = siteUrl
//                 window.alert(siteUrl)
//                 link.setAttribute("href", siteUrl);
//                 window.location.href = siteUrl;

//             }

//             else if (siteUrl.includes("http://134.117.214.42/en/")) {
//                 // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
//                 window.alert("case2")
//                 // siteUrl = siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
//                 // link.setAttribute("href", siteUrl);
//                 var replacedUrl = siteUrl.replace(/(http:\/\/134\.117\.214\.42)\/en/, "$1/fr");
//                 window.alert(replacedUrl)
//                 link.setAttribute("href", replacedUrl);
//                 window.location.href = replacedUrl;

//             }
//         }
//         else {

//             if (siteUrl.includes("http://134.117.214.42/fr/")) {
//                 window.alert("case3")
//                 // siteUrl = siteUrl
//                 window.alert(siteUrl)
//                 link.setAttribute("href", siteUrl);
//                 window.location.href = siteUrl;
//             }

//             else if (siteUrl.includes("http://134.117.214.42/en/")) {
//                 // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
//                 window.alert("case4")
//                 // siteUrl = siteUrl.replace("http://134.117.214.42/fr/", "http://134.117.214.42/en/");
//                 // window.alert(siteUrl)
//                 // link.setAttribute("href", siteUrl);
//                 var replacedUrl = siteUrl.replace(/(http:\/\/134\.117\.214\.42)\/en/, "$1/fr");
//                 window.alert(replacedUrl)
//                 link.setAttribute("href", replacedUrl);
//                 window.location.href = replacedUrl;

//             }
//         }

//     }

//     else if (siteLang == 'en') {
//         if (siteUrl.length > 30) {

//             if (siteUrl.includes("http://134.117.214.42/en/")) {
//                 window.alert("case4")
//                 siteUrl = siteUrl
//                 window.alert(siteUrl)
//                 link.setAttribute("href", siteUrl);
//             }

//             else if (siteUrl.includes("http://134.117.214.42/fr/")) {
//                 // siteUrl = siteUrl.substring(0, 21) + "/en" + siteUrl.substring(21);
//                 window.alert("case5")
//                 // siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
//                 // window.alert(siteUrl)
//                 // link.setAttribute("href", siteUrl);
//                 var replacedUrl = siteUrl.replace(/(http:\/\/134\.117\.214\.42)\/fr/, "$1/en");
//                 window.alert(replacedUrl)
//                 link.setAttribute("href", replacedUrl);
//                 window.location.href = replacedUrl;

//             }

//         }
//         else {

//             if (siteUrl.includes("http://134.117.214.42/en/")) {
//                 window.alert("case6")
//                 siteUrl = siteUrl
//                 window.alert(siteUrl)
//                 link.setAttribute("href", siteUrl);

//             }

//             else if (siteUrl.includes("http://134.117.214.42/fr/")) {
//                 window.alert("case7")
//                 // siteUrl = siteUrl.replace("http://134.117.214.42/en/", "http://134.117.214.42/fr/");
//                 // window.alert(siteUrl)
//                 // link.setAttribute("href", siteUrl);
//                 var replacedUrl = siteUrl.replace(/(http:\/\/134\.117\.214\.42)\/fr/, "$1/en");
//                 window.alert(replacedUrl)
//                 link.setAttribute("href", replacedUrl);
//                 window.location.href = replacedUrl;

//             }

//         }
//     }



// };

function changeLang(siteLang) {
  var siteUrl = window.location.href;
  var link = document.getElementById("langButton");

  var isFrench = siteLang === 'fr';
  var langSegment = isFrench ? '/fr' : '/en';

  var replacedUrl;

  if (siteUrl.includes('/en/') && !siteUrl.includes('/token')) {
    replacedUrl = siteUrl.replace(/\/en\//, langSegment + '/');
  } else if (siteUrl.includes('/fr/') && !siteUrl.includes('/token')) {
    replacedUrl = siteUrl.replace(/\/fr\//, langSegment + '/');
  } else {
    var langUrlSegment = '/' + langSegment.substring(1);
    replacedUrl = siteUrl.replace(/\/(theme|date)\//, langUrlSegment + '/$1/');
  }

  link.setAttribute("href", replacedUrl);
  window.location.replace(replacedUrl);
}


