// 从当前目录加载 con.json 文件
fetch('./con.json')
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
                set_cont(item.name, item.link);
            } else if (item.type === 1) {
                // 有菜单，输出name和menu
                set_menu(item.name, item.menu);
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