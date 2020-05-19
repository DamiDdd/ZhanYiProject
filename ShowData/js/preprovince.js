let url = window.location.href;
var province = decodeURI(url.split("=")[1] || "湖北");
// 设置标题
let titleStr = province + "疫情动态";
let title = document.createElement("title");
title.innerText = titleStr;
$("head")[0].appendChild(title);
// 动态引入地图JS文件
let mapScript = document.createElement("script");
var srcStr = "province/" + provinceDic[province] + ".js";
mapScript.setAttribute("src", srcStr);
mapScript.setAttribute("type", "text/javascript");
mapScript.setAttribute("charset", "utf-8");
// 找到province.js文件的script标签的位置
let indexJs = document.querySelector("#indexJs");
// 将引入的地图文件置于province.js前
document.getElementsByTagName("head")[0].insertBefore(mapScript, indexJs);