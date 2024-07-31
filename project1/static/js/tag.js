function tag(generate, update) {
    dt = new Date();
    generate = new Date(generate)
    update = new Date(update)
    if (generate === update && (dt.getDate() - generate.getDate()) < 32) {
        return 'new'
    } else if ((dt.getDate() - update.getDate()) < 32) {
        return 'update'
    }
}