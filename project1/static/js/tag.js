function tag(generate, update) {
    now = new Date();
    nowTime = Math.ceil(now.getTime() / (1000 * 60 * 60 * 24));
    generate = new Date(generate);
    generateTime = Math.ceil(generate.getTime() / (1000 * 60 * 60 * 24));
    if (update) {
        update = new Date(update);
        updateTime = Math.ceil(update.getTime() / (1000 * 60 * 60 * 24));
    } else {
        updateTime = 0;
    }
    if (!update && ((nowTime - generateTime) < 32)) {
        return 'new'
    } else if ((nowTime - updateTime) < 32) {
        return 'update'
    }
}