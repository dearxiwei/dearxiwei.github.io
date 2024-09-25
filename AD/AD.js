function createWebsiteLinks() {
    // 网站链接列表
    // const websites = [
    //     "https://www.example1.com",
    //     "https://www.example2.com",
    //     "https://www.example3.com",
    //     "https://www.example4.com",
    //     "https://www.example5.com"
    // ];

    // 遍历列表并创建div和a标签
    websites.forEach(url => {
        // 创建div元素
        const container = document.createElement('div');
        container.className = 'container';

        // 创建a标签
        const link = document.createElement('a');
        link.href = url;
        link.target = "_blank";
        link.textContent = url;

        // 将a标签添加到div中
        container.appendChild(link);

        // 将div添加到body中
        document.body.appendChild(container);

        // 添加br标签
        document.body.appendChild(document.createElement('br'));
    });
}

const webkey = "MTExMQ=="; // 替换为你的实际webkey

function createFloatingWindow() {
    // 创建悬浮窗div元素
    const overlay = document.createElement('div');
    overlay.className = 'overlay';

    // 创建文本输入框
    const input = document.createElement('input');
    input.type = 'number';
    input.placeholder = '请输入数字';

    // 创建按钮
    const button = document.createElement('button');
    button.textContent = '提交';
    button.onclick = function() {
        key(input.value, overlay);
    };

    // 将输入框和按钮添加到悬浮窗中
    overlay.appendChild(input);
    overlay.appendChild(button);

    // 将悬浮窗添加到body中
    document.body.appendChild(overlay);
}

function key(inputValue, overlay) {
    // 将输入的数字转换为 Base64 编码
    const encodedInputValue = btoa(inputValue);

    // 与webkey进行对比（webkey也需要是 Base64 编码）
    if (encodedInputValue === webkey) {
        // 隐藏悬浮窗
        overlay.style.display = 'none';
        // 调用createWebsiteLinks函数
        createWebsiteLinks();
    } else {
        alert('输入不正确，请重试。');
    }
}
createFloatingWindow();

//  https://www.bejson.com/encrypt/jsobfuscate/
//  js加密配置如下：
//  基础配置 :                  方法变量重命名
//  字符串设置(全选并默认):      字符串加密  字符串编码base64    字符串加密系数0.5   旋转字符串  重排字符串  分割字符串10    变量加密    Unicode转义序列