/**
 * 
 * 畅图云 常用工具类
 * 
 */


/**
 * 请求表单
 * @param {表单配置} data 
 * @returns 
 */
function getFormDesin(data) {
    return new Promise(function(resolve, reject) {
        fetch('http://39.98.252.137:4600/api/v1/worksheet/getFilterRows', {
            method: 'post',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json;charset=UTF-8'
            }
        }).then(response => {
            if (response.ok) {
                response.json().then(json => {
                    //处理逻辑
                    if (json.code == 200) {
                        resolve(json.data)
                    }
                });
            }
        }).catch(err => {
            reject(err)
        });
    })
}