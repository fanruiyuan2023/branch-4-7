

    import * as THREE from "/static/ThreeJS/build/three.module.js";
    import { OrbitControls } from "/static/ThreeJS/examples/jsm/controls/OrbitControls.js";
    import { GLTFLoader } from "/static/ThreeJS/examples/jsm/loaders/GLTFLoader.js";
    import { third_person_gltf_setparames,  third_person_gltf_tick} from "/static/js/gdmeta/third_person_gltf.js";

    // 待导入的三维模型
    var gltfObj = null;
    var renderer = null;
    var scene = null;
    // 视频混合器
    var mixer = null;
    var camera= null;


    var moduleCode = window.document.getElementById("moduleCode").innerHTML
    loadModule(moduleCode);


    function loadModule(moduleCode){

        const gltfLoader = new GLTFLoader();
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
        // 增加坐标系红色代表 X 轴. 绿色代表 Y 轴. 蓝色代表 Z 轴.
        // 显示三维坐标系
        const axes = new THREE.AxesHelper(20);
        // 添加坐标系到场景中
        // scene.add(axes);
        // 是否包含动画
        var hasAnimation = false;

        // 创建一个时钟对象Clock
        var clock = new THREE.Clock();
        gltfLoader.setPath('/static/upload/'+moduleCode+"/")
            .load('module.glb', function (gltf) {
                console.log("gltf",gltf)

                const box = new THREE.Box3().setFromObject( gltf.scene );
                const moduleSize = new THREE.Vector3();
                // 获取模型大小尺寸
                box.getSize(moduleSize);
                console.log(moduleSize);
                var k = 5 / Math.max(moduleSize.x,moduleSize.y,moduleSize.z);
                //k = Math.floor(k);
                k = 1;
                gltf.scene.rotation.y = Math.PI;
                //gltf.scene.scale.set(k, k, k);
                gltf.scene.position.set(0, moduleSize.y/2, 0);
                /*
                gltf.scene.traverse(function (child) {
                    if (child instanceof THREE.Mesh) {
                        child.castShadow = true; //阴影
                        child.receiveShadow = true; //接受别人投的阴影
                        child.material.emissive = child.material.color;
                        child.material.emissiveMap = child.material.map;
                    }
                });
                */
                scene.add(gltf.scene);
                gltfObj = gltf.scene;
                ///////////////////////显示动画////////////////////////////
                /*
                if(gltf.animations.length>0){
                    hasAnimation = true;
                    mixer = new THREE.AnimationMixer(gltf);
                    var AnimationAction = mixer.clipAction(gltf.animations[0]);
                    AnimationAction.timeScale = 1; //默认1，可以调节播放速度
                    AnimationAction.loop = THREE.LoopRepeat;  //THREE.LoopOnce; //不循环播放
                    AnimationAction.clampWhenFinished = true;//暂停在最后一帧播放的状态
                    AnimationAction.play();//播放动画
                }
                */
            }, function(res){
                // 显示加载的百分比
                //console.log(res.loaded/res.total*100 + "%")
            });
        //添加一个蓝色点光源
        const light = new THREE.PointLight(0x0000ff, 1, 100, 1);
        light.position.set(0, 3, 3);
        scene.add(light);

        ///////////////////////////////////////////////////////////////
         // 添加环境光
         let ambientLight = new THREE.AmbientLight(0xffffff); //设置环境光
         scene.add(ambientLight); //将环境光添加到场景中
         let pointLight = new THREE.PointLight(0xffffff, 1, 0);
         pointLight.position.set(0.2, 0.5, 0); //设置点光源位置
         scene.add(pointLight); //将点光源添加至场景

        ///////////////////////////////////////////////////////////////

        renderer = new THREE.WebGLRenderer();
        renderer.setClearColor(new THREE.Color(0xbbbbbb));
        renderer.setSize( window.innerWidth, window.innerHeight );
        //document.body.appendChild( renderer.domElement );
        document.getElementById("divScene").appendChild( renderer.domElement );
        // 鼠标操作
        const controls = new OrbitControls(camera,renderer.domElement);//创建控件对

        camera.position.z = -3;
        camera.position.y = 2;
        camera.lookAt(new THREE.Vector3(0,0,0));

        //////////////////////////////////////////////
        // 加载第三人称
        third_person_gltf_setparames(scene, camera, controls);
        //controls.enabled = false;

        ///////////////////////////////////////////////

        animate();
    }



    function animate() {
        requestAnimationFrame( animate );
        renderer.render( scene, camera );
        third_person_gltf_tick();
    };