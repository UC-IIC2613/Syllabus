let resources = {

    images: {},
    musics: {},

    play: function(name, override = true){

        let sound = this.musics[name];

        if (sound){
            if(override){
                sound.play();
            } else {
                if(!sound.playing()) {
                    sound.play();
                }
            }
        }
    },

    stop: function(name){

        let sound = this.musics[name];

        if (sound && sound.playing()) {
            sound.stop();
            sound.unload();
        }
    },

	loadMusic: function(name, file){

        console.log("Loading sound", file);

        return new Promise((resolve, reject) => {

            let sound = new Howl({
                src: [file],
                html5: true,
                preload: true,
            });

            sound.once('load', function(){
                resolve([name, sound]);
            });
        });
	},

    loadImage: function(name, url){

        console.log("Loading image", url);

        return new Promise((resolve, reject) => {

            var image = new Image();

            image.onload = function() {
                resolve([name, image]);
            };

            image.src = url;
        });
	},

    loadMusics: function(){

        return new Promise((resolve, reject) => {

            const files = [
                this.loadMusic("move", 'visualization/audio/bump.wav'),
                this.loadMusic("game-over", 'visualization/audio/game-over.wav'),
                this.loadMusic("win", 'visualization/audio/win.wav'),
                this.loadMusic("gold", 'visualization/audio/coin.wav'),
                this.loadMusic("arrow", 'visualization/audio/arrow.wav'),
                this.loadMusic("error", 'visualization/audio/error.mp3'),
                this.loadMusic("theme", 'visualization/audio/background.mp3')
            ];

            Promise.all(files).then((result) => {
                resolve(["musics", Object.fromEntries(result)]);
            }).catch((error) => {
                reject(error);
            });
        });
	},

	loadImages: function(){

        return new Promise((resolve, reject) => {

            const files = [
                this.loadImage('facing_to_up', 'visualization/img/player_facing_to_up.png'),
                this.loadImage('facing_to_down', 'visualization/img/player_facing_to_down.png'),
                this.loadImage('facing_to_left', 'visualization/img/player_facing_to_left.png'),
                this.loadImage('facing_to_right', 'visualization/img/player_facing_to_right.png'),
                this.loadImage('wall', 'visualization/img/wall.png'),
                this.loadImage('floor', 'visualization/img/floor.png'),
                this.loadImage('hole', 'visualization/img/hole.png'),
                this.loadImage('wumpus', 'visualization/img/wumpus.png'),
                this.loadImage('gold', 'visualization/img/gold.png'),
                this.loadImage('floor_gold', 'visualization/img/floor_gold.png'),
            ];

            Promise.all(files).then((result) => {
                resolve(["images", Object.fromEntries(result)]);
            }).catch((error) => {
                reject(error);
            });
        });
	},

    load: function(){

        var that = this;

        return new Promise((resolve, reject) => {

            const files = [
                this.loadImages(),
                this.loadMusics(),
            ];

            Promise.all(files).then((result) => {

                result = Object.fromEntries(result);

                that.images = result.images;
                that.musics = result.musics;

                resolve(result);
            }).catch((error) => {
                reject(error);
            });
        });
    }
}
