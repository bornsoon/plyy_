function plyyTag(generate, update) {
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
        return 'NEW'
    } else if ((nowTime - updateTime) < 32) {
        return 'UPDATE'
    }
}


function curatorTag(date) {
    now = new Date();
    nowTime = Math.ceil(now.getTime() / (1000 * 60 * 60 * 24));
    date = new Date(date);
    dateTime = Math.ceil(date.getTime() / (1000 * 60 * 60 * 24));
    if ((nowTime - dateTime) < 32) {
        return True
    }
}