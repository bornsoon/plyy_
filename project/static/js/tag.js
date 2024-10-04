asof = 365

function isTag(generate, update) {
    now = new Date();
    nowTime = Math.ceil(now.getTime() / (1000 * 60 * 60 * 24));
    generate = new Date(generate);
    genTime = Math.ceil(generate.getTime() / (1000 * 60 * 60 * 24));
    if (update) {
        update = new Date(update);
        updateTime = Math.ceil(update.getTime() / (1000 * 60 * 60 * 24));
    } else {
        updateTime = 0;
    };
    if (!(update) && ((nowTime - genTime) < asof)) {
        return 'NEW'
    } else if ((nowTime - updateTime) < asof) {
        return 'UPDATE'
    };
    if ((nowTime - genTime) < asof || (nowTime - updateTime) < asof) {
        return 'True'
    }
}