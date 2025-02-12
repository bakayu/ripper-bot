module.exports = {
    apps: [{
        name: "discord-ripper-bot",
        script: "./start.sh",
        watch: false,
        env: {
            NODE_ENV: "production",
        }
    }]
}