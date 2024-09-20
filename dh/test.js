// 从当前目录加载 con.json 文件
fetch('https://dearxiwei.github.io/dh/1.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('无法读取文件: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        data.forEach(item => {
            if (item.type === 0) {
                // 无菜单，输出name和link
                //set_cont(item.name, item.link);
                link_generate(item.name, item.link);
            } else if (item.type === 1) {
                // 有菜单，输出name和menu
                //set_menu(item.name, item.menu);
                menu_generate(item.name, item.menu);
            }
        });
    })
    .catch(error => console.error('读取或解析JSON时出错:', error));

// 模拟 set_cont 函数
function set_cont(name, link) {
    console.log(`无菜单 -> 名称: ${name}, 链接: ${link}`);
}

// 模拟 set_menu 函数
function set_menu(name, menu) {
    console.log(`有菜单 -> 名称: ${name}, 菜单:`);
    menu.forEach(site => {
        console.log(`网站名称: ${site[0]}, 网站地址: ${site[1]}`);
    });
}

// 生成随机10位大写字母组合的函数
function generateRandomId() {
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let result = '';
    for (let i = 0; i < 10; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// 用于生成 type=0 时的链接
function link_generate(name, link) {
    // 获取html展示区元素
    const displayArea = document.querySelector('ul.mdui-list.mdui-list-dense.mdui-text-color-theme');

    // 创建新的div元素
    const divElement = document.createElement('div');
    divElement.className = 'waves-block radius mdui-col waves-effect waves-block';

    // 创建a标签和li元素
    const aElement = document.createElement('a');
    aElement.href = link;

    const liElement = document.createElement('li');
    liElement.className = 'mdui-list-item';
    liElement.textContent = name;

    // 组装元素
    aElement.appendChild(liElement);
    divElement.appendChild(aElement);

    // 将新创建的元素插入展示区
    displayArea.appendChild(divElement);
}

// 用于生成 type=1 时的菜单
function menu_generate(name, menu) {
    // 获取html展示区元素
    const displayArea = document.querySelector('ul.mdui-list.mdui-list-dense.mdui-text-color-theme');
    // 获取html菜单区元素
    const menuArea = document.querySelector('body.mdui-drawer-body-left');

    // 生成随机ID
    const randomId = generateRandomId();

    // 创建新的菜单div元素
    const menuDiv = document.createElement('div');
    menuDiv.className = 'waves-block radius mdui-col waves-effect waves-block';

    const liElement = document.createElement('li');
    liElement.className = 'mdui-list-item';
    // 这里使用生成的随机ID来设置mdui-dialog属性
    liElement.setAttribute('mdui-dialog', `{target: '#${randomId}'}`);
    liElement.textContent = name;

    // 将li元素添加到菜单div
    menuDiv.appendChild(liElement);

    // 将菜单div添加到展示区
    displayArea.appendChild(menuDiv);

    // 创建新的对话框div
    const dialogDiv = document.createElement('div');
    dialogDiv.className = 'mdui-dialog mdui-color-theme-50';
    dialogDiv.id = randomId;

    // 创建工具栏元素
    const toolbarDiv = document.createElement('div');
    toolbarDiv.className = 'mdui-toolbar';
    toolbarDiv.style.marginTop = '8px';
    toolbarDiv.style.paddingLeft = '8px';

    const titleSpan = document.createElement('span');
    titleSpan.className = 'mdui-typo-title';
    titleSpan.textContent = name;

    const spacerDiv = document.createElement('div');
    spacerDiv.className = 'mdui-toolbar-spacer';

    const buttonDiv = document.createElement('div');
    buttonDiv.className = 'waves-circle';

    const closeButton = document.createElement('button');
    closeButton.className = 'mdui-btn mdui-btn-icon';
    closeButton.setAttribute('mdui-dialog-close', '');

    const closeIcon = document.createElement('i');
    closeIcon.className = 'mdui-icon material-icons';
    closeIcon.textContent = 'close';

    closeButton.appendChild(closeIcon);
    buttonDiv.appendChild(closeButton);
    toolbarDiv.appendChild(titleSpan);
    toolbarDiv.appendChild(spacerDiv);
    toolbarDiv.appendChild(buttonDiv);

    // 创建内容区
    const ulElement = document.createElement('ul');
    ulElement.className = 'mdui-list mdui-dialog-content mdui-list-dense';

    const rowDiv = document.createElement('div');
    rowDiv.className = 'mdui-row-xs-1 mdui-row-sm-2 mdui-row-md-3 mdui-row-lg-4 mdui-row-gapless';

    ulElement.appendChild(rowDiv);
    dialogDiv.appendChild(toolbarDiv);
    dialogDiv.appendChild(ulElement);

    // 遍历menu生成链接
    menu.forEach(item => {
        const divElement = document.createElement('div');
        divElement.className = 'waves-block radius mdui-col waves-effect waves-block';

        const aElement = document.createElement('a');
        aElement.href = item[1];

        const liElement = document.createElement('li');
        liElement.className = 'mdui-list-item';
        liElement.textContent = item[0];

        aElement.appendChild(liElement);
        divElement.appendChild(aElement);

        rowDiv.appendChild(divElement);
    });


    // 将对话框div添加到菜单区
    menuArea.appendChild(dialogDiv);
}