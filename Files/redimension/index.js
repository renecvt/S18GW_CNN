const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const dirname = path.join(__dirname, '../');

const gwNoiseFolder = 'qtransform';
const gwRdFolder = 'qtransform_rd';

const paths = [ { mainPath:`${dirname}${gwNoiseFolder}`, rdPath:`${dirname}${gwRdFolder}` } ];

const pairs = {};
for (const path of paths) {
  const mainExists = fs.existsSync(path.mainPath);
  const rdExists = fs.existsSync(path.rdPath);
  if (!mainExists) throw new Error(`Directory ${path.mainPath} does not exist. Did you run template generator?`);
  if (rdExists) {
    const isDirectory = fs.lstatSync(path.rdPath).isDirectory();
    if (!isDirectory) throw new Error(`Path: ${path.rdPath} is not a directory.`);
  } else {
    fs.mkdirSync(path.rdPath);
  }
  const filesInMainFolder = fs.readdirSync(path.mainPath);
  for (const file of filesInMainFolder) {
    pairs[file] = {
      mainPath: `${path.mainPath}/${file}`,
      rdPath: `${path.rdPath}/Rd${file}`,
    };
  }
}

(async () => {
  for (const key of Reflect.ownKeys(pairs)) {
    await sharp(pairs[key].mainPath)
          .resize(32, 16, { kernel: sharp.kernel.nearest })
          .ignoreAspectRatio()
          .toFile(pairs[key].rdPath);
  }
})();