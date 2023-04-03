
import * as THREE from "/static/ThreeJS/build/three.module.js";
import { GLTFLoader } from "/static/ThreeJS/examples/jsm/loaders/GLTFLoader.js";

let idleAction, walkAction, runAction;
var scene = null;
var third_carame = null;
var third_player = null;
var mixer = null;
var clock = new THREE.Clock();
var mixer = null;
var controls = null;

var pressKey = false;

var speed = 3;
var rotate_speed = 10;

var last_behavior = "idle";
var curr_behavior = "idle";

var moveForward = false;
var moveBackward = false;
var moveLeft = false;
var moveRight = false;
var run = false;

// 草地
var grass = null;
// 场景中的所有物体和子物体(用于碰撞检测)
var objectsInScene = [];

var third_player_modele_path = "/static/modules/Xbot.glb";

function third_person_gltf_setparames(t_scene, t_camera, t_controls){

    scene = t_scene;
    third_carame = t_camera;
    controls = t_controls

    third_person_gltf_init();

    getAll3DObjsInScene();
}

function third_person_gltf_init(){
    document.addEventListener( 'keydown', onKeyDown );
    document.addEventListener( 'keyup', onKeyUp );
    createGrass();
    load_module();
}

function load_module(){
    const loader = new GLTFLoader();
    loader.load( third_player_modele_path, function ( gltf ) {

        third_player = gltf.scene;
        scene.add( third_player );

        third_player.traverse( function ( object ) {
            if ( object.isMesh ) object.castShadow = true;
        } );

        const animations = gltf.animations;
        mixer = new THREE.AnimationMixer( third_player );
        idleAction = mixer.clipAction( animations[ 2 ] );
        walkAction = mixer.clipAction( animations[ 6 ] );
        runAction = mixer.clipAction( animations[ 3 ] );
        setWeight(idleAction, 0);
        setWeight(walkAction, 0);
        setWeight(runAction, 1);
        idleAction.play();
        walkAction.play();
        runAction.play();

        third_person_gltf_tick();
    })

}

function setWeight( action, weight ) {
    action.enabled = true;
    action.setEffectiveTimeScale( 1 );
    action.setEffectiveWeight( weight );
}

function camera_follow(){
    if(third_player != null && pressKey == true){

        var x = third_player.position.x;
        var y = third_player.position.y + 2;
        var z = third_player.position.z + 2;
        third_carame.position.set(x, y, z);
        //third_carame.lookAt(third_player);
    }else{
        console.log("third player is null...")
    }

}

function third_person_gltf_tick(){
    let mixerUpdateDelta = clock.getDelta();
    if(mixer != null){
        mixer.update( mixerUpdateDelta );
    }else{
        console.log("mixer is null...")
    }
    behavior();
    //camera_follow();
}


function createGrass() {

  const geometry = new THREE.PlaneGeometry(100, 100);

  const texture = new THREE.TextureLoader().load("/static/images/grasslight-big.jpg");
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;

  texture.repeat.set(100, 100);

  const grassMaterial = new THREE.MeshBasicMaterial({ map: texture });

  grass = new THREE.Mesh(geometry, grassMaterial);

  grass.rotation.x = -0.5 * Math.PI;

  scene.add(grass);

  third_person_gltf_tick();
}


function walk_to_idle(){
    //walkAction.corssFadeTo(idleAction,1,false);
    setWeight(idleAction, 1);
    setWeight(walkAction, 0);
    setWeight(runAction, 0);
}

function walk_to_run(){

}

function idle_to_walk(){
    //idleAction.crossFadeTo(walkAction,1,false);
    setWeight(idleAction, 0);
    setWeight(walkAction, 1);
    setWeight(runAction, 0);
}




