function stob(str) {
    // 将UTF-8编码的字符串转换为字节序列  
    var bytes = unescape(encodeURIComponent(str));

    // 将字节序列转换为Base64编码  
    var base64 = btoa(bytes);

    return base64;
};

function btos(base64) {
    // 将Base64编码字符串转换为字节序列  
    var bytes = atob(base64);

    // 将字节序列转换为UTF-8编码的字符串  
    var str = decodeURIComponent(escape(bytes));

    return str;
}
