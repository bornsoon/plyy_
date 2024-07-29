function tag(generate, update) {
    dt = new Date();

    if (generate === update && (generate.getDate() - dt.getDate()) < 32) {
        return 'new'
    } else if ((update.getDate() - dt.getDate()) < 32) {
        return 'update'
    }
}