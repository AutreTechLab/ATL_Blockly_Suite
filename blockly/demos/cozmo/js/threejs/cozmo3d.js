function Cozmo() {
  var that = this;

  var cozmoTexture = new THREE.ImageUtils.loadTexture( 'img/3d/cozmo.png' );
  var cozmoMaterial = new THREE.MeshBasicMaterial( { map: cozmoTexture, side: THREE.FrontSide } );
  // var cubeMaterial = new THREE.MeshLambertMaterial( { map: cubeTexture, side: THREE.FrontSide } );

  var bodyGeometry = new THREE.CubeGeometry( 70, 30, 56 );
  var headGeometry = new THREE.CubeGeometry( 36, 36, 39.4 );

  var bodyMesh = new THREE.Mesh(bodyGeometry, cozmoMaterial);
  bodyMesh.position.x = 10;
  bodyMesh.position.y = -27;
  bodyMesh.updateMatrix();
  headGeometry.merge(bodyMesh.geometry, bodyMesh.matrix);
  that._body = new THREE.Mesh(headGeometry, cozmoMaterial);

  this.update = function(data) {
    that._body.position.x = data.x;
    that._body.position.y = data.z + 42;
    that._body.position.z = -data.y;
    var rot = data.rot;
    var quat = new THREE.Quaternion(-rot[2], -rot[0], -rot[1], rot[3])
    that._body.setRotationFromQuaternion(quat);
  };

  this.addToScene = function(scene) {
    scene.add(that._body);
  };

  this.removeFromScene = function(scene) {
    scene.remove(that._body);
  };
}

function Cube(model) {
  var that = this;

  var models = {
    'CRATE': 'img/3d/crate.jpg',
    'ZOMBIE': 'img/3d/zombiehd.png',
    'SPIDERMAN': 'img/3d/spiderman.png'
  };

  this._model = 'CRATE';
  this.setOpacity = null;

  if (model) {
    that._model = model;
  }

  if (that._model === 'CRATE') {
    var cubeTexture = new THREE.ImageUtils.loadTexture(models[model]);
    var cubeMaterial = new THREE.MeshBasicMaterial( { map: cubeTexture, side: THREE.FrontSide, transparent: true } );
    // var cubeMaterial = new THREE.MeshBasicMaterial( { color: 0x225522, side: THREE.FrontSide } );
    var cubeGeometry = new THREE.CubeGeometry( 44.3, 44.3, 44.3 );
    that._cube = new THREE.Mesh( cubeGeometry, cubeMaterial );
    that.setOpacity = function(opacity) {
      cubeMaterial.opacity = opacity;
    }

    // var geometry = new THREE.EdgesGeometry( that._cube.geometry );
    // var material = new THREE.LineBasicMaterial( { color: 0x00ff000, linewidth: 3 } );
    // var edges = new THREE.LineSegments( geometry, material );
    // that._cube.add( edges );
  } else {
    var char = new MinecraftChar(models[model]);
    that._cube = char.getRoot();
    that.setOpacity = char.setOpacity;
  }

  this.update = function(data) {
    that._cube.position.x = data.x;
    if (that._model === 'CRATE') {
      that._cube.position.y = data.z + 22.15;
    } else {
      that._cube.position.y = data.z;
    }
    if (!data.seen) {
      that.setOpacity(0);
    } else if (!data.visible) {
      that.setOpacity(0.5);
    } else {
      that.setOpacity(1);
    }
    that._cube.position.z = -data.y + 22.15;
    var rot = data.rot;
    var quat = new THREE.Quaternion(-rot[2], -rot[0], -rot[1], rot[3])
    that._cube.setRotationFromQuaternion(quat);
  };

  this.addToScene = function(scene) {
    scene.add(that._cube);
  };

  this.removeFromScene = function(scene) {
    scene.remove(that._cube);
  };

  this.getReplacement = function(model) {
    that._model = model;
    var replacement= replacement = new Cube(model);
    copyPose(that._cube, replacement._cube);
    return replacement;
  };
}

