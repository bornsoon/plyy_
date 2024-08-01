function tag(generate, update) {
    dt = new Date();
    generate = new Date(generate)
    if (update) {
        update = new Date(update)
    }
    console.log(update)
    if (!update && (dt.getDate() - generate.getDate()) < 32) {
        return 'new'
    } else if ((dt.getDate() - update.getDate()) < 32) {
        return 'update'
    }
}