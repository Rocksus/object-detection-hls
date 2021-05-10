const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;
const ffmpeg = require('fluent-ffmpeg');
ffmpeg.setFfmpegPath(ffmpegPath);

console.log("using ffmpeg path at:", ffmpegPath);

const path = require('path');

function callback() {
    console.log("done converting")
}

const inputFile = path.join(__dirname, 'input.mp4');
const outputFile = path.join(__dirname, 'streams', 'output.m3u8');

ffmpeg(inputFile, { timeout: 432000 })
    .addOptions([
        '-profile:v baseline', // baseline profile (level 3.0) for H264 video codec
        '-level 3.0',
        '-s 640x360',          // 640px width, 360px height output video dimensions
        '-start_number 0',     // start the first .ts segment at index 0
        '-hls_time 10',        // 10 second segment duration
        '-hls_list_size 0',    // Maxmimum number of playlist entries (0 means all entries/infinite)
        '-f hls'               // HLS format
    ])
    .output(outputFile)
    .on('end', callback)
    .on('error', console.error)
    .run()
