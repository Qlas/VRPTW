const { gitDescribeSync } = require("git-describe");
// git-describe by default match tags by regex 'v[0-9]*'
const gitInfo = gitDescribeSync({ match: "*" });
process.env.VUE_APP_GIT_HASH = gitInfo.hash;
process.env.VUE_APP_GIT_TAG = gitInfo.tag;
process.env.VUE_APP_GIT_DISTANCE = gitInfo.distance;

module.exports = {
    outputDir: "dist",
    productionSourceMap: false,
    assetsDir: "static",
    devServer: {
        proxy: {
            "/api*": {
                // Forward frontend dev server request for /api to django dev server
                target: "http://django:8000/",
            },
        },
    },
};
