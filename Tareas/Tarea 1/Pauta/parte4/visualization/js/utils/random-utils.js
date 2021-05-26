class RandomUtils {

    static shuffle(array) {

        var currentIndex = array.length, temporaryValue, randomIndex;

        // While there remain elements to shuffle...
        while (0 !== currentIndex) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;

            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    }

    /**
     * @param {number} min
     * @param {number} max
     * @returns a random number between min (included) and max (excluded)
     */
    static getRandomInteger(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    static getRandomIndex(array) {
        return RandomUtils.getRandomInteger(0, array.length);
    }

    static getRandomElement(array) {
        return array[RandomUtils.getRandomIndex(array)];
    }

    static getRandomElements(array, numberOfElements) {

        let indexes = ArrayUtils.getIndexesFromSize(array.length);

        RandomUtils.shuffle(indexes);

        let selected = indexes.filter((e,i) => i < numberOfElements);

        return selected.map(el => array[el]);
    }

    static getRandomLevel(lines, columns, trigger=false) {

        let positions = ArrayUtils.getIndexes(lines, columns);
        let holes, wumpus, golds;

        positions = ArrayUtils.removeByValues(positions, [[0, 0]]);
        positions = ArrayUtils.removeByValues(positions, [[0, 1]]);
        positions = ArrayUtils.removeByValues(positions, [[1, 0]]);
        positions = ArrayUtils.removeByValues(positions, [[1, 1]]);

        if (trigger) {
            if (Array.isArray(trigger[4][0])) {
                holes = trigger[4];
            } else {
                holes = [trigger[4]];
            }
            positions = ArrayUtils.removeByValues(positions, holes);

            if (Array.isArray(trigger[3][0])) {
                wumpus = trigger[3];
            } else {
                wumpus = [trigger[3]];
            }
            positions = ArrayUtils.removeByValues(positions, wumpus);

            if (Array.isArray(trigger[2][0])) {
                golds = trigger[2];
            } else {
                golds = [trigger[2]];
            }
            positions = ArrayUtils.removeByValues(positions, golds);
        } else {
            holes = RandomUtils.getRandomElements(positions, 3);
            positions = ArrayUtils.removeByValues(positions, holes);

            wumpus = RandomUtils.getRandomElements(positions, 8);
            positions = ArrayUtils.removeByValues(positions, wumpus);

            golds = RandomUtils.getRandomElements(positions, 8);
            positions = ArrayUtils.removeByValues(positions, golds);
        }

        return { holes, wumpus, golds };
    }
}