function Cozmo3d() {

  var that = this;

  this._initialized = false;
  this._id = null;
  this._scene = null;
  this._camera = null;
  this._controls = null;
  this._cozmo = null;
  this._cubes = [];
  this._anaglyph = false;
  this._models = ['CRATE', 'CRATE', 'CRATE'];

  this.init = function() {
    if (that._initialized) {
      return;
    }

    that._scene = new THREE.Scene();
    var canvas = document.getElementById("canvas_3d");
    var width = $(canvas).width();
    var height = $(canvas).height();
    that._camera = new THREE.PerspectiveCamera( 60, width/height, 0.01, 3000 );

    that._camera.position.set(0,250,300);
    // that._camera.focalLength = 3;
    that._camera.lookAt(that._scene.position);
    that._scene.add(that._camera);

    that._renderer = new THREE.WebGLRenderer({canvas: canvas, antialias: false});
    that._renderer.setSize(width, height);
    that._renderer.setPixelRatio( window.devicePixelRatio );

    that._controls = new THREE.OrbitControls( that._camera, canvas );
    that._controls.maxDistance = 1000;

    var light = new THREE.PointLight(0xffffff);
    light.position.set(-100,400,100);
    that._scene.add(light);

    // FLOOR
    var floorTexture = new THREE.ImageUtils.loadTexture( 'img/3d/grasslight-thin.jpg' );
    floorTexture.wrapS = floorTexture.wrapT = THREE.RepeatWrapping; 
    floorTexture.repeat.set( 1, 10 );
    var floorMaterial = new THREE.MeshBasicMaterial( { map: floorTexture, side: THREE.BackSide } );
    var floorGeometry = new THREE.PlaneGeometry(1000, 1000, 10, 10);
    var floor = new THREE.Mesh(floorGeometry, floorMaterial);
    // floor.position.y = -0.5;
    floor.rotation.x = Math.PI / 2;
    that._scene.add(floor);

    // SKYBOX
    var skyBoxGeometry = new THREE.CubeGeometry( 2000, 2000, 2000 );
    var skyBoxMaterial = new THREE.MeshBasicMaterial( { color: 0x9999ff, side: THREE.BackSide } );
    var skyBox = new THREE.Mesh( skyBoxGeometry, skyBoxMaterial );
    that._scene.add(skyBox);

    // COZMO
    that._cozmo = new Cozmo();
    that._cozmo.addToScene(that._scene);

    // CUBES
    for (var i = 0; i < that._models.length; i++) {
      var cube = new Cube(that._models[i]);
      cube.addToScene(that._scene);
      that._cubes.push(cube);
    }

    that._effect = new THREE.AnaglyphEffect( that._renderer, width || 2, height || 2 );

    that._initialized = true;
  };

  this.start = function() {
    if (!that._initialized) {
      return;
    }
  
    // Mock locations first to see the scene whithout any program running.
    var data = {
      "cozmo": {
        "z": 0.4872395694255829,
        "y": -83.60612487792969,
        "x": 40.18196105957031,
        "rot": [0.9496887922286987, 0, 0, 0.31319528818130493]
      },
      "cubes": [{
          "z": 55.19646072387695,
          "y": 42.23066711425781,
          "x": 205.2679443359375,
          "rot": [0.9169570803642273, -0.011252639815211296, 0.016658909618854523, 0.39847904443740845],
          "seen": true,
          "visible": true
        }, {
          "z": 11.110040664672852,
          "y": 4.5121307373046875,
          "x": 225.24978637695312,
          "rot": [0.8439759016036987, -0.016450760886073112, -0.00048563163727521896, -0.5361286401748657],
          "seen": false,
          "visible": true
        }, {
          "z": 10.047748565673828,
          "y": 60.61991882324219,
          "x": 185.5138397216797,
          "rot": [-0.35887035727500916, -0.012327473610639572, -0.02147647552192211, -0.9330589175224304],
          "seen": true,
          "visible": false
        }
      ]
    };
    that.onData(data);

    that._render();
  };
  
  this.stop = function() {
    if (!that._initialized) {
      return;
    }
    cancelAnimationFrame(that._id);
  };

  this._render = function () {
    that._id = requestAnimationFrame( that._render );

    if (that.anaglyph) {
      that._effect.render(that._scene, that._camera);
    } else {
      that._renderer.render(that._scene, that._camera);
    }

    that._controls.update();
  };

  this.toggleAnaglyph = function() {
    if (!that._initialized) {
      return;
    }
    that.anaglyph = !that.anaglyph;
  };

  this.onData = function(data) {
    if (!that._initialized) {
      return;
    }
    // console.log("received cozmo position", data, JSON.stringify(data));
    that._cozmo.update(data.cozmo);

    for (var i = 0; i < that._cubes.length; i++) {
      that._cubes[i].update(data.cubes[i]);
    }
  };

  this.setCubeModel = function(model, num) {
    console.log('Changing model for cube', model, num);
    that._models[num-1] = model;
    if (!that._initialized) {
      return;
    }
    var oldCube = that._cubes[num-1];
    var newCube = oldCube.getReplacement(model);
    oldCube.removeFromScene(that._scene);
    newCube.addToScene(that._scene);
    that._cubes[num-1] = newCube;
  };

}

function copyPose(fromObj, toObj) {
  toObj.position.copy(fromObj.position);
  toObj.rotation.copy(fromObj.rotation);
};