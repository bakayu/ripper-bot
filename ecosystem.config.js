module.exports = {
    apps: [{
        name: "discord-ripper-bot",
        script: "./run.sh",
        watch: false,
        env: {
            NODE_ENV: "production",
        }
    }]
}
