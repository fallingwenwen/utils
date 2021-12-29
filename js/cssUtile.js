/**
 * 
 * @param {css样式} cssText 
 */
addCSS('.mapboxgl-popup-content{background-color: rgb(135 153 199 / 50%);font-size:15px;}  .linkPop a{color:#ebc60e;}');

function addCSS(cssText) {
    var style = document.createElement('style'), //创建一个style元素
        head = document.head || document.getElementsByTagName('head')[0]; //获取head元素
    style.type = 'text/css'; //这里必须显示设置style元素的type属性为text/css，否则在ie中不起作用
    if (style.styleSheet) { //IE
        var func = function() {
                try { //防止IE中stylesheet数量超过限制而发生错误
                    style.styleSheet.cssText = cssText;
                } catch (e) {

                }
            }
            //如果当前styleSheet还不能用，则放到异步中则行
        if (style.styleSheet.disabled) {
            setTimeout(func, 10);
        } else {
            func();
        }
    } else { //w3c
        //w3c浏览器中只要创建文本节点插入到style元素中就行了
        var textNode = document.createTextNode(cssText);
        style.appendChild(textNode);
    }
    head.appendChild(style); //把创建的style元素插入到head中  
}