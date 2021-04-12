var canvas, // Canvas DOM element
  ctx,
  keys,
  env,
  isAlive = true,
  isFinished = false,
  player;

function restart(text = false) {
  // Esto debe crearlo con el mapa dado
  let pos;
  if (text) {
    let info = text
      .split(/\r?\n/)
      .map((x) => x.split(",").filter((x) => x != "").map(x => parseInt(x)));
    info[3] = info[3].reduce(function (result, value, index, array) {
        if (index % 2 === 0) result.push(array.slice(index, index + 2));
        return result;
      }, []);
    info[4] = info[4].reduce(function (result, value, index, array) {
      if (index % 2 === 0) result.push(array.slice(index, index + 2));
      return result;
    }, []);
    info[5] = info[5].reduce(function (result, value, index, array) {
      if (index % 2 === 0) result.push(array.slice(index, index + 2));
      return result;
    }, []);
    if (info[6]) {
      info[6] = info[6].reduce(function (result, value, index, array) {
        if (index % 2 === 0) result.push(array.slice(index, index + 2));
        return result;
      }, []);
    }
    env = new Environment(info[0][0], info[0][1], 64, 64, info);
    pos = [64 * info[1][0], 64 * info[1][1]];
  }

  if (!env) {
    env = new Environment(10, 7, 64, 64);
    pos = [0, 0];
  }

  // We need to create a new environment if it is the first time of the player won
  if (isFinished) {
    env = new Environment(10, 7, 64, 64);
    pos = [0, 0];
  } else {
    env.restart();
    resizeCanvas();
  }

  player = new Player(env, pos[0], pos[1]);

  $("#modal-win").modal("hide");
  $("#modal-game-over").modal("hide");
  $("#btn-remove-walls").prop("checked", false);

  resources.stop("game-over");
  resources.stop("win");
  resources.play("theme", false);

  (isAlive = true), (isFinished = false), animate();
}

// Browser window resize
function resizeCanvas() {
  canvas.width = env.width * env.i;
  canvas.height = env.height * env.j;
}

// Keyboard key down
function onKeydown(e) {
  // if (player) {
  // 	keys.onKeyDown(e);
  // };
  keys.onKeyDown(e);

  animate();
}

function update() {
  if (player.update(keys)) {
    player.score += 1;
  }

  var deadWumpus = player.kill(keys);

  if (deadWumpus) {
    // player.score += 1000;
    env.removeWumpus(deadWumpus);
  }

  var capturedGold = player.capture(keys);

  if (capturedGold) {
    // player.score += 1000;

    env.removeGold(capturedGold);

    resources.play("gold");

    if (env.golds.length == 0) {
      isFinished = true;
    }
  }

  if (env.hasAHole(player) || env.hasAWumpus(player)) {
    isAlive = false;
  }

  $("#score").html(player.score);
  $("#arrow").html(player.arrow);
  $("#gold").html(env.golds.length);

  if (!isAlive) {
    displayGameOver();
  }

  if (isFinished) {
    displayCongratulations();
  }
}

function displayGameOver() {
  $("#modal-game-over").modal("show");
  resources.play("game-over", false);
  resources.stop("theme");
}

function displayCongratulations() {
  $("#modal-win").modal("show");
  resources.play("win", false);
  resources.stop("theme");
}

function draw() {
  // Wipe the canvas clean
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (env) {
    env.draw(ctx);
  }

  if (player) {
    player.draw(ctx);
  }
}

function animate() {
  update();
  draw();
}

function getURL() {
  var url = "{";

  url += '"holes":' + encodeToArray(env.holes) + ",";
  url += '"golds":' + encodeToArray(env.golds) + ",";
  url += '"wumpus":' + encodeToArray(env.wumpus) + "}";

  return "#" + btoa(url);
}

function encodeToArray(array) {
  return JSON.stringify(array);
}

function getLink() {
  return window.location.href + getURL();
}

function loadEnvironment(hash) {
  var link = atob(hash.replace("#", ""));

  var obj = $.parseJSON(link);

  env.holes = obj.holes;
  env.golds = obj.golds;
  env.wumpus = obj.wumpus;

  animate();
}

function getCurrentVolume() {
  return localStorage.getItem("wws-volume") || 0.1;
}

function changeVolumeTo(level) {
  console.log("Changing volume to", level);

  Howler.volume(level);

  localStorage.setItem("wws-volume", level);
}

