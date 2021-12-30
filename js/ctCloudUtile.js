/**
 * 
 * 畅图云 常用工具类
 * 工具类列表：
 * 1.请求表单
 * 2.盾构线路
 * 3.盾构线路动画
 * 
 */


/**
 * *********************************************    请求表单    *********************************************
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


/**
 * **************************************************** 盾构线路 *********************************************
 */
class ShieldLine {
    /**
     * 处理点数据到数组
     * @param {geojson points} gs 
     */
    constructor(gs) {
            if (gs) {
                const points = []
                gs.features.forEach(e => {
                    points.push([e.geometry.coordinates[0], e.geometry.coordinates[1], 0])
                });
                this.points = points;
            }
        }
        /**
         * 绘制普通线
         * @param {points} p 
         * @param {color} c 
         * @returns 
         */
    drawLine(p, c) {
            const lineGeo = new THREE.Geometry();
            let lineMaterial = new THREE.LineBasicMaterial({ color: c });
            for (var i = 0; i < p.length - 1; i++) {
                const pt0 = new THREE.Vector3(p[i][0], p[i][1], p[i][2]);
                const pt1 = new THREE.Vector3(p[i + 1][0], p[i + 1][1], p[i + 1][2]);
                lineGeo.vertices.push(pt0, pt1);
            }
            const line = new THREE.Line(lineGeo, lineMaterial);
            return line
        }
        /**
         * 绘制带宽度的线  Line2库
         * @param {points [x1,y1,z1,x2,y2,z2]} p  
         * @param {颜色} color 
         * @param {线宽} lineWidth 
         * @returns  线
         */
    drawWidthLine(p, color, lineWidth) {
            const geometry = new THREE.LineGeometry();
            geometry.setPositions(p);
            geometry.verticesNeedUpdate = true;
            let material = new THREE.LineMaterial({
                color: color,
                linewidth: lineWidth,
            });
            material.resolution.set(window.innerWidth, window.innerHeight);
            return new THREE.Line2(geometry, material);
        }
        /**
         * 传入多少个点，画多少个盾构环,最后一个画红色
         * @param {points} p
         * @param {line_name} n 
         * @param {color} c 
         * @param {radius} r 
         */
    drawShieldLine(p, n, c, r) {
        const group = new THREE.Group();
        for (var i = 0; i < p.length - 1; i++) {
            const x1 = parseFloat(p[i][0]);
            const y1 = parseFloat(p[i][1]);
            const z1 = parseFloat(p[i][2]);
            const x2 = parseFloat(p[i + 1][0]);
            const y2 = parseFloat(p[i + 1][1]);
            const z2 = parseFloat(p[i + 1][2]);
            const x = (x2 + x1) / 2;
            const y = (y2 + y1) / 2;
            const z = (z2 + z1) / 2;
            const pt0 = new THREE.Vector3(x1, y1, z1);
            const pt1 = new THREE.Vector3(x2, y2, z2);
            const cylinderHeight = pt1.distanceTo(pt0);
            const axis = new THREE.Vector3(0, 1, 0);
            let cylinder, cylinderMaterial;
            const cylinderGeo = new THREE.CylinderGeometry(r, r, cylinderHeight, 32);
            // 盾构环
            cylinderMaterial = new THREE.MeshLambertMaterial({ color: i === (p.length - 2) ? 0xff0000 : c, side: THREE.DoubleSide, opacity: 0.1 });
            // cylinderMaterial = new THREE.MeshLambertMaterial({ color: 0x00ff00, side: THREE.DoubleSide, opacity: 0.1 });

            cylinder = new THREE.Mesh(cylinderGeo, cylinderMaterial);
            // 设置属性
            cylinder.name = n.concat("_", i);
            Object.assign(cylinder.userData, { currentLineName: n, currentRingNum: i });
            cylinder.scale.set(r !== 0 ? r : 1, cylinderHeight !== 0 ? cylinderHeight : 1, r !== 0 ? r : 1)
            cylinder.position.set(x, y, z);
            cylinder.quaternion.setFromUnitVectors(axis, new THREE.Vector3().subVectors(pt0, pt1).normalize());

            group.add(cylinder);
        }
        group.name = n;
        return group;
    }
}


/************************************************************************盾构线路 动-画************************************************************************************************************** */
/**
 * 
 * @param {group namespaced: true} n 
 * @param {time} t 
 */
function simAnimation(n, t) {
    // 根据组名称查找组
    let group = app.query(n);
    // 隐藏组中所有盾构环
    group.children.forEach(el => {
        el.visible = false;
    })
    let tweenArray = [],
        s = 0,
        e = group.children.length;
    // 计算每个盾构环的时间
    const tmpTime = parseFloat((t / e).toFixed(3));
    for (var i = 0; i < e; i++) {
        //假设数组长度为100， 第一个数为0，最后一个数为,100
        const tween = new TWEEN.Tween({ x: i }).to({ x: i + 1 }, tmpTime).easing(TWEEN.Easing.Linear.None).onUpdate(function(m) {
            // 首先显示第0个盾构环
            let obj = group.children[parseInt(m.x) - 1];
            if (obj) {
                obj.visible = true;
            }
        }).onComplete(function(e) {
            // console.log(e);
        })
        tweenArray.push(tween);
    }
    // 执行动画
    tweenArray[0].start();
    for (let j = 1; j < tweenArray.length; j++) {
        tweenArray[j - 1].chain(tweenArray[j]);
    }
}