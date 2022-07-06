let i = 0;
let flag = 1;

function appendChildtohtml() {
     if (i == data.length) {
          flag = 0;
          return 0;
     }

     var ul = document.getElementById("pre");
     var li = document.createElement("li");

     li.innerHTML =
          '<li> <a data-fancybox="" target="_blank"  class="video fancybox.iframe video-container" title="Play" href=\'https://www.youtube.com/watch?v=' +
          data[i]["videoId"] +
          '\'><div class="video-overlay"> <div class="middle-center"></div></div><img src=\'https://img.youtube.com/vi_webp/' +
          data[i]["videoId"] +
          '/mqdefault.webp\' width=100% height=auto ></a><div><h4 style = "color:antiquewhite ;font-family: \'Electrolize\', sans-serif;"  class="des">' +
          data[i]["title"] +
          "</h4></div></li>";
     ul.appendChild(li);
     i++;
}
if ($(window).height() + 20 >= getDocHeight()) {
     appendChildtohtml();
     appendChildtohtml();
     appendChildtohtml();
     appendChildtohtml();
}
appendChildtohtml();
appendChildtohtml();
appendChildtohtml();
appendChildtohtml();

function getDocHeight() {
     var D = document;
     return Math.max(D.body.scrollHeight, D.documentElement.scrollHeight, D.body.offsetHeight, D.documentElement.offsetHeight, D.body.clientHeight, D.documentElement.clientHeight);
}

$(window).scroll(function () {
     if ((($(window).scrollTop() + $(window).height()) | 0) >= getDocHeight() - 600) {
          appendChildtohtml();
          appendChildtohtml();
          appendChildtohtml();
          appendChildtohtml();
     }
});
