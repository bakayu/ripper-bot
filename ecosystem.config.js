module.exports = {
    apps: [{
        name: "rbot",
        script: "./run.sh",
        watch: false,
        env: {
            NODE_ENV: "production",
        }
    }]
}