function simulation(info) {
  // Escribir simulación dada el archivo.
  // Si no hay info, mensaje de no hay archivo cargado

  // Si jugador no esta donde debería, mensaje de que debería estar ahi

  // Simulación
  let i = 0;

  if (player.x != info[1][0] || player.y != info[1][1]) {
    $("#messages").text(
      "Para simular debes estar en la posición inicial según el archivo."
    );
  }

  function myLoop() {
    setTimeout(function () {
      let [x, y] = info[5][i];
      let arrow_x, arrow_y, gold_x, gold_y, wumpus_x, wumpus_y;
      if (info[6] && info[6].length) {
        [arrow_x, arrow_y] = info[6][0];
      }
      if (info[3].length) {
        [wumpus_x, wumpus_y] = info[3][0];
      }
      if (info[2]) {
        [gold_x, gold_y] = info[2];
      }
      // Mato wumpus
      if ((player.x / 64 == arrow_x && player.y / 64 == arrow_y) && (x == wumpus_x && y == wumpus_y)) {
        keys.space = true;
        i--;
        info[6] = info[6].slice(1);
        info[3] = info[3].slice(1);
        // Izquierda
        if (player.x / 64 - 1 == x && player.y / 64 == y) {
          player.direction = FACING_TO_LEFT;
        }
        // Derecha 
        else if (player.x / 64 + 1 == x && player.y / 64 == y) {
          player.direction = FACING_TO_RIGHT;
        }
        // Arriba
        else if (player.x / 64 == x && player.y / 64 - 1 == y) {
          player.direction = FACING_TO_UP;
        }
        // Abajo
        else if (player.x / 64 == x && player.y / 64 + 1 == y) {
          player.direction = FACING_TO_DOWN;
        }
      }
      // Izquierda
      else if (player.x / 64 - 1 == x && player.y / 64 == y) {
        keys.left = true;
        player.direction = FACING_TO_LEFT;
      }
      // Derecha
      else if (player.x / 64 + 1 == x && player.y / 64 == y) {
        keys.right = true;
        player.direction = FACING_TO_RIGHT;
      }
      // Arriba
      else if (player.x / 64 == x && player.y / 64 - 1 == y) {
        keys.up = true;
        player.direction = FACING_TO_UP;
      }
      // Abajo
      else if (player.x / 64 == x && player.y / 64 + 1 == y) {
        keys.down = true;
        player.direction = FACING_TO_DOWN;
      }
      animate();
      if (i < info[5].length - 1) {
        i++;
        myLoop();
      }
      // Capturo oro
      if (player.x / 64 == gold_x && player.y / 64 == gold_y) {
        keys.enter = true;
        animate();
      }
    }, 800);
  }

  myLoop();
}

$(function () {
  console.log("Welcome to Wumpus World Simulator");

  // Declare the canvas and rendering context
  canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");
  keys = new Keys();

  $("#btn-remove-walls").change(function () {
    env.removeWalls = this.checked;
    // Remove focus
    $(this).blur();
    animate();
  });

  $(".btn-restart").click(function () {
    $("#messages").text("Para simular debes cargar nuevamente el archivo.");
    env = false;
    //fr = new FileReader();
    // console.log("hola");
    $("#fileform")[0].reset();
    restart();
  });

  $(".card-game").width(canvas.width);
  $(".card-game .card-content").height(canvas.height);

  $("#simulator").click(function () {
    // ACA Simular Juego!!
    $("#messages").text("");
    simulation(env.trigger);
    // $("#textarea-link").text(getLink());
  });

  changeVolumeTo(getCurrentVolume());

  $("#btn-volume").val(getCurrentVolume().toString());

  $("#btn-volume").change(function (event) {
    event.preventDefault();
    changeVolumeTo($(this).val());
  });

  document.getElementById("inputfile").addEventListener("change", function () {
    $("#messages").text("");
    var fr = new FileReader();
    fr.onload = function () {
      restart(fr.result);

      // Start listening for events
      window.addEventListener("keydown", onKeydown, false);

      animate();
    };

    fr.readAsText(this.files[0]);
  });

  resources.load().then(() => {
    resources.play("theme", false);

    var hash = window.location.hash;

    if (hash) {
      loadEnvironment(hash);
    }

    restart();

    resizeCanvas();

    // Start listening for events
    window.addEventListener("keydown", onKeydown, false);

    animate();
  });
});
