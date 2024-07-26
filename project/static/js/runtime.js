function song_time(time) {
    time =parseInt(time/1000)
    minute = parseInt(time / 60)
    second = time % 60
    return minute + ':' + String(second).padStart(2,"0");
}