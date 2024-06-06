// 异步加载JSON文件
function loadJSON(callback) {
    // 创建一个新的XMLHttpRequest对象，用于异步加载数据
    var xhr = new XMLHttpRequest();
    xhr.overrideMimeType("application/json");
    xhr.open('GET', './js/1.json', true); // 在这里指定要加载的JSON文件名（假设JSON文件名为1.json）
    xhr.onreadystatechange = function() {
        // 当请求状态发生变化时，检查是否成功加载数据
        if (xhr.readyState == 4 && xhr.status == 200) {
            // 调用传递的回调函数，将响应文本传递给它
            callback(xhr.responseText);
        }
    };
    // 发起请求
    xhr.send(null);
}

// 处理JSON数据
function processJSON(data) {
    // 获取一个HTML元素，用于将JSON数据添加到页面
    var article = document.getElementById('article');
    // 解析JSON数据
    var jsonData = JSON.parse(data);
    var itemCount = jsonData.length;
    //console.log(itemCount);
    // 获取id为cnt的p元素
    var pElement = document.getElementById('cnt');

    // 修改文本值
    pElement.textContent = itemCount;

    // 遍历JSON数据中的每个项目
    for (var i = itemCount - 1; i >= 0; i--) {
        var item = jsonData[i];

        // 获取父元素
        var articles = document.getElementById('articles');

        // 创建article-item div元素，设置样式为width: 100%
        var articleItem = document.createElement('div');
        articleItem.className = 'article-item';
        articleItem.style.width = '100%';

        // 创建h2元素，设置class为article-title，文本为变量的值
        var h2Element = document.createElement('h2');
        h2Element.className = 'article-title';
        h2Element.textContent = item.title;

        // 创建p元素，文本为变量的值
        var pElement = document.createElement('p');
        pElement.textContent = item.content;

        // 如果item.img有值存在，创建img标签
        if (item.img) {
            var imgElement = document.createElement('img');
            imgElement.src = './img/' + item.img;
            imgElement.style.width = '140px';
            imgElement.style.height = 'auto';
            imgElement.style.borderRadius = '5%';
            imgElement.style.border = '3px solid gray';
            imgElement.style.display = 'block';
            articleItem.appendChild(imgElement);
        }


        // 创建article-data div元素
        var articleData = document.createElement('div');
        articleData.className = 'article-data';

        // 创建第一个span元素，文本为变量的值
        var span1 = document.createElement('span');
        span1.textContent = item.tab;

        // 创建第二个span元素，文本为变量的值
        var span2 = document.createElement('span');
        span2.textContent = item.time;

        // 将创建的元素按照嵌套关系添加到页面中
        articleData.appendChild(span1);
        articleData.appendChild(span2);
        articleItem.appendChild(h2Element);
        articleItem.appendChild(pElement);
        if (item.img) {
            articleItem.appendChild(imgElement);
        }
        articleItem.appendChild(articleData);
        articles.appendChild(articleItem);


        console.log(item.title);
        console.log('已执行');
    }
}

// 调用函数加载和处理JSON数据
loadJSON(processJSON);