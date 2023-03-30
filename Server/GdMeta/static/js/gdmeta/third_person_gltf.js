
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
var rotate_speed = 30;

var last_behavior = "idle";
var curr_behavior = "idle";

var third_player_modele_path = "/static/modules/Xbot.glb";

function third_person_gltf_setparames(t_scene, t_camera, t_controls){

    scene = t_scene;
    third_carame = t_camera;
    controls = t_controls

    third_person_gltf_init()
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
        setWeight(idleAction, 1);
        setWeight(walkAction, 0);
        setWeight(runAction, 0);
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

  const geometry = new THREE.PlaneGeometry(1000, 1000);

  const texture = new THREE.TextureLoader().load("/static/images/grasslight-big.jpg");
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;

  texture.repeat.set(10, 10);

  const grassMaterial = new THREE.MeshBasicMaterial({ map: texture });

  const grass = new THREE.Mesh(geometry, grassMaterial);

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
            //moveForward = true;
            //third_player.position.x += -0.1;
            third_player.translateZ (speed * clock.getDelta());
            //idle_to_walk();
            curr_behavior = "walk";
            break;

        case 'ArrowLeft':
        case 'KeyA':
            //moveLeft = true;

            third_player.rotateOnAxis(new THREE.Vector3(0, 1, 0), rotate_speed*clock.getDelta());
            break;

        case 'ArrowDown':
        case 'KeyS':
            //moveBackward = true;
            //third_player.position.x += -0.1;
            third_player.translateZ (-speed* clock.getDelta());
            //idle_to_walk();
            curr_behavior = "walk";
            break;

        case 'ArrowRight':
        case 'KeyD':
            //moveRight = true;
            third_player.rotateOnAxis(new THREE.Vector3(0, 1, 0), -rotate_speed*clock.getDelta());
            break;

        case 'Space':
            //if ( canJump === true ) velocity.y += 350;
            //canJump = false;
            break;
    }
};

const onKeyUp = function ( event ) {
    controls.enabled = true;
    controls.target = third_player.position;
    pressKey = false;
    switch ( event.code ) {

        case 'ArrowUp':
        case 'KeyW':
            //moveForward = false;
            //walk_to_idle();
            curr_behavior = "idle";
            break;

        case 'ArrowLeft':
        case 'KeyA':
            //moveLeft = false;
            break;

        case 'ArrowDown':
        case 'KeyS':
            //moveBackward = false;
            //walk_to_idle();
            curr_behavior = "idle";
            break;

        case 'ArrowRight':
        case 'KeyD':
            //moveRight = false;
            break;
    }

};

function behavior(){
    if(last_behavior != curr_behavior){
        if(last_behavior == "idle" && curr_behavior == "walk"){
            idle_to_walk();
        }
        if(last_behavior == "walk" && curr_behavior == "idle"){
            walk_to_idle();
        }
    }
    last_behavior = curr_behavior;
}

export { third_person_gltf_setparames,  third_person_gltf_tick};
