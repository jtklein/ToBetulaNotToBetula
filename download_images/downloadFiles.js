const fs = require("fs");
const request = require("request");
const uuidv4 = require("uuid/v4");
const isCorrupted = require("is-corrupted-jpeg");
const gm = require("gm");
const async = require("async");

if (process.argv.length < 4) {
  console.log("Not all params given");
  return;
}

const DOWNLOAD_ASYNC_LIMIT = 30;

function l(index, message) {
  console.log(`${index}: ${message}`);
}

var checkIfImageIsValid = function(filename, index, callback) {
  if (isCorrupted(filename)) {
    l(index, filename + "is corrupted!");
    fs.unlink(filename, () => {
      callback();
    });
  } else {
    // Load into gm
    gm(filename)
      .noProfile()
      .write(filename, err => {
        if (err) {
          l(index, err);
        }
        callback();
      });
  }
};

function downloadImage(url, folder, index, callback) {
  request.head(url, { timeout: 2000 }, (err, res, body) => {
    if (err) {
      return callback("Error");
    }

    if (!res || !res.headers) {
      return callback("Could not get headers");
    }

    if (
      !res.headers["content-type"] ||
      res.headers["content-type"] != "image/jpeg"
    ) {
      l(index, "Not image - content-type:", res.headers["content-type"]);
      return callback("Not an image");
    }

    const id = uuidv4();
    var fullFilename = folder + "/" + id + ".jpg";
    const resized = folder + "/resized/" + id + ".jpg";
    l(index, fullFilename);

    request(url)
      .on("error", () => {
        return callback("Error downloading image");
      })
      .pipe(fs.createWriteStream(fullFilename))
      .on("close", () => {
        // Check image is valid
        l(index, "onClose");
        checkIfImageIsValid(fullFilename, index, () => {
          // Resize images that are bigger than 1000px on w or h
          gm(fullFilename)
            .resize(1000, 1000, ">")
            .autoOrient()
            .write(resized, err => {
              if (err) {
                l(i, err);
              }
            });
          callback();
        });
      });
  });
};

console.log("Going to look at the image list - ", process.argv[2]);
console.log("We will be categorising these images as", process.argv[3]);

const baseFolder = "training_data";
const subfolder = baseFolder + "/" + process.argv[3];
const resizedFolder = subfolder + "/resized";
if (!fs.existsSync(baseFolder)) {
  console.log(`Creating base folder`, baseFolder);
  fs.mkdirSync(baseFolder);
}
if (!fs.existsSync(subfolder)) {
  console.log(`Creating sub-folder`, subfolder);
  fs.mkdirSync(subfolder);
}
if (!fs.existsSync(resizedFolder)) {
  console.log(`Creating resized folder`, resizedFolder);
  fs.mkdirSync(resizedFolder);
}

const urls = fs
  .readFileSync(process.argv[2], "utf8")
  .toString()
  .split("\n");
const slicedUrls = urls.splice(60, urls.length - 60);
console.log(urls);

var index = 0;
async.eachLimit(
  urls,
  DOWNLOAD_ASYNC_LIMIT,
  (image, cb) => {
    index++;
    l(index, "Start downloading of" + image);
    downloadImage(
      image,
      subfolder,
      index,
      err => {
        if (err) {
          l(index, err);
          console.log("Could not download");
        }
        l(index, "downloaded");
        cb();
      }
    );
  },
  () => {
    console.log("All done  ✅");
  }
);