const onKeyDown = function ( event ) {
    controls.enabled = false;
    pressKey = true;

    switch ( event.code ) {

        case 'ArrowUp':
        case 'KeyW':
            moveForward = true;
            if(/*onIntersect() == true*/ false){
                speed = 0;
            }else{
                speed = 10;
            }
            third_player.translateZ (speed * clock.getDelta());
            curr_behavior = "walk";
            break;

        case 'ArrowLeft':
        case 'KeyA':
            moveLeft = true;
            curr_behavior = "turn_left";
            third_player.rotateOnAxis(new THREE.Vector3(0, 1, 0), rotate_speed*clock.getDelta());
            break;

        case 'ArrowDown':
        case 'KeyS':
            speed = 10;
            moveBackward = true;
            //third_player.position.x += -0.1;
            third_player.translateZ (-speed* clock.getDelta());
            //idle_to_walk();
            curr_behavior = "walk";
            break;

        case 'ArrowRight':
        case 'KeyD':
            moveRight = true;
            curr_behavior = "turn_right";
            third_player.rotateOnAxis(new THREE.Vector3(0, 1, 0), -rotate_speed*clock.getDelta());
            break;

        case 'Space':
            //if ( canJump === true ) velocity.y += 350;
            //canJump = false;
            break;

        case 'Shift':
            run = true;
            break;
    }
};

const onKeyUp = function ( event ) {
    controls.enabled = true;
    //controls.target = third_player.position;
    pressKey = false;
    switch ( event.code ) {

        case 'ArrowUp':
        case 'KeyW':
            moveForward = false;
            //walk_to_idle();
            curr_behavior = "idle";
            break;

        case 'ArrowLeft':
        case 'KeyA':
            moveLeft = false;
            break;

        case 'ArrowDown':
        case 'KeyS':
            moveBackward = false;
            //walk_to_idle();
            curr_behavior = "idle";
            break;

        case 'ArrowRight':
        case 'KeyD':
            moveRight = false;
            break;

        case 'Shift':
            run = false;
            break;
    }

};

function behavior(){

    if(idleAction == null || walkAction == null || runAction == null){
        return;
    }

    if(moveForward == true || moveBackward == true || moveLeft == true || moveRight == true){
        if(run == true){
            setWeight(idleAction, 0);
            setWeight(runAction, 1);
            setWeight(walkAction, 1);
        }else{
            setWeight(idleAction, 0);
            setWeight(runAction, 0);
            setWeight(walkAction, 1);
        }

    }else{

        setWeight(idleAction, 1);
        setWeight(runAction, 0);
        setWeight(walkAction, 0);

    }

}

// 获取场景中所有的物体
function getAll3DObjsInScene(){

    if(scene == null){
        return
    }
    scene.traverse(function(obj){
        getObjects(obj);
    })
    console.log(objectsInScene);
}

// 递归获取
function getObjects(obj){

    if(obj.isObject3D){
        var objs = obj.children;
        if(objs.length > 0){
            for(var i=0;i<obj.length;i++){
                if(objs[i] != third_player && objs[i] != grass){
                    objectsInScene.push(objs[i]);
                }
                getObjects(objs[i]);
            }
        }else{
            if(obj != third_player && obj != grass){
                objectsInScene.push(obj);
            }
        }
    }
}

// 碰撞检测
function onIntersect(){

    var bool = false;
    const box = new THREE.Box3().setFromObject( third_player );
    const moduleSize = new THREE.Vector3();
    // 获取角色大小尺寸
    box.getSize(moduleSize);

    // 创建一个立方体，包围住角色，从简化华碰撞检测
    const geometry = new THREE.BoxGeometry(moduleSize.x,moduleSize.y,moduleSize.z);
    const material = new THREE.MeshPhongMaterial({color: 0xfff});
    const cube = new THREE.Mesh(geometry, material);
    cube.position.x = third_player.position.x;
    cube.position.y = third_player.position.y;
    cube.position.z = third_player.position.z;

    const centerCoord = third_player.position.clone();
    const position = cube.geometry.attributes.position;
    // 顶点三位向量
    const vertices = [];
    for(let i=0; i<position.count; i++){
        vertices.push(new THREE.Vector3(position.getX(i),position.getY(i),position.getZ(i)));
    }
    for(let i=0;i<vertices.length;i++){
        // 获取世界坐标系下网格变换后的坐标
        let vertexWorldCoord = vertices[i].clone().applyMatrix4(third_player.matrixWorld);
        // 获取由中心指向定点的向量
        var dir = vertexWorldCoord.clone().sub(centerCoord);
        // 发射射线
        let raycaster = new THREE.Raycaster(centerCoord, dir.clone().normalize());
        // 放入要检测的物体，返回相交物体
        let intersects = raycaster.intersectObjects(objectsInScene, true);
        if(intersects.length > 0){
            bool = true;
            break;
        }
    }
    //console.log("onIntersect:"+bool)
    return bool;
}

export { third_person_gltf_setparames,  third_person_gltf_tick};
